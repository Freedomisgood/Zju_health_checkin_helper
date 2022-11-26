# -*- coding: utf-8 -*-
# @Time    : 2022/5/10 18:02
# @Author  : Mrli
# @File    : utils.py
import datetime
import json
import re


@DeprecationWarning
def cope_with_captcha(sess):
    """识别验证码, 目前版本中不需要ocr了"""
    response = sess.get('https://healthreport.zju.edu.cn/ncov/wap/default/code')
    img_bytes = response.content
    # with open("captcha.png", "wb") as f:
    #     f.write(img_bytes)
    try:
        from ddddocr import DdddOcr
    except ImportError:
        pass
    else:
        # ocr = ddddocr.DdddOcr(det=False, ocr=True)
        res = ocr.classification(img_bytes)
        return res.upper()
    return "ocr is not installed!"


def get_day(delta=0):
    """
    获得指定格式的日期
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=delta)
    yesterday = today - oneday
    return yesterday.strftime("%Y%m%d")


def take_out_json(content):
    """
    从字符串jsonp中提取json数据
    """
    s = re.search("^jsonp_\d+_\((.*?)\);?$", content, re.S)
    return json.loads(s.group(1) if s else "{}")


def get_date():
    """Get current date"""
    today = datetime.date.today()
    return "%4d%02d%02d" % (today.year, today.month, today.day)
