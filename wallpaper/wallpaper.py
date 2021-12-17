#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import os
from pixivpy3 import *
import ctypes
import platform

system = platform.system()
headers = {
    'referer': 'https://app-api.pixiv.net/'
}
# clash listen to 7890, you can replace it if you need.
proxies = {
    'https': 'http://127.0.0.1:7890'
}

def setWallPaper(pic_path):
    if system == 'Windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pic_path, 0)
    elif system == 'Linux':
        # use follow instruction to listen the result on terminal when changing your wallpaper and replace it.
        # 'xfconf-query -c xfce4-desktop -p /backdrop -m'
        command = 'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitorHDMI-0/workspace0/last-image -s '
        print(pic_path)
        os.system(command + pic_path)

# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"

# If a special network environment is meet, please configure requests as you need.
# Otherwise, just keep it empty.
_REQUESTS_KWARGS = {
    'proxies': {
        'https': 'http://127.0.0.1:7890',
    },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

path = os.path.expanduser('~').replace('\\', '/') + '/Pictures/.wallpaper/'
if not os.path.exists(path):
    os.makedirs(path)

def dlPic(url):
    path_to_file = path + url[url.rfind('/') + 1 : ]

    pic = requests.get(url, headers=headers, proxies=proxies)
    if pic:
        with open(path_to_file, 'wb') as f:
            f.write(pic.content)
        setWallPaper(path_to_file)
        print('Change wallpaper success!')
    else:
        dlPic(url[:-4] + '.png')

def getOri(url):
    suffix = url[url.find('/img/') : url.rfind('_p0') + 3] + url[-4:]
    url = 'https://i.pximg.net/img-original' + suffix

    return url

def appapi_ranking(aapi, mode='week'):
    json_result = aapi.illust_ranking(mode)
    index = 0
    while True:
        illust = json_result.illusts[index]
        index += 1

        url = getOri(illust.image_urls['large'])
        pic_name = url[url.rfind('/') + 1 : ]
        if illust.height < illust.width :
            a = path + pic_name
            b = a[:-4] + '.png'

            if not (os.path.exists(a) or os.path.exists(b)):
                break

    print(illust.title, url)
    dlPic(url)

def main():
    # app-api
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)
    aapi.auth(refresh_token=_REFRESH_TOKEN)

    appapi_ranking(aapi)

if __name__ == '__main__':
    main()
