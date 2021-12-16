#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import os
from pixivpy3 import *
import ctypes

def setWallPaper(pic_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pic_path, 0)

# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"
_TEST_WRITE = False

# If a special network environment is meet, please configure requests as you need.
# Otherwise, just keep it empty.
_REQUESTS_KWARGS = {
    'proxies': {
        'https': 'http://127.0.0.1:7890',
    },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

headers = {
    'referer': 'https://app-api.pixiv.net/'
}
proxies = {
    'https': 'http://127.0.0.1:7890'
}
path = os.path.expanduser('~').replace('\\', '/') + '/Pictures/Saved Pictures/'

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

def appapi_ranking(aapi):
    json_result = aapi.illust_ranking('week')
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

    print(url)
    dlPic(url)

def main():
    # app-api
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)

    aapi.auth(refresh_token=_REFRESH_TOKEN)

    appapi_ranking(aapi)

if __name__ == '__main__':
    main()
