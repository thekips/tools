# -*- coding:utf-8 -*-
import sys
import re
import requests
import hashlib
import time
import copy
import random
import base64

from checkin_logger import logger

# API_URL
LIKIE_URL = 'http://c.tieba.baidu.com/c/f/forum/like'
TBS_URL = 'http://tieba.baidu.com/dc/common/tbs'
SIGN_URL = 'http://c.tieba.baidu.com/c/c/forum/sign'
HOT_THREAD = 'https://tieba.baidu.com/mo/q/activity/getActivityThreadList'
AGREE_URL = 'https://tieba.baidu.com/mo/q/submit/opAgree'

URL_PAGE_SIGN = 'https://tieba.baidu.com/mo/q/usergrowth/commitUGTaskInfo'
URL_PAGE_QUERY = 'https://tieba.baidu.com/mo/q/usergrowth/showUserGrowth'

SIGN_DATA = {
    '_client_type': '2',
    '_client_version': '9.7.8.0',
    '_phone_imei': '000000000000000',
    'model': 'MI+5',
    "net_type": "1",
}

EQUAL = r'='
EMPTY_STR = r''
SIGN_KEY = 'tiebaclient!!!'
UTF8 = "utf-8"

cookies = sys.argv[1]
headers = {
    'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
}
s = requests.Session()
s.headers = headers

try:
    bduss = re.findall(r'(?<=BDUSS\=).*?(?=\;)',cookies)[0]
except:
    logger.error('ERROR COOKIES...')


def get_tbs():
    logger.info("获取tbs开始...")
    try:
        tbs = s.get(url=TBS_URL, timeout=5).json()['tbs']
    except Exception as e:
        logger.error("获取tbs出错" + e)
        logger.info("重新获取tbs开始")
        tbs = s.get(url=TBS_URL, timeout=5).json()['tbs']

    logger.info('tbs:' + tbs)
    logger.info("获取tbs结束")
    return tbs


def get_favorite(bduss):
    logger.info("获取关注的贴吧开始...")
    # 客户端关注的贴吧
    returnData = {}
    i = 1
    data = {
        'BDUSS': bduss,
        '_client_type': '2',
        '_client_id': 'wappc_1534235498291_488',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        'from': '1008621y',
        'page_no': '1',
        'page_size': '200',
        'model': 'MI+5',
        'net_type': '1',
        'timestamp': str(int(time.time())),
        'vcode_tag': '11',
    }
    data = encodeData(data)
    try:
        res = s.post(url=LIKIE_URL, data=data, timeout=5).json()
    except Exception as e:
        logger.error("获取关注的贴吧出错" + e)
        return []
    returnData = res
    if 'forum_list' not in returnData:
        returnData['forum_list'] = []
    if res['forum_list'] == []:
        return {'gconforum': [], 'non-gconforum': []}
    if 'non-gconforum' not in returnData['forum_list']:
        returnData['forum_list']['non-gconforum'] = []
    if 'gconforum' not in returnData['forum_list']:
        returnData['forum_list']['gconforum'] = []
    while 'has_more' in res and res['has_more'] == '1':
        i = i + 1
        data = {
            'BDUSS': bduss,
            '_client_type': '2',
            '_client_id': 'wappc_1534235498291_488',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            'from': '1008621y',
            'page_no': str(i),
            'page_size': '200',
            'model': 'MI+5',
            'net_type': '1',
            'timestamp': str(int(time.time())),
            'vcode_tag': '11',
        }
        data = encodeData(data)
        try:
            res = s.post(url=LIKIE_URL, data=data, timeout=5).json()
        except Exception as e:
            logger.error("获取关注的贴吧出错" + e)
            continue
        if 'forum_list' not in res:
            continue
        if 'non-gconforum' in res['forum_list']:
            returnData['forum_list']['non-gconforum'].append(res['forum_list']['non-gconforum'])
        if 'gconforum' in res['forum_list']:
            returnData['forum_list']['gconforum'].append(res['forum_list']['gconforum'])

    t = []
    for i in returnData['forum_list']['non-gconforum']:
        if isinstance(i, list):
            for j in i:
                if isinstance(j, list):
                    for k in j:
                        t.append(k)
                else:
                    t.append(j)
        else:
            t.append(i)
    for i in returnData['forum_list']['gconforum']:
        if isinstance(i, list):
            for j in i:
                if isinstance(j, list):
                    for k in j:
                        t.append(k)
                else:
                    t.append(j)
        else:
            t.append(i)
    logger.info("获取关注的贴吧结束")
    return t


def encodeData(data):
    s = EMPTY_STR
    keys = data.keys()
    for i in sorted(keys):
        s += i + EQUAL + str(data[i])
    sign = hashlib.md5((s + SIGN_KEY).encode(UTF8)).hexdigest().upper()
    data.update({'sign': str(sign)})
    return data


def client_sign(bduss, tbs, fid, kw):
    # 客户端签到
    data = copy.copy(SIGN_DATA)
    data.update({'BDUSS': bduss, 'fid': fid, 'kw': kw, 'tbs': tbs, 'timestamp': str(int(time.time()))})
    data = encodeData(data)
    res = s.post(url=SIGN_URL, data=data, timeout=5).json()
    return res

def query_rank(is_show=False):
    # 查询贴吧等级
    time.sleep(random.random())
    resp = s.get(URL_PAGE_QUERY)
    info = resp.json()['data']

    level_info = info['level_info']
    for level in level_info:
        if level['is_current'] == 1:
            rank = str(level['level'])
            exp = str(level['growth_value'])
            if is_show:
                logger.info(f'Your rank is V{rank}, EXP is {exp}')

            return int(exp)

def page_sign(tbs):
    # 贴吧等级签到
    logger.info('开始贴吧等级签到...')
    pre_exp = query_rank()

    data = {
        'tbs': tbs,
        'act_type': 'page_sign',
        'cuid': '6137F977B7F6BB0CCD5906A6D9064433',
    }
    resp = s.post(URL_PAGE_SIGN, data=data)
    logger.info(resp.json()['error'])

    cur_exp = query_rank()
    logger.info('你获得了%d点经验' % (cur_exp - pre_exp))

def hot_thread(tbs):
    params = {
        'rn': '10',
        'pn': '1',
        'sort_type': '1',
        'order_type': '1',
        'activity_name': 'excellent_thread',
    }
    resp = s.get(HOT_THREAD, params=params)

    if resp.status_code != 200:
        logger.info('Hot thread failed...')
        return

    pre_exp = query_rank()
    datas = resp.json()['data']['thread_list']
    for data in datas:
        agree = data['agree']['has_agree']

        if not agree:
            params = {
                'forum_id': data['forum_id'],
                'thread_id': data['tid'],
                'op_type': '0',
                'agree_type': '2',
                'obj_type': '3',
                'tbs': tbs,
                'is_client': '1',
                'client_type': '1',
            }
            response = requests.get(AGREE_URL, params=params, cookies=cookies, headers=headers)  

            logger.info(data['title'])
            break

    cur_exp = query_rank()
    logger.info('你获得了%d点经验' % (cur_exp - pre_exp))

def emotion_set(tbs):
    # 设置今日心情
    logger.info('设置今日心情...')
    # Maybe need to alter...
    resp = s.get('https://tieba.baidu.com/mo/q/customfigure/showCustomFigure')
    res_link = resp.json()['data']['figure_meta']['url']
    logger.info('res_link is: ' + res_link)
    resp = requests.get(res_link)
    # logger.info('resp is: ' + resp.text)
    figure_meta = base64.b64encode(resp.text.encode('utf-8'))
    figure_meta = str(figure_meta, 'utf-8')
    # logger.info('figuremeata is: ' + figure_meta)

    data = {
        'figure_meta': figure_meta,
        'tbs': '',
    }
    response = s.post('https://tieba.baidu.com/mo/q/customfigure/uploadFigureMeta', data=data)

    pre_exp = query_rank()

    emotion_list = [['放烟花', '300468284768'], ['福到了', '300468285246']]

    def submit_emotion(index):
        data = {
            'meta_type': 'url',
            'meta_value': res_link,
            'background_type': 'tone',
            'background_value': 'DBA6F5',
            'figure_pid': '300674490666',
            'background_figure_pid': '300684193294',
            'text': emotion_list[index][0],
            'icon': emotion_list[index][1],
            'tbs': '',
        }

        response = s.post(
            'https://tieba.baidu.com/mo/q/customfigure/submitCustomFigure',
            data=data,
        )
        logger.info(response.json())

    submit_emotion(0)
    time.sleep(random.randint(1,4))
    submit_emotion(1)

    cur_exp = query_rank()
    logger.info('你获得了%d点经验' % (cur_exp - pre_exp))


tbs = get_tbs()
page_sign(tbs)

emotion_set(tbs)

time.sleep(random.random())
logger.info("开始签到...")
favorites = get_favorite(bduss)
length = len(favorites)
for index, fav in enumerate(favorites):
    logger.info("[%d/%d] " % (index+1, length) + "正在签到贴吧：" + fav["name"])
    time.sleep(random.randint(1,3))
    logger.info(client_sign(bduss, tbs, fav["id"], fav["name"]))
logger.info("签到完成")