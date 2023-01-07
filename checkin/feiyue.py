import re
import time
import sys
import requests
from checkin_logger import logger
from parsel import Selector

cookies = sys.argv[1]

GAME_URL = 'https://bbs.kfpromax.com/kf_fw_ig_index.php'
BATTLE_URL = 'https://bbs.kfpromax.com/kf_fw_ig_intel.php'

headers = {
    'referer': GAME_URL,
    'cookie': cookies,
}
session = requests.session()
session.headers = headers

response = session.get(GAME_URL)
if response.status_code == 200:
    safeid = re.findall(r'(?<=safeid=).*(?=\")', response.text)
    if len(safeid) > 0:
        safeid = safeid[0]
    else:
        logger.error('Can\'t find safeid...')
        exit
else:
    logger.error(response.status_code)
    exit

data = {
    'safeid': safeid,
}

while True:
    response = session.post(BATTLE_URL, data=data)

    if response.text == 'no':
        logger.info('%s, 今日已死亡，请明日再来...' % response.text)
        break
    else:
        selector = Selector(response.text)
        info = selector.xpath('//text()').getall()
        logger.info(info)
        time.sleep(1)
