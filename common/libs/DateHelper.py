"""
    created by 邱晨 on 2020/5/4 10:51 下午.
"""
import datetime


def getCurrentTime(fmt='%Y-%m-%d %H:%M:%S'):
    dt = datetime.datetime.now()
    return dt.strftime(fmt)
