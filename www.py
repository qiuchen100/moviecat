"""
    created by 邱晨 on 2020/5/2 3:37 下午.
"""
from application import app

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

'''
    拦截器和错误处理器
'''
from interceptors.auth import *
from interceptors.errorHandler import *

'''
    蓝图
'''
from controllers.index import index_page
from controllers.member import member_page
app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(member_page, url_prefix='/member')

'''
    模板函数
'''
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
