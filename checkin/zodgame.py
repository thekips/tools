import requests
import re
import sys
from checkin_logger import logger

# ZODGAME_COOKIE
cookie = sys.argv[1]

# tgbot机器人配置,为空为不启用
bottoken = ''
chatid = ''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.146 Safari/537.36 ',
    'cookie': cookie
}


def get_user_info():
    # 获取积分
    s = requests.Session()
    user_url = 'https://zodgame.xyz/home.php?mod=spacecp&ac=credit'
    try:
        user_r = s.get(url=user_url, headers=headers)
        user_page = user_r.text.encode(
            user_r.encoding).decode(user_r.apparent_encoding)
        # print(user_page)
        user_info_re = '<input type="hidden" name="formhash" value="(.*?)" />.*title="访问我的空间">(.*?)</a>.*</ul><ul class="creditl mtm bbda cl"><li class="xi1 cl"><em>.(.*?).</em>(.*?).&nbsp;'
        user_info = re.findall(user_info_re, user_page, re.S)
        # print(user_info)
        if len(user_info) > 0:
            formhash, username, points_name, points_num = user_info[0]
            # print(points_name,points_num)
            return s, formhash, username, points_name, points_num
        else:
            logger.info('未获取到数据,疑似cookie失效')
            tg_bot('未获取到数据,疑似cookie失效')
            exit()
    except Exception as error:
        logger.error(error)
        logger.error("zodgame签到出错")


def zodgame():
    s, formhash, username, points_name, points_num = get_user_info()
    # print('用户:{}\n{}{}'.format(username,points_name, points_num))
    url = 'https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
    data = {
        'formhash': formhash,
        'qdxq': 'kx',
    }
    try:
        r = s.post(url=url, data=data, headers=headers)
        page_text = r.text.encode(r.encoding).decode(r.apparent_encoding)
        if "已被系统拒绝" in page_text:
            tg_bot('zodgame的cookie已过期')
            logger.info("zodgame的cookie已过期")
        elif "恭喜" in page_text:
            s, formhash, username, points_name, points_num = get_user_info()
            logger.info('zodgame签到成功!\n用户:{}\n{}{}'.format(
                username, points_name, points_num))
            tg_bot('zodgame签到成功!\n用户:{}\n{}{}'.format(
                username, points_name, points_num))
        elif '已经签到' in page_text:
            tg_bot('zodgame已经签到了')
            logger.info('zodgame已经签到了')
        else:
            logger.error(page_text)
            tg_bot('zodgame签到出错')
    except Exception as error:
        logger.error(error)
        logger.error("zodgame签到出错")


def tg_bot(text):
    if bottoken and chatid:
        tgcurl = 'https://api.telegram.org/bot{}/sendMessage'.format(bottoken)
        data = {
            "chat_id": chatid,
            "text": text
        }
        requests.post(tgcurl, data=data)


if __name__ == '__main__':
    if cookie:
        zodgame()
    else:
        logger.error('您未配置cookie')