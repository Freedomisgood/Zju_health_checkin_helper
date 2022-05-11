import base64
import hashlib
import hmac
import os.path
import time
import urllib.parse
from functools import reduce
from pathlib import Path

import requests

__author__ = 'Mrli'

CONFIG_INI_FILENAME = "push_config.ini"
CONFIG_INI_PATH = Path(__file__).resolve().parent.with_name("push_config.ini")

REMIND_MSG = """
[pusher]
pusher_type = pushplus

[serverchan]
sec_key =

[dingding]
access_token =
secret =

[pushplus]
pushplus_token = 
"""


class PusherException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class IPushUtil:
    def push(self, content: str, title: str = "") -> bool:
        pass


class PushplusPush(IPushUtil):
    def __init__(self, push_title, options: dict):
        self.pushplus_token = options.get("pushplus_token")
        self.push_title = push_title

    def push(self, content: str, title: str = "") -> bool:
        d = {
            "token": self.pushplus_token,
            "template": "markdown",
            "title": "{push_title}-{title}".format(push_title=self.push_title, title=title),
            "content": content
        }
        res = requests.post("http://www.pushplus.plus/send", data=d)
        if not (200 <= res.json().get("code") < 300):
            print(res.json())
        return 200 <= res.json().get("code") < 300


class ServerChanPush(IPushUtil):
    def __init__(self, push_title, options: dict):
        self.sec_key = options.get("sec_key")
        self.push_title = push_title

    def push(self, content: str, title: str = "") -> bool:
        data = {
            'text': "{push_title}-{title}".format(push_title=self.push_title, title=title),
            'desp': content
        }
        res = requests.post(url='https://sc.ftqq.com/{}.send'.format(self.sec_key), data=data)
        if not (res.json().get("errmsg") == "success"):
            print(res.json())
        return res.json().get("errmsg") == "success"


class DingDingPush(IPushUtil):
    URL = "https://oapi.dingtalk.com/robot/send"

    def __init__(self, push_title, options: dict):
        self.access_token = options.get("access_token")
        self.secret = options.get("secret")
        self.target_url = self.get_url()
        self.push_title = push_title

    def get_url(self):
        timestamp = round(time.time() * 1000)
        secret_enc = bytes(self.secret, encoding="utf-8")
        string_to_sign = "{}\n{}".format(timestamp, self.secret)
        string_to_sign_enc = bytes(string_to_sign, encoding="utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return self.URL + "?access_token={access_token}&timestamp={timestamp}&sign={sign}".format(
            access_token=self.access_token, timestamp=timestamp, sign=sign)

    def push(self, content: str, title: str = "") -> bool:
        msg = self.gen_markdown_msg(title, content)
        return self.send(msg)

    def send(self, message):
        resp = requests.post(self.target_url, json=message)
        return resp.json()

    @staticmethod
    def gen_text_msg(content, at=None, at_all=False):
        if at is None:
            at = []
        return {
            "msgtype": "text",
            "text": {"content": content},
            "at": {"atMobiles": at, "isAtAll": at_all},
        }

    def gen_markdown_msg(self, title, text, at=None, at_all=False):
        def generateText():
            res = ""
            # 最顶行显示标题
            res += "# " + "{}-".format(self.push_title) + title + "\n"
            # 内容
            res += text
            # at对象
            res += reduce(lambda x, y: x + "@" + y, at, "")
            return res

        return {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": generateText()
            },
            "at": {"atMobiles": at, "isAtAll": at_all},
        }


class Pusher:
    def __init__(self, logger=None):
        if logger:
            self.cout = logger.info
        else:
            self.cout = print
        self._pusher = self.init()

    def init(self):
        """
        实例化pusher
        :return:
        """
        from configparser import RawConfigParser
        cp = RawConfigParser()
        if not os.path.exists(CONFIG_INI_PATH):
            raise PusherException(
                "请创建{filename}配置文件\npusher配置信息如下:\n{msg}".format(filename=CONFIG_INI_FILENAME, msg=REMIND_MSG))
        cp.read(CONFIG_INI_PATH, encoding="utf8")
        pusher_type = cp.get("pusher", "pusher_type").lower()
        push_title = cp.get("pusher", "push_title")
        # 是否使用了pusher
        if not pusher_type:
            self.cout("初始化Pusher: 当前未配置Pusher, 如果需要推送功能, 则在{filename}".format(filename=CONFIG_INI_FILENAME))
            return None

        generator_info = dict(cp.items(pusher_type))
        # 检查pusher配置
        if pusher_type and not self._valid(generator_info):
            raise PusherException("{}_pusher配置错误，不能为空~".format(pusher_type))

        if pusher_type == "serverchan":
            return ServerChanPush(push_title, generator_info)
        elif pusher_type == "dingding":
            return DingDingPush(push_title, generator_info)
        elif pusher_type == "pushplus":
            return PushplusPush(push_title, generator_info)
        else:
            raise PusherException("不可知pusher类型~")

    @staticmethod
    def _valid(config_dict: dict):
        """
        判断字典值是否为空
        :param dict:
        :return:
        """
        for v in config_dict.values():
            if not v:
                return False
        return True

    def push(self, content: str, title: str = "") -> bool:
        if not self._pusher:
            self.cout("当前未配置pusher, 消息无法发送")
            return False
        return self._pusher.push(content, title)
