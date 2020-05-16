"""
    created by 邱晨 on 2020/5/3 6:35 下午.
"""
from flask import Blueprint, render_template, request, make_response, redirect
from common.libs.Helper import ops_renderJSON, ops_renderErrJSON
from common.models.user import User
from common.libs.UserService import UserService
from common.libs.DateHelper import getCurrentTime
from common.libs.UrlManager import UrlManager
from application import db, app


member_page = Blueprint('member_page', __name__)


@member_page.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('member/reg.html')

    req = request.values
    loginName = req.get('loginName', '')
    loginPwd = req.get('loginPwd', '')
    loginPwd2 = req.get('loginPwd2', '')
    if len(loginName) < 1:
        return ops_renderErrJSON('用户名不能为空！')
    if len(loginPwd) < 6:
        return ops_renderErrJSON('密码不能为空且长度不能小于6！')
    if loginPwd != loginPwd2:
        return ops_renderErrJSON('两次输入的密码不相等！')

    user_info = User.query.filter_by(login_name=loginName).one_or_none()
    if user_info is not None:
        return ops_renderErrJSON('该用户名已被注册！')
    model_user = User()
    model_user.login_name = loginName
    model_user.login_salt = UserService.geneSalt(8)
    model_user.login_pwd = UserService.genePwd(loginPwd, model_user.login_salt)
    model_user.created_time = model_user.updated_time = getCurrentTime()
    db.session.add(model_user)
    db.session.commit()
    return ops_renderJSON(msg='注册成功！')


@member_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('member/login.html')

    req = request.values
    loginName = req.get('loginName', '')
    loginPwd = req.get('loginPwd', '')
    if len(loginName) < 1:
        return ops_renderErrJSON('用户名不能为空！')
    if len(loginPwd) < 6:
        return ops_renderErrJSON('密码不能为空且长度不能小于6！')
    user_info = User.query.filter_by(login_name=loginName).one_or_none()
    if user_info is None:
        return ops_renderErrJSON('该用户名不存在！')
    salt_pwd = UserService.genePwd(loginPwd, user_info.login_salt)
    if salt_pwd != user_info.login_pwd:
        return ops_renderErrJSON('用户密码错误！')
    if user_info.status == 0:
        return ops_renderErrJSON('该用户已被禁用！')
    # session['uid'] = user_info.id
    response = make_response(ops_renderJSON(msg='登录成功！'))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],
                        '{}#{}'.format(UserService.geneAuth(user_info), user_info.id),
                        60 * 60 * 24 * 7)
    return response


@member_page.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response