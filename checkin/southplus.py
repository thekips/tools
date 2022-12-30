import sys
import re
import requests

from checkin_logger import logger

URL = 'https://www.south-plus.net/plugin.php'

cookies = sys.argv[1]

def get_info(s):
    res = re.findall(r'(?<=CDATA).*(?=\])', s)

    return res[0] if len(res) >= 1 else s

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    "cookie": cookies,
}
session = requests.session()
session.headers = headers

#领取奖励
params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job',
    'cid': '15',
    'nowtime': '1672151938011',
    'verify': 'f2807318',
}
response = session.get(URL, params=params)
logger.info(get_info(response.text))

#完成任务
params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'actions': 'job2',
    'cid': '15',
    'nowtime': '1672152113906',
    'verify': 'f2807318',
}
response = session.get(URL, params=params)
logger.info(get_info(response.text))