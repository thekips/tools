import js2py
import base64
import requests
import random
import json
import re
from checkin_logger import logger

CryptoJS = js2py.require('crypto-js')
# token = sys.argv[1]
# 0. 二次元男: 5fa93f9721284e0001059714 1. 二次元女: 5f97abc75fb6630001df6fec 2. 精选: 660a8d049755e32830ae8f39 3. 游戏: 5f97abeb5fb6630001df7024 4. 插画: 5f9bfc0251fa9f00016cc685 5. 小姐姐: 5f97ac1172a3ec0001c39f88 6. 小哥哥: 5fb3c4514d03d000019cdcb7 7. 文字控: 5f97abf5da2b3c0001f940c2 8. 静物: 5fac0f5e8404d300019eeb5f 9. 创意: 5fac14140481d90001db0c95 10. 简约: 5fb3ca84861e0d0001621e35 11. 风景: 5f97ac059b97b30001021442 12. 城市&道路: 5fb3cd8b861e0d00016225e4 13. 萌宠: 5fbcdef42aaaee000179388c 14. 个性潮图: 5fb3ccdc4d03d000019cf297 15. 速度激情: 5fb3d2b61348460001704599 16. 宇宙星云: 5fb3d1cc48eb4300019801cd 17. 影视: 5f97ac19da2b3c0001f940fa 18. 其他: 5f97ac21da2b3c0001f940fe 19. 电脑壁纸: 5fb341d2d1cb4d00014a38dd
index = {0: '静物', 1: '风景', 2: '插画', 3: '城市道路'}
#I = random.randint(0, len(index)-1)
I = 2
classify_ids = {index[0]: '5fac0f5e8404d300019eeb5f', index[1]: '5f97ac059b97b30001021442', index[2]: '5f9bfc0251fa9f00016cc685', index[3]: '5fb3cd8b861e0d00016225e4'}

def decode_b64_aes(enc):
    key = 'aes'
    enc = base64.b64decode(enc).decode('utf-8')
    dec = CryptoJS.AES.decrypt(enc, key).toString(CryptoJS.enc.Utf8)
    return eval(dec)

def get_info(ids):
    params = {
        'token': '',
        'param': '{"page":1e+6,"size":30,"classify_ids":"%s","v":3}' % ids,
        'path': 'wallpaper/get_list_by_classify',
    }
    response = requests.get('https://client.ibzhi.com/http/client', params=params)
    page_num = decode_b64_aes(response.text)['totalPages']
    page_num = int(page_num ** 0.5)

    rand = random.randint(0, page_num-1)
    params = {
        'token': '',
        'param': '{"page":%s,"size":30,"classify_ids":"%s","v":3}' % (rand, ids),
        'path': 'wallpaper/get_list_by_classify',
    }

    logger.info('Get class %s in page %d/%d' % (index[I], rand + 1, page_num))
    response = requests.get('https://client.ibzhi.com/http/client', params=params)
    info = decode_b64_aes(response.text)
    info = info['data']

    return info

ids = classify_ids[index[I]]
info1 = get_info(ids)
info2 = get_info('5fb341d2d1cb4d00014a38dd')

wallpaper = {}
wallpaper['class'] = index[I]
info_len = len(info1)
index1 = random.randint(0, info_len - 1)
wallpaper['lock'] = re.sub(r'\?.*', '', info1[index1]['originalUrl'])
index2 = random.randint(0, info_len - 1)
wallpaper['home'] = re.sub(r'\?.*', '', info1[index2]['originalUrl'])
index3 = random.randint(0, info_len - 1)
wallpaper['desktop'] = re.sub(r'\?.*', '', info2[index3]['originalUrl'])
logger.info("Choose No.%d & No.%d in %d pics" % (index1 + 1, index2 + 1, info_len))

wallpaper = json.dumps(wallpaper, ensure_ascii=False)
logger.info(wallpaper)
with open('wallpaper.txt', 'w', encoding='utf-8') as f:
    f.write(wallpaper)
