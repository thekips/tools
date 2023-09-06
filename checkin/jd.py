import re
import requests
import sys
from checkin_logger import logger

URL = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld&client=apple&clientVersion=10.0.4&networkType=wifi&osVersion=14.8.1&uuid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&openudid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&jsonp=jsonp_1645885800574_58482";

# Maybe to use...
# def replace(match):
#     if match.group(0) == ",":
#         return ';'
#     elif match.group(0) == ":":
#         return '='
#     else:
#         return ''

# def cookie_to_dict(cookie):
#     # return {item.split('=')[0]: item.split('=')[1] for item in cookie.split(';')}
#      cookie_dic = {}
#      for i in cookie.split(';'):
#          cookie_dic[i.split('=')[0]] = i.split('=')[1]
#      return cookie_dic

# def dict_to_cookie(dic):
#     dic = str(dic)
#     cookie = re.sub(r'\{|\}|\'|\ |\,|\:', replace, dic)
#     # cookie = re.sub(r'\{|\}|\'|\ ', "", dic)
#     # cookie = re.sub(r'\,', ";", cookie)
#     # cookie = re.sub(r'\:', "=", cookie)
#     return cookie

# def replace_cookie_spaces(cookie):
#     new_cookie = ''
#     for i in cookie.split():
#         new_cookie += i
#     return new_cookie

cookies = sys.argv[1]
headers  = {
    "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
    "Cookie": cookies
}
session = requests.session()
session.headers = headers

# you only need to replace pt_key after 30day
# headers["Cookie"] = replace_cookie_spaces(headers["Cookie"])
# cookie = cookie_to_dict(headers["Cookie"])
# cookie["pt_key"] = pt_key
# headers["Cookie"] = dict_to_cookie(cookie)

resp = session.post(URL)
try:
    info = re.findall(r'(?<=dailyAward).*?(?=,"beanImgUrl)', resp.text)[0] + "}"
    logger.info(info)
except:
    logger.error('Sign Failure')