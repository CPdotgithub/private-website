import os
from celery import Celery

CELERY_BROKER_URL = 'redis://:'+os.getenv('redis_password')+'@127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://:'+os.getenv('redis_password')+'@127.0.0.1:6379/1'

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


class MyTask(celery.Task): # celery 基类

    def on_success(self, retval, task_id, args, kwargs):
        # 执行成功的操作
        print('MyTasks 基类回调，任务执行成功')
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 执行失败的操作
        # 任务执行失败，可以调用接口进行失败报警等操作
        print('MyTasks 基类回调，任务执行失败')
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)