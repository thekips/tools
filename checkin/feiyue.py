import re
import time
import sys
import requests
from checkin_logger import logger
from parsel import Selector

cookies = sys.argv[1]
EXP_URL = 'https://bbs.kfpromax.com/kf_growup.php?ok=3&safeid=%s'
GAME_URL = 'https://bbs.kfpromax.com/kf_fw_ig_index.php'
BATTLE_URL = 'https://bbs.kfpromax.com/kf_fw_ig_intel.php'

headers = {
    'cookie': cookies,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55',
}
session = requests.session()
session.headers = headers
logger.info(headers)

response = session.get(GAME_URL)
if response.status_code == 200:
    safeid = re.findall(r'(?<=safeid=).*(?=\")', response.text)
    if len(safeid) > 0:
        safeid = safeid[0]
        logger.info('safeid is: %s' % safeid)
    else:
        logger.error('Process end, Can\'t find safeid...')
        sys.exit()
else:
    logger.error(response.status_code)
    sys.exit()

# Checkin
data = {
    'safeid': safeid,
    'ok': '3',
}
response = session.get(EXP_URL % safeid)
logger.info('Check End...')

# Game
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
