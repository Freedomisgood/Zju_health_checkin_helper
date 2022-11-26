# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 21:11
# @Author  : Mrli
# @File    : update_utils.py
from log_data import *

IN_SCHOOL = True
if IN_SCHOOL:
    old_data = old_in_data
    now_data = now_in_data
else:
    old_data = old_out_data
    now_data = now_out_data


def copeFlagParam():
    ss = """
    "verifyCode": cope_with_captcha(self.sess),
    "uid": new_uid,
    "id": new_id,
    'date': get_date(),
    'created': round(time.time()),
    'address': formatted_address,
    'geo_api_info': geo_api_info_dict,
    'area': ew,
    'province': address_component.get("province"),
    'city': address_component.get("city"),
    "campus": campus,
    """
    import re
    pattern = '[\"\'](\w+)[\"\']: ?(.*?),\n'
    res = re.sub(pattern, '\"\\1\": \"var\",\n', ss)
    print(res)


def getDictIntersection(a, b):
    s1 = set(a.keys())
    s2 = set(b.keys())
    return s1.intersection(s2)


def getUpdatedInfo():
    """获得当前版本的参数有哪些改动"""
    print("\n**now_data 中新增的参数~: ")
    for k, v in now_data.items():
        if k not in old_data.keys():
            print(f"'{k}': '{v}',")

    print("\n**old_data 中删除的参数: ")
    for k, v in old_data.items():
        if k not in now_data.keys():
            print(f"'{k}': '{v}',")

    print("\n**更新的值有~: ")
    key_list = getDictIntersection(now_data, old_data)
    for k in key_list:
        if old_data.get(k) != now_data.get(k) and old_data.get(k) != "var":
            print(f"[k]: {k}\n\told: {old_data.get(k)}, now: {now_data.get(k)}")


if __name__ == '__main__':
    # copeFlagParam()
    print(f"{'~'*20}当前对比的为{'校内' if IN_SCHOOL else '校外'}抓包数据{'~'*20}")
    getUpdatedInfo()
