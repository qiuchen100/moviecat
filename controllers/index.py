"""
    created by 邱晨 on 2020/4/29 1:59 下午.
"""
from flask import Blueprint, request, redirect
from sqlalchemy.sql.expression import func
from common.libs.Helper import ops_render, iPagenation
from common.models.moive import Movie
from common.libs.UrlManager import UrlManager
from application import db


index_page = Blueprint('index_page', __name__)


@index_page.route('/')
def index():
    req = request.values
    page = int(req.get('p', 1))
    order_by = req.get('order', 'latest')
    total_count = Movie.query.count()
    page_params = {
        'page_size': 30,
        'total_count': total_count,
        'url': '/?',
        'page': page
    }
    pages = iPagenation(page_params)
    offset = (page - 1) * pages['page_size']
    limit = page * pages['page_size']
    order_by_f = Movie.pub_date.desc() if order_by == 'latest' else  Movie.view_counter.desc()
    movie_list = Movie.query.order_by(order_by_f, Movie.id.desc())[offset:limit]
    return ops_render('index.html', {"data": movie_list, "pages": pages})


@index_page.route('/info')
def info():
    req = request.values
    id = int(req.get('id', 0))
    info = Movie.query.filter_by(id=id).first()
    if not info:
        redirect(UrlManager.buildUrl('/'))

    '''
    更新阅读数量
    '''
    info.view_counter += 1
    db.session.add(info)
    db.session.commit()
    '''
    获取推荐
    '''
    recommend_list = Movie.query.order_by(func.rand()).limit(4)
    return ops_render('info.html', {'info': info, 'recommend_list': recommend_list})