# -*- coding: utf-8 -*-#

"""
# @Author: github.com/qiuchen100
# @Date: 2020/5/7 00:26
# @Description:
# @Modified By:
"""
from flask_script import Command


class MovieJob(Command):

    def run(self):
        print('run job movie...')

