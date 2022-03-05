#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import ctypes
import platform
import re

URL = 'https://api.iyk0.com/mryt/'
SYSTEM = platform.system()
PATH = os.path.expanduser("~").replace("\\", "/") + "/Pictures/.wallpaper/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

def sysProxy():
    if SYSTEM == 'Windows':
        cmd = 'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer'
        with os.popen(cmd) as f:
            res  = f.read()
        proxy = 'http://' + re.sub(r'[^\d\.:]', '', res)
    elif SYSTEM == 'Linux':
        pass

    if proxy == '':
        return None
    else:
        return {'http': proxy, 'https': proxy}
        

def setWallpaper(pic_path):
    if SYSTEM == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pic_path, 0)
    elif SYSTEM == "Linux":
        # use follow instruction to listen the result on terminal when changing your wallpaper and replace it.
        # 'xfconf-query -c xfce4-desktop -p /backdrop -m'
        command = "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitorHDMI-0/workspace0/last-image -s "
        print(pic_path)
        os.system(command + pic_path)


def dlPic(url, pic_path):
    pic = requests.get(url, proxies=sysProxy())
    if pic:
        with open(pic_path, "wb") as f:
            f.write(pic.content)

def bingAPI():
    res = requests.get(URL, proxies=sysProxy())
    json_result = res.json()['data']
    index = 0
    while True:

        url = json_result[index]['imgurl']
        pic_name = url[url.find("=") + 1 : url.find('&')]
        pic_path = PATH + pic_name
        index += 1

        if not os.path.exists(pic_path):
            break

    print(pic_name, url)
    dlPic(url, pic_path)
    setWallpaper(pic_path)
    print("Change wallpaper success!")


def main():
    bingAPI()


if __name__ == "__main__":
    main()
