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


@celery.task(name='task.stock_daily_data',bind=True,ignore_result=True,default_retry_delay=300,max_retries=5)
def stock_daily_data(date):
        bs.login()
        # 获取交易日 日历
        rs_date = bs.query_trade_dates(start_date='2020-01-01')
        date_list = []
        while (rs_date.error_code == '0') & rs_date.next():
            date_list.append(rs_date.get_row_data())
        df_date = pd.DataFrame(date_list,columns=rs_date.fields)

        exchg_date = df_date[df_date["is_trading_day"]=='1']
        date_list= exchg_date["calendar_date"].to_list()
      
