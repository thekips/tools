#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import os
from pixivpy3 import *
import ctypes
import platform

SYSTEM = platform.system()
headers = {
    'referer': 'https://app-api.pixiv.net/'
}

def proxyStr():
    if SYSTEM == 'Windows':
        cmd = 'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer'
        with os.popen(cmd) as f:
            res  = f.read()
        proxy = 'http://' + re.sub(r'[^\d\.:]', '', res)
    elif SYSTEM == 'Linux':
        pass

    return proxy

def proxyDic():
    proxy = proxyStr()

    if proxy == '':
        return None
    else:
        return {'http': proxy, 'https': proxy}


def setWallPaper(pic_path):
    if SYSTEM == 'Windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pic_path, 0)
    elif SYSTEM == 'Linux':
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
        'https': proxyStr(),
    },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

path = os.path.expanduser('~').replace('\\', '/') + '/Pictures/.wallpaper/'
if not os.path.exists(path):
    os.makedirs(path)

def dlPic(url):
    path_to_file = path + url[url.rfind('/') + 1 : ]

    pic = requests.get(url, headers=headers, proxies=proxyDic())
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

    appapi_ranking(aapi, 'week')


if __name__ == '__main__':
    main()
