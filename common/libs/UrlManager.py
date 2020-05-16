"""
    created by 邱晨 on 2020/5/3 10:04 下午.
"""
from application import app
from common.libs.DateHelper import getCurrentTime
import os


class UrlManager(object):

    @staticmethod
    def buildUrl(path):
        config_domain = app.config['DOMAIN']
        return '{}{}'.format(config_domain['www'], path)

    @staticmethod
    def buildStaticUrl(path):
        path = '/static' + path + '?ver=' + UrlManager.getReleaseVersion()
        return UrlManager.buildUrl(path)

    @staticmethod
    def getReleaseVersion():
        '''
        版本管理
        开发模式 使用时间作为我们的版本号
        生产环境 使用版本文件进行管理覆盖开发模式的值
        '''
        ver = getCurrentTime('%Y%m%d%H%M%S%f')
        release_path = app.config.get('RELEASE_PATH')
        if release_path and os.path.exists(release_path):
            with open(release_path, 'r') as f:
                ver = f.readline()
        return ver


