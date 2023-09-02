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
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Cookie': cookies,
    'User-Agent': 'xiaoheihe/1.3.279 (com.max.xiaoheihe; build:977; iOS 16.5.1) Alamofire/5.6.4',
    'Accept-Language': 'zh-Hans-CN;q=1.0, ja-CN;q=0.9',
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


# import hmac
# import base64
# from functools import reduce
# class BlackBox:
#     def u(self, t):
#         if 128 & t:
#             return 255 & (t << 1 ^ 27)
#         else:
#             return t << 1

#     def _(self, t):
#         return self.u(t) ^ t

#     def h(self, t):
#         return self._(self.u(t))

#     def m(self, t):
#         return self.h(self._(self.u(t)))

#     def p(self, t):
#         return self.m(t) ^ self.h(t) ^ self._(t)

#     def f(self, t):
#         e = [
#             self.p(t[0]) ^ self.m(t[1]) ^ self.h(t[2]) ^ self._(t[3]),
#             self._(t[0]) ^ self.p(t[1]) ^ self.m(t[2]) ^ self.h(t[3]),
#             self.h(t[0]) ^ self._(t[1]) ^ self.p(t[2]) ^ self.m(t[3]),
#             self.m(t[0]) ^ self.h(t[1]) ^ self._(t[2]) ^ self.p(t[3]),
#         ]
#         return e

#     def hmac_sha1(self, url, time):
#         code = hmac.new(url, digestmod='sha1')
#         byte = time.to_bytes(8, 'big')
#         code.update(byte)
#         return code.digest()

#     def getHkey(self, url, time):
#         code = self.hmac_sha1(base64.b64encode(url.encode()), time + 1)
#         key = "BCDFGHJKMNPQRTVWXY23456789"
#         n = 15 & code[-1]
#         r = 2147483647 & int.from_bytes(code[n:n+4], 'big')
#         hkey = ''
#         for i in range(5):
#             d = r % len(key)
#             r = int(r / len(key))
#             hkey += key[d]
#         text = hkey[1:]
#         text_list = []
#         for i in range(len(text)):
#             text_list.append(ord(text[i]))
#         u = str(reduce(lambda t, e: t+e, self.f(text_list)) % 100)
#         if len(u) < 2:
#             u = '0' + u
#         return hkey + u

# box = BlackBox()
# sign_time = str(int(time.time()))
# url = 'https://api.xiaoheihe.cn/task/sign_v3/get_sign_state'
# time = int(time.time())
# hkey = box.getHkey(url, time)
# logger.info(hkey)
# params = {
#     'lang': 'zh-cn',
#     'os_type': 'iOS',
#     'os_version': '16.5.1',
#     '_time': sign_time,
#     'version': '1.3.262',
#     'device_id': '93FA4CBB-7EB1-4BFF-BBAF-F5F23D97307E',
#     'heybox_id': '16774945',
#     'nonce': '0SQGM2EZXVZ2Poen4MjNXT7WyDvPPCof',
#     'dw': '414',
#     'x_app': 'heybox',
#     'x_client_type': 'mobile',
#     'x_os_type': 'iOS',
#     'hkey': hkey,
# }

# response = session.get('https://api.xiaoheihe.cn/task/sign_v3/get_sign_state', params=params)
# logger.info(response.json())