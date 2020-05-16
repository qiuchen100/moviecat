"""
    created by 邱晨 on 2020/5/3 11:49 上午.
"""
from flask import request, g
from application import app
from common.models.user import User
from common.libs.UserService import UserService


@app.before_request
def before_request():
    app.logger.info('----------before request-----------')
    user_info = check_login()
    g.current_user = user_info
    return


@app.after_request
def after_request(response):
    app.logger.info('----------after request-----------')
    return response


def check_login():
    """
    判断用户是否登录
    """
    cookies = request.cookies
    cookie_name = app.config['AUTH_COOKIE_NAME']
    auth_cookie = cookies.get(cookie_name)
    if auth_cookie is None:
        return
    auth_info = auth_cookie.split('#')
    if len(auth_info) != 2:
        return
    try:
        user_info = User.query.filter_by(id=auth_info[1]).one_or_none()
        if user_info is None:
            return
        if auth_info[0] != UserService.geneAuth(user_info):
            return
        return user_info
    except Exception:
        return