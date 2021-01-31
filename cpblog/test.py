import pymysql
import redis
import os
from celery import Celery
import requests,json
import time
import baostock as bs
import pandas as pd
from cpblog.extensions import db
from cpblog.models import QuantPost

def get_quant_posts():
    for page_num in range(10):

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
get_quant_posts()
    