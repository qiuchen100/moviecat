"""
    created by 邱晨 on 2020/5/2 3:37 下午.
"""
from www import *
from application import manager
from flask_script import Server, Command
import datetime
from jobs.launcher import RunJob

# web server
manager.add_command("runserver", Server(host='0.0.0.0', use_debugger=True, use_reloader=True))

# job

manager.add_command("runjob", RunJob)


# create table

@Command
def create_all():
    '''
        初始化数据库
    '''
    from application import db
    db.create_all()


manager.add_command("create_all", create_all)


def aps_test():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()

