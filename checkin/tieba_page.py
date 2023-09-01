import requests
import time
import random
from checkin_logger import logger

URL_PAGE_SIGN = 'https://tieba.baidu.com/mo/q/usergrowth/commitUGTaskInfo'
URL_PAGE_QUERY = 'https://tieba.baidu.com/mo/q/usergrowth/showUserGrowth'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Sec-Fetch-Mode': 'cors',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Origin': 'https://tieba.baidu.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 tieba/12.46.1.0 uniqueId/65D98A7F765416C01E554DBB9EDADFEFFDFDBA873OBHJJHNMOQ skin/default',
    'Cookie': 'USER_JUMP=-1; BAIDUCUID=gaSItjiD2a_Du2i8_uHEigifvi__8Haxj8SIu0ipHa0n8HaUl8Bj8gtsHOrutWP5909mA; BAIDUZID=VmS2TWFHW_hdQjWd6sX15Yf3o1iH2LtqX3ycop7edYIgxM5YYG01CxeM03HpmZQAFQnp7XcYnIMo2DGAKD6iCyA; BDUSS=kdTejVRTFN-eUhQVXhZREpycGMycWFWWWNUdk5-T3lhfm94OEtxRWF2OXJ1UmxqSUFBQUFBJCQAAAAAAAAAAAEAAACLgnw1ucK2wG~X7wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGss8mJrLPJiV; CUID=6137F977B7F6BB0CCD5906A6D9064433; TBBRAND=iPhone; TBCOOKIEVERSION=12.46.1.0; _client_version=12.46.1.0; caid=%7B%22caid%22%3A%5B%7B%22vendor%22%3A%220%22%2C%22generateTime%22%3A%221693470428%22%2C%22caid%22%3A%5B%7B%22version%22%3A%2200%22%2C%22caid%22%3A%2200_FA8E11251BE0C35364FA2A5FE8CD9E4F_497D4876A2EAA748FC2506E1E573167D%22%7D%5D%7D%2C%7B%22vendor%22%3A%221%22%2C%22generateTime%22%3A%221693470428%22%2C%22caid%22%3A%5B%7B%22version%22%3A%2220220111%22%2C%22caid%22%3A%2233e9d21511c06b10df487cf48841b038%22%7D%2C%7B%22version%22%3A%2220230330%22%2C%22caid%22%3A%223091c53214415bc891f06e22a0a0d2a2%22%7D%5D%7D%2C%7B%22vendor%22%3A%222%22%2C%22generateTime%22%3A%221693454514%22%2C%22caid%22%3A%5B%7B%22version%22%3A%2200%22%2C%22caid%22%3A%2235D33E73-7081-AA6A-BACD-CE634EACC5E4%22%7D%5D%7D%5D%2C%22factors_data%22%3A%22ewogICJmYWN0b3JzVmVyc2lvbiIgOiAiMyIsCiAgImZhY3RvcnNGb3JDYWlkIiA6IHsKICAgICJwaHlzaWNhbE1lbW9yeSIgOiAiMzExODIxOTI2NCIsCiAgICAiY2FycmllckluZm8iIDogIuS4reWbveeUteS%5C%2FoSIsCiAgICAibWFjaGluZSIgOiAiaVBob25lMTAsMiIsCiAgICAic3lzRmlsZVRpbWUiIDogIjE2ODc0NTI2NzYuMzgzMjEwIiwKICAgICJjb3VudHJ5Q29kZSIgOiAiQ04iLAogICAgImJvb3RTZWNUaW1lIiA6ICIxNjkzNDA4MDI0IiwKICAgICJkZXZpY2VOYW1lIiA6ICI4NjdFNTdCRDA2MkM3MTY5OTk1REMwM0NDMDU0MUMxOSIsCiAgICAidGltZVpvbmUiIDogIjI4ODAwIiwKICAgICJsYW5ndWFnZSIgOiAiemgtSGFucy1DTiIsCiAgICAiZGlzayIgOiAiMjU1OTc4OTgzNDI0IiwKICAgICJzeXN0ZW1WZXJzaW9uIiA6ICIxNi41LjEiLAogICAgImNwdU51bWJlciIgOiAiNiIsCiAgICAibW9kZWwiIDogIkQyMUFQIiwKICAgICJtb2JCaXJ0aFRpbWUiIDogIjE2NTgwNzAzOTMuNjE1MjMxNDQwIgogIH0KfQ%3D%3D%22%2C%22caid_valid%22%3A%221%22%7D; pure_mode=0; xcx_mode=0; STOKEN=075904193853888ce31e827fcac5cad54e4662e5ac7c0e7104f5e574357138a3; SP_FW_VER=3.590.5; __bid_n=189022cb2f73728c8b5146; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1690197296,1690286211; CLIENTHEIGHT=736; CLIENTWIDTH=414; TIEBAUID=b285b4ca266ae81ba2f25e49; PSTM=1673340809; BAIDUID=5B20B903A75983B34C1D998AD7A858B4:FG=1; BAIDU_WISE_UID=wapp_1665220019569_43; BAIDUID_BFESS=3CEDA3DFA4A2AD4293AB9C9B553994F6:FG=1',
}

data = {
    'tbs': 'd91a40aebcdd97ec1693470441',
    'act_type': 'page_sign',
    'cuid': '6137F977B7F6BB0CCD5906A6D9064433',
}

session = requests.session()
session.headers = headers
resp = session.post(URL_SIGN, data=data)
logger.info(resp.json()['error'])

def query_rank():

    time.sleep(random.random())
    resp = session.get(URL_QUERY)
    info = resp.json()['data']

    level_info = info['level_info']
    for level in level_info:
        if level['is_current'] == 1:
            rank = str(level['level'])
            exp = str(level['growth_value'])
            logger.info(f'Your rank is V{rank}, EXP is {exp}')
            break

query_rank()