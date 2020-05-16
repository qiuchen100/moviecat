"""
    created by 邱晨 on 2020/4/29 1:59 下午.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os

# flask-sqlacodegen "mysql+pymysql://root:root@127.0.0.1:8889/movie_cat" --tables user --outfile "common/models/user.py"  --flask
app = Flask(__name__)
app.config.from_pyfile('config/base_setting.py')
if 'ops_config' in os.environ:
    app.config.from_pyfile('config/{0}_setting.py'.format(os.environ['ops_config']))

manager = Manager(app)

db = SQLAlchemy(app)







