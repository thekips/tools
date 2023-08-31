import sys
import time
import hashlib
import requests
from checkin_logger import logger
from urllib.parse import urlparse

URL_SIGN = 'https://api.xiaoheihe.cn/task/sign/'

def gen_hkey(url, sign_time):
    def url_to_path(url):
        path = urlparse(url).path
        if path and path[-1] == '/':
            path = path[:-1]
        return path
    def get_md5(data: str):
        md5 = hashlib.md5()
        md5.update(data.encode('utf-8'))
        result = md5.hexdigest()
        return result
    hkey = f'{url_to_path(url)}/bfhdkud_time={sign_time}'
    hkey = get_md5(hkey)
    hkey = hkey.replace('a', 'app')
    hkey = hkey.replace('0', 'app')
    hkey = get_md5(hkey)
    hkey = hkey[:10]
    return hkey


cookies = sys.argv[1]
sign_time = str(int(time.time()))
hkey = gen_hkey(URL_SIGN, sign_time)

headers = {
    'Cookie': cookies,
    'Referer': 'http://api.maxjia.com/',
}
session = requests.session()
session.headers = headers

params = {
    'heybox_id': '16774945',
    'imei': '8be4ead13ab97cc6',
    'os_type': 'iOS',
    'os_version': '16.5.1',
    # '_time': int(time.time()),
    '_time': sign_time,
    'version': '1.3.118',
    'channel': 'heybox_xiaomi',
    'hkey': hkey
}


response = session.get(URL_SIGN, params=params)
logger.info(response.json())