import os
from flask import render_template, flash, redirect, url_for, current_app,request, abort, Blueprint,make_response,g

from flask_login import login_required, current_user
from cpblog.decorators import confirm_required, permission_required
from cpblog.extensions import db,cache,celery
from cpblog.models import Admin,Account,Order,LoanOrder, IndustryInfo,StockInfo,InstitutionInfo,InstitutionStockDaily,StockDaily,QuantPost
from cpblog.emails import send_new_order_email,send_week_report_email
from datetime import datetime
from cpblog.tasks import get_quant_posts
from celery import Celery
import requests ,json,time
from pyecharts import options as opts
from pyecharts.charts import Kline
import pandas as pd
import tushare as ts

stock_bp = Blueprint('stock', __name__)

def kline_base(code) -> Kline:
    pro = ts.pro_api('d51f868eec8a150f0f399be85c66d5882a6dbaa25aed81c6abe9f6fb')

    df = pro.daily(ts_code=code, start_date='20200101')
    df.index=pd.to_datetime(df.trade_date)
    df=df.sort_index()
    v1=list(df.loc[:,['open','close','low','high']].values.tolist())
    t=df.index
    v0=list(t.strftime('%Y%m%d'))


    c = (
        Kline()
        .add_xaxis(v0)
        .add_yaxis("kline", v1)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],

        )
        
    )
    return c






@stock_bp.route('/')
def index():
    
    return render_template('stock/index.html')



@stock_bp.route("/kline/<string:code>")
def kline(code):
  
    c = kline_base(code)
    return c.dump_options_with_quotes()

@stock_bp.route('/stockinfo/<string:code>')
def game(code):   
    
    return render_template('stock/report.html',code=code)


@cache.cached(60*60)
@stock_bp.route('/quant_posts')
@stock_bp.route('/quant_posts/<int:page_num>' ,methods=['GET', 'POST'])
def quant_posts(page_num=1):
    if request.method == 'GET':
        url = f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num}'

        response = requests.get(url=url)
        response.encoding='utf-8'
        text = response.text
    
        jsondata = json.loads(text)
        last_url = f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num-1}'
        next_url= f'https://bigquant.com/community/c/research/l/latest.json?no_subcategories=false&page={page_num+1}'
        quantposts = jsondata['topic_list']['topics']
        g.quantposts = quantposts
    
    #return render_template('stock/test.html',text=posts)

    return render_template('stock/quantposts.html',quantposts=quantposts)




# @login_required
# @stock_bp.route('/collected_posts',methods=['GET', 'POST'])
# def collected_posts():
#     quantposts = QuantPost.query.filter_by(user_id=current_user.id).all()
#     return render_template('stock/collectposts.html',quantposts=quantposts)


@stock_bp.route('/read_post/<int:post_id>',methods=['GET', 'POST'])
def read_post(post_id):
    url = f'https://bigquant.com/community/t/topic/{post_id}'
    return redirect(location=url)

# @login_required
# @stock_bp.route('/delete_post/<int:post_id>',methods=['GET', 'POST'])
# def delete_post(post_id):
   
#     post = QuantPost.query.filter_by(post_id=post_id,user_id=current_user.id).delete()
#     db.session.commit()


# @cache.cached()
# @stock_bp.route('/choose_stock',methods=['GET', 'POST'])

# def choose_stock(page_num=1):
    
#     return render_template('stock/quantposts.html')