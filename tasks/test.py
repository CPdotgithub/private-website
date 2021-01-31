from tasks import celery 
import time
@celery.task(name='tasks.add')
def add(a,b):
    time.sleep(1)
    return a+b