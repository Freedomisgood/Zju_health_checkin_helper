# -*- coding: utf-8 -*-
# @Time    : 2022/5/10 18:04
# @Author  : Mrli
# @File    : pusher.py

# ▲.在这里设置推送pushplus!
import requests


def push2pushplus(content, token=""):
    """
    推送消息到pushplus
    """
    if token == '':
        print("[注意] 未提供token，不进行pushplus推送！")
    else:
        server_url = f"http://www.pushplus.plus/send"
        params = {
            "token": token,
            "title": 'ZJU钉钉健康打卡',
            "content": content
        }

        response = requests.get(server_url, params=params)
        json_data = response.json()
        print(json_data)
