# -*- coding: utf-8 -*-#

"""
# @Author: github.com/qiuchen100
# @Date: 2020/5/6 22:03
# @Description:
# @Modified By:
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def aps_test():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


scheduler = BlockingScheduler()
scheduler.add_job(aps_test, "cron", second='*/5')

scheduler.start()

