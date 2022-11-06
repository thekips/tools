#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from weakref import proxy
import requests
import sys
import os
from pixivpy3 import *
import platform


def get_sys_proxy():
    if SYSTEM == "Windows":
        with os.popen(REG_PROXY) as f:
            res = f.read()
        proxy = "http://" + re.sub(r"[^\d\.:]", "", res)
    elif SYSTEM == "Linux":
        pass

    if proxy == "":
        return None
    else:
        return {"http": proxy, "https": proxy}


def get_pic_url(url):
    suffix = url[url.find("/img/") : url.rfind("_p0") + 3] + url[-4:]
    url = "https://i.pximg.net/img-original" + suffix

    return url


def dl_pic(url, path_to_file, proxy):
    if os.path.exists(path_to_file):
        print("PASS")
        return

    headers = {"referer": "https://app-api.pixiv.net/"}
    try:
        pic = requests.get(url, headers=headers, proxies=proxy)
        if pic:
            with open(path_to_file, "wb") as f:
                f.write(pic.content)
    except:
        dl_pic(url[:-4] + ".png", path_to_file, proxy)


def dl_ranking(aapi, path, proxy, mode="week"):
    json_result = aapi.illust_ranking(mode)
    illusts = json_result.illusts

    cnt = 0
    while True:

        for illust in illusts:
            url = get_pic_url(illust.image_urls["large"])

            path_to_file = (
                path + url[url.rfind("/") + 1 : -4] + "#" + illust.title + ".jpg"
            )

            if os.path.exists(path_to_file):
                print(illust.title, "PASS")
                continue

            print(cnt, illust.title, url)
            dl_pic(url, path_to_file, proxy)

            cnt += 1
            if cnt == 100:
                break

        if cnt == 100:
            break
        next_qs = aapi.parse_qs(json_result.next_url)
        json_result = aapi.illust_ranking(**next_qs)
        illusts = json_result.illusts


SYSTEM = platform.system()
REG_PROXY = 'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer'
# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"

# If a special network environment is meet, please configure requests as you need.
# Otherwise, just keep it empty.
_REQUESTS_KWARGS = {
    "proxies": {
        "https": get_sys_proxy().get("http"),
    },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}


def main(mode="week"):
    path = os.path.expanduser("~") + "/Pictures/Pixiv/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Create AppPixivAPI class
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)
    aapi.auth(refresh_token=_REFRESH_TOKEN)

    proxy = get_sys_proxy()
    dl_ranking(aapi, path, proxy, mode)


if len(sys.argv) >= 2:
    main(sys.argv[1])
else:
    main()
