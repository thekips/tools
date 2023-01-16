import sys
import requests
import json
from checkin_logger import logger

# 设置Server酱post地址 不需要可以删除
serverChan = "https://sc.ftqq.com/*****************************************.send"
# 状态地址
current_url = 'https://zhiyou.smzdm.com/user/info/jsonp_get_current'
# 签到地址
checkin_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

# SMZDM_COOKIE
cookies = sys.argv[1]
headers = {
    'Referer': 'https://www.smzdm.com/',
    'Host': 'zhiyou.smzdm.com',
    'Cookie': cookies,
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
session = requests.session()
session.headers = headers


def req(url):
    url = url
    res = session.get(url)
    if res.status_code == 200:
        data = json.loads(res.text)
        logger.info('data is:', data)
        return data


data = req(current_url)
if data['checkin']['has_checkin']:
    info = '%s 你目前积分：%s，经验值：%s，金币：%s，碎银子：%s，威望：%s，等级：%s，已经签到：%s天' % (data['nickname'], data['point'], data['exp'], data['gold'], data['silver'], data['prestige'], data['level'],data['checkin']['daily_checkin_num'])
    logger.info(info)
else:
    checkin = req(checkin_url)['data']
    if checkin != []: 
        info = '%s 目前积分：%s，增加积分：%s，经验值：%s，金币：%s，威望：%s，等级：%s' % (data['nickname'], checkin['point'], checkin['add_point'], checkin['exp'], checkin['gold'], checkin['prestige'], checkin['rank'])
        logger.info(info)