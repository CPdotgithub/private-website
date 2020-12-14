import os
from cpblog import create_app
from celery import Celery
from cpblog.tasks import  log


def make_celery(app):
    celery = Celery(
        app.name,
        bocker = app.config['CELERY_BROKER_URL'],       
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)
   
    celery.Task = ContextTask
    return celery
flask_app = create_app('development')
celery = make_celery(flask_app)
