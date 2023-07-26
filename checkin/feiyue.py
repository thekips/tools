#%%
import re
import time
import sys
import requests
import random
from checkin_logger import logger
from parsel import Selector


EXP_URL = 'https://bbs.kfpromax.com/kf_growup.php?ok=3&safeid=%s'
HALO_URL = 'https://bbs.kfpromax.com/kf_fw_ig_halo.php?do=buy&id=2&safeid=%s'
GAME_URL = 'https://bbs.kfpromax.com/kf_fw_ig_index.php'
BATTLE_URL = 'https://bbs.kfpromax.com/kf_fw_ig_intel.php'

def get_text(response):
    selector = Selector(response.text)
    return selector.xpath('//text()').getall()

cookies = sys.argv[1]

# Create session
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'cookie': cookies,
}
session = requests.session()
session.headers = headers
# logger.info(headers)


# Verify if cookie is valid.
response = session.get(GAME_URL)
if response.status_code == 200:
    safeid = re.findall(r'(?<=safeid=).*(?=\")', response.text)
    if len(safeid) > 0:
        safeid = safeid[0]
        logger.info('safeid is: %s' % safeid)
    else:
        logger.error('Login failure, Can\'t find safeid...')
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


# Halo Up
response = session.get(HALO_URL % safeid)
logger.info(get_text(response))


# Game Start
data = {
    'safeid': safeid,
}
response = session.get(GAME_URL)
while True:
    time.sleep(random.random() + 1)
    response = session.post(BATTLE_URL, data=data)

    if response.text == 'no':
        logger.info('%s, 今日已死亡，请明日再来...' % response.text)
        break
    else:
        logger.info(get_text(response))
