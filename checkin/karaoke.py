import requests
import time
import random
import sys
from checkin_logger import logger

session = requests.session()

URL_QUERY = 'https://node.kg.qq.com/vMission'
URL_SIGN = 'http://httpdns.kg.qq.com/api/v1/d'
cookies = sys.argv[1]

headers = {
    'Cookie': cookies,
}
session = requests.session()
session.headers = headers

def query_wallet():
    params = {
        "outCharset": 'utf-8',
        "format": "json",
    }

    resp = session.get(URL_QUERY, params=params)
    info = resp.json()
    info = info['data']['user']['data']

    point_num = info['stIntegral']['lAmount']
    flower_num = info['stFlower']['lAmount']
    logger.info(f'point: {point_num}, flower: {flower_num}')


query_wallet()

# Sign
time.sleep(random.random())
params = {
    'host': 'wns.kg.qq.com',
    'sign': '09f1e75d0296fc07e4aabef21cd1cc57', # Alter this if Fail to sign
}
resp = session.get(URL_SIGN, params=params)
if resp.json()['retCode'] == 0:
    logger.info('Sign Success!')
else:
    logger.info('Sign Failure...')

time.sleep(random.random())
query_wallet()