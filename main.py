# -*- coding: utf-8 -*-
# @Time    : 2022/5/10 17:59
# @File    : main.py
"""
健康打卡启动脚本
"""
__author__ = "Mrli"

import os

from helper.exceptions import ParamError
from helper.health_checkin_helper import HealthCheckInHelper


def _init_parser():
    """获得CLI参数"""
    from argparse import ArgumentParser

    parser = ArgumentParser("自动打卡脚本v2")
    parser.add_argument("-a", "--account", type=str, required=True, help="统一认证平台账号")
    parser.add_argument("-p", "--password", type=str, required=True, help="统一认证平台密码")
    parser.add_argument("-lng", "--longitude", type=str, required=True, help="定位经度")
    parser.add_argument("-lat", "--latitude", type=str, required=True, help="定位纬度")
    parser.add_argument("-c", "--campus", type=str, required=True, help="校区")
    return parser.parse_args()


if __name__ == '__main__':
    args = _init_parser()
    s = HealthCheckInHelper(args.account, args.password)
    s.run(lng=args.longitude, lat=args.latitude, campus=args.campus, delay_run=False)
