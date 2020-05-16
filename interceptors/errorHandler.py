"""
    created by 邱晨 on 2020/5/3 11:56 上午.
"""
from application import app


@app.errorhandler(404)
def error_404(e):
    return '404 not found'

