import js2py
import base64
import requests
import random
import json
import re
from checkin_logger import logger

CryptoJS = js2py.require('crypto-js')
# token = sys.argv[1]
index = {0: '静物', 1: '风景', 2: '插画', 3: '城市道路'}
I = random.randint(0, len(index)-1)
classify_ids = {index[0]: '5fac0f5e8404d300019eeb5f', index[1]: '5f97ac059b97b30001021442', index[2]: '5f9bfc0251fa9f00016cc685', index[3]: '5fb3cd8b861e0d00016225e4'}

def decode_b64_aes(enc):
    key = 'aes'
    enc = base64.b64decode(enc).decode('utf-8')
    dec = CryptoJS.AES.decrypt(enc, key).toString(CryptoJS.enc.Utf8)
    return eval(dec)


logger.info('Get class %s' % index[I])
ids = classify_ids[index[I]]
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

response = requests.get('https://client.ibzhi.com/http/client', params=params)
info = decode_b64_aes(response.text)
info = info['data']

wallpaper = {}
wallpaper['class'] = index[I]
info_len = len(info)
logger.info(info_len)
index = random.randint(0, info_len - 1)
wallpaper['lock'] = re.sub(r'\?.*', '', info[index]['originalUrl'])
index = random.randint(0, info_len)
wallpaper['home'] = re.sub(r'\?.*', '', info[index]['originalUrl'])

wallpaper = json.dumps(wallpaper, ensure_ascii=False)
logger.info(wallpaper)
with open('wallpaper.txt', 'w', encoding='utf-8') as f:
    f.write(wallpaper)
