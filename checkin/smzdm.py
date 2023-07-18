import json
import re
import time
import requests
import hashlib
import sys
import prettytable as pt

from checkin_logger import logger
from random import randint
from urllib.parse import unquote

#SMZDM_COOKIE
cookies = sys.argv[1]

class SmzdmBot:
    SIGN_KEY = "zok5JtAq3$QixaA%mncn*jGWlEpSL3E1"   # iOS
    # SIGN_KEY = "apr1$AwP!wRRT$gJ/q.X24poeBInlUJC"   # Android

    def __init__(self, ANDROID_COOKIE: str, SK=None, **kwargs):
        self.cookies = unquote(ANDROID_COOKIE)
        self.sk = SK
        self.cookies_dict = self._cookies_to_dict()

        self.session = requests.Session()
        self.session.headers.update(self._headers())

    def _timestamp(self):
        sleep = randint(1, 5)
        time.sleep(sleep)
        timestamp = int(time.time())
        return timestamp

    def _cookies_to_dict(self):
        cookies_dict = {k: v for k, v in re.findall("(.*?)=(.*?);", self.cookies)}
        return cookies_dict

    def _user_agent(self):
        try:
            device_smzdm = self.cookies_dict["device_smzdm"]
            device_smzdm_version = self.cookies_dict["device_smzdm_version"]
            device_smzdm_version_code = self.cookies_dict["device_smzdm_version_code"]
            device_system_version = self.cookies_dict["device_system_version"]
            device_type = self.cookies_dict["device_type"]
            user_agent = f"smzdm_{device_smzdm}_V{device_smzdm_version} rv:{device_smzdm_version_code} ({device_type};{device_smzdm.capitalize()}{device_system_version};zh)smzdmapp"
        except KeyError:
            user_agent = "smzdm_android_V10.4.26 rv:866 (MI 8;Android10;zh)smzdmapp"
        return user_agent

    def _headers(self):
        headers = {
            "User-Agent": self._user_agent(),
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            **{
                "Request_Key": f"{randint(10000000, 100000000) * 10000000000 + self._timestamp()}",
                "Cookie": self.cookies,
            },
        }
        return headers

    def _web_headers(self):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Referer": "https://m.smzdm.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
        }
        return headers

    def _sign_data(self, data):
        sign_str = (
            "&".join(f"{key}={value}" for key, value in sorted(data.items()) if value)
            + f"&key={self.SIGN_KEY}"
        )
        sign = hashlib.md5(sign_str.encode()).hexdigest().upper()
        data.update({"sign": sign})
        return data

    def data(self, extra_data=None):
        data = {
            "weixin": "1",
            "captcha": "",
            "f": self.cookies_dict["device_smzdm"],
            "v": self.cookies_dict["device_smzdm_version"],
            "touchstone_event": "",
            "time": self._timestamp() * 1000,
            "token": self.cookies_dict["sess"],
        }
        if self.sk:
            data.update({"sk": self.sk})
        if extra_data:
            data.update(extra_data)
        return self._sign_data(data)

    def request(self, method, url, params=None, extra_data=None):
        data = self.data(extra_data)
        return self.session.request(method, url, params=params, data=data)


class SmzdmTasks:
    def __init__(self, bot: SmzdmBot) -> None:
        self.bot = bot

    def checkin(self):
        url = "https://user-api.smzdm.com/checkin"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            resp_data = resp.json()["data"]
            checkin_num = resp_data["daily_num"]
            gold = resp_data["cgold"]
            point = resp_data["cpoints"]
            exp = resp_data["cexperience"]
            rank = resp_data["rank"]
            cards = resp_data["cards"]
            tb = pt.PrettyTable()
            tb.field_names = ["签到天数", "金币", "积分", "经验", "等级", "补签卡"]
            tb.add_row([checkin_num, gold, point, exp, rank, cards])
            logger.info(f"\n{tb}")
            msg = f"""\n签到成功{checkin_num}天
            金币: {gold}
            积分: {point}
            经验: {exp}
            等级: {rank}
            补签卡: {cards}"""
            return msg
        else:
            logger.error("Faile to sign in")
            logger.info(resp.text)
            msg = "Fail to login in"
            return msg

    def vip_info(self):
        msg = ""
        url = "https://user-api.smzdm.com/vip"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            resp_data = resp.json()["data"]
            rank = resp_data["vip"]["exp_level"]
            exp_current_level = resp_data["vip"]["exp_current_level"]
            exp_level_expire = resp_data["vip"]["exp_level_expire"]
            tb = pt.PrettyTable()
            tb.field_names = ["值会员等级", "值会员经验", "值会员有效期"]
            tb.add_row([rank, exp_current_level, exp_level_expire])
            logger.info(f"\n{tb}")
            msg = f"""
            值会员等级: {rank}
            值会员经验: {exp_current_level}
            值会员有效期: {exp_level_expire}"""
        return msg

    def all_reward(self):
        msg = ""
        url = "https://user-api.smzdm.com/checkin/all_reward"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            resp_data = resp.json()["data"]
            if resp_data["normal_reward"]["gift"]["title"]:
                msg = f"\n{resp_data['normal_reward']['gift']['title']}: {resp_data['normal_reward']['gift']['content_str']}"
            elif resp_data["normal_reward"]["gift"]["content_str"]:
                msg = f"\n{resp_data['normal_reward']['gift']['content_str']}: {resp_data['normal_reward']['gift']['sub_content']}"
            logger.info(msg)
        else:
            logger.info("No reward today")
        return msg

    def _get_lottery_chance(self, params):
        headers = self.bot._web_headers()
        url = "https://zhiyou.smzdm.com/user/lottery/jsonp_get_current"
        resp = self.bot.session.get(url, headers=headers, params=params)
        try:
            result = json.loads(re.findall("({.*})", resp.text)[0])
            if result["remain_free_lottery_count"] < 1:
                logger.warning("No lottery chance left")
                return False
            else:
                return True
        except Exception:
            logger.warning("No lottery chance left")
            return False

    def _draw_lottery(self, params):
        msg = """
            没有抽奖机会
        """
        headers = self.bot._web_headers()
        url = "https://zhiyou.smzdm.com/user/lottery/jsonp_draw"
        resp = self.bot.session.get(url, headers=headers, params=params)
        try:
            result = json.loads(re.findall("({.*})", resp.text)[0])
            msg = f"""
            {result["error_msg"]}"""
        except Exception:
            logger.warning("Fail to parser lottery result")
        return msg

    def lottery(self):
        msg = """
            没有抽奖机会
        """
        timestamp = self.bot._timestamp()
        params = {
            "callback": "jQuery34100013381784658652585_{timestamp}",
            "active_id": "A6X1veWE2O",
            "_": timestamp,
        }
        if self._get_lottery_chance(params):
            msg = self._draw_lottery(params)
        return msg

    def extra_reward(self):
        continue_checkin_reward_show = False
        userdata_v2 = self._show_view_v2()
        try:
            for item in userdata_v2["data"]["rows"]:
                if item["cell_type"] == "18001":
                    continue_checkin_reward_show = item["cell_data"][
                        "checkin_continue"
                    ]["continue_checkin_reward_show"]
                    break
        except Exception as e:
            logger.error(f"Fail to check extra reward: {e}")
        if not continue_checkin_reward_show:
            return
        url = "https://user-api.smzdm.com/checkin/extra_reward"
        resp = self.bot.request("POST", url)
        logger.info(resp.json()["data"])

    def _show_view_v2(self):
        url = "https://user-api.smzdm.com/checkin/show_view_v2"
        resp = self.bot.request("POST", url)
        if resp.status_code == 200 and int(resp.json()["error_code"]) == 0:
            return resp.json()


def main():
    msg = ""

    bot = SmzdmBot(cookies)
    tasks = SmzdmTasks(bot)
    msg += tasks.checkin()
    msg += tasks.vip_info()
    msg += tasks.all_reward()
    tasks.extra_reward()
    msg += tasks.lottery()

main()
