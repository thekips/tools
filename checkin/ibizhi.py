import js2py
import base64
import requests
import random
import json
import sys

CryptoJS = js2py.require('crypto-js')
token = sys.argv[1]
I = 1
index = {0: '静物', 1: '风景'}
classify_ids = {'静物': '5fac0f5e8404d300019eeb5f', '风景': '5f97ac059b97b30001021442'}

def decode_b64_aes(enc):
    key = 'aes'
    enc = base64.b64decode(enc).decode('utf-8')
    dec = CryptoJS.AES.decrypt(enc, key).toString(CryptoJS.enc.Utf8)
    return eval(dec)

ids = classify_ids[index[I]]
params = {
    'token': token,
    'param': '{"page":1e+6,"size":30,"classify_ids":"%s","v":3}' % ids,
    'path': 'wallpaper/get_list_by_classify',
}
response = requests.get('https://client.ibzhi.com/http/client', params=params)
page_num = decode_b64_aes(response.text)['totalPages']

rand = random.randint(0, page_num-1)
params = {
    'token': token,
    'param': '{"page":%s,"size":30,"classify_ids":"%s","v":3}' % (rand, ids),
    'path': 'wallpaper/get_list_by_classify',
}

response = requests.get('https://client.ibzhi.com/http/client', params=params)
info = decode_b64_aes(response.text)
info = info['data']

wallpaper = {}
index = random.randint(0, 29)
wallpaper['lock'] = info[index]['originalUrl']
index = random.randint(0, 29)
wallpaper['home'] = info[index]['originalUrl']

wallpaper = json.dumps(wallpaper, ensure_ascii=False)
print(wallpaper)
with open('wallpaper.txt', 'w', encoding='utf-8') as f:
    f.write(wallpaper)