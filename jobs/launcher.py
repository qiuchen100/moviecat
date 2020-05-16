# -*- coding: utf-8 -*-#
import sys, argparse, traceback, importlib
from flask_script import Command


'''
Job 统一入口文件
python manager.py runjob -m Test (jobs/tasks/Test.py)
python manager.py runjob -m test/index (jobs/tasks/test/index)
'''


class RunJob(Command):

    capture_all_args = True

    def run(self, *args, **kwargs):
        args = sys.argv[2:]
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument('-m', '--name', dest='name', metavar='name', help='指定job名称', required=True)
        parser.add_argument('-a', '--act', dest='act', metavar='act', help='指定动作类型', required=False)
        parser.add_argument('-p', '--param', dest='param', metavar='param', nargs='*', help='业务参数', required=False)
        params = parser.parse_args(args)
        params_dict = params.__dict__

        if 'name' not in params_dict or not params_dict:
            return self.tips()
        try:
            '''
            from jobs.task.test import JobTask
            '''
            module_name = params_dict['name'].replace('/', '.')
            import_module = 'jobs.tasks.{}'.format(module_name)
            target = importlib.import_module(import_module)
            sys.exit(target.JobTask().run(params_dict))
        except Exception as e:
            traceback.print_exc()
        return

    def tips(self):
        tip_msg = '''
        请正确到调度Job
        python manager.py runjob -m Test (jobs/tasks/Test.py)
        python manager.py runjob -m test/index (jobs/tasks/test/index)
        '''
        return tip_msg