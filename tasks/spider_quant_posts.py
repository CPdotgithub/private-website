import requests
import json
from cpblog.extensions import cache
from tasks import celery, MyTask



@celery.task()
@cache.memoize(60*60)
def get_quant_posts(page_num=1):
    url = f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num}'

    response = requests.get(url=url)
    response.encoding='utf-8'
    text = response.text
  
    jsondata = json.loads(text)
    last_url = f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num-1}'
    next_url= f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num+1}'
    posts = jsondata['topic_list']['topics']
    return posts




