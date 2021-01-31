import os
from celery import Celery
import requests,json
import time
import baostock as bs
import pandas as pd
from cpblog.extensions import db
from cpblog.models import QuantPost



CELERY_BROKER_URL = 'redis://:'+os.getenv('redis_password')+'@127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://:'+os.getenv('redis_password')+'@127.0.0.1:6379/1'

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.add')
def add(a,b):
    time.sleep(1)
    return a+b


@celery.task(name='tasks.get_quant_posts')

def get_quant_posts():
    for page_num in range(3):

        url = f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num}'

        response = requests.get(url=url)
        response.encoding='utf-8'
        text = response.text  
        jsondata = json.loads(text)
        posts = jsondata['topic_list']['topics']
        for post in posts:
            post_id = post['post_id']
            title = post['title']
            excerpt = post['excerpt']
            post = QuantPost(post_id=post_id,title=title,excerpt=excerpt)
            db.session.add(post)
    db.session.commit()



