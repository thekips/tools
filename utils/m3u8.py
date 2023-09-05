import os
import requests
import ffmpeg
import sys
from concurrent.futures import ThreadPoolExecutor
from lxml import etree

def get_m3u8_url(url):
    response = requests.get(url)
    html = etree.HTML(response.text)
    video = html.xpath('//*[@id="video-play"]')

    return video[0].get('data-src')

def dlVideo(segment_url, i):
    try:
        segment_filename = os.path.join(output_dir, f'segment_{i}.ts')
        print(segment_url)
        if os.path.exists(segment_filename):
            print(f'Exist {segment_filename}')
            return

        segment_response = requests.get(segment_url)
        if segment_response.status_code == 200:
            with open(segment_filename, 'wb') as segment_file:
                segment_file.write(segment_response.content)
        else:
            print(f"Failed to download segment {i}")
            dlVideo(segment_url)
    except:
        # dlVideo(segment_url)
        print(f"Retry to download segment {segment_url}")
        dlVideo(segment_url)

# 获得M3U8 URL和保存目录
url = sys.argv[1]
m3u8_url = get_m3u8_url(url)
output_dir = os.path.join(os.getcwd(), 'data')

# 创建保存目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 下载M3U8文件
print(m3u8_url)
response = requests.get(m3u8_url)
if response.status_code == 200:
    m3u8_content = response.text

    # 解析M3U8文件，获取视频片段URL
    base_url = m3u8_url[:m3u8_url.rfind('/')+1]
    
    segments = [line.strip() for line in m3u8_content.split('\n') if line and not line.startswith('#')]
    segments = [base_url + x for x in segments if x.find('http') == -1]
    i_list = [x for x in range(len(segments))]


    # 下载视频片段
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(dlVideo, segments, i_list)

    output_filename = os.path.join(output_dir, 'output.mp4')
    segment_files = [os.path.join(output_dir, f'segment_{i}.ts') for i in range(len(segments))]
    if not os.path.exists(output_filename):
        # 合并视频片段
        input_files = [ffmpeg.input(file) for file in segment_files]

        # 使用ffmpeg进行合并
        concated = ffmpeg.concat(*input_files)
        output = ffmpeg.output(concated, output_filename, strict='experimental')
        # 运行FFmpeg命令
        ffmpeg.run(output)

    for f in segment_files:
        os.remove(f)
    print(f"Video saved as {output_filename}")
else:
    print("Failed to fetch M3U8 file")
