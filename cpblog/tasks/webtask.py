from cpblog.extensions import celery
import requests 
import json
import random
from cpblog.StockModels.financialmodel import StockDaily


@celery.task()
def log(msg):
    return msg

@celery.task()
def dailyprice(em,stock_id):
    if em == "sz":
        random_time = random.random()
        url = f"http://www.szse.cn/api/market/ssjjhq/getTimeData?random={random_time}&marketId=1&code={stock_id}"
        headers = {
            "Referer": f"http://www.szse.cn/market/trend/index.html?code={stock_id}"
        }
        response = requests.get(url=url,headers=headers)
        jsondata = json.loads(response.content)
        # data = jsondata['data']
        # code = data['code']
        # name = data['name']
        # close = data['close']
        # open = data['open']
        # now  = data['now']
        # high  = data['high']
        # low    = data['low']
        # volume = data['volume']
        # marketTime  = data['marketTime']
        # buy5 = data['sellbuy5'][1]
        # buy5 = data['sellbuy5'][1]
        # buy5 = data['sellbuy5'][1]
        # buy5 = data['sellbuy5'][1]
        return jsondata
@celery.task()
def get_history_k_data(code,start_date,end_date,frequency,adjustflag):
    import baostock as bs
    bs.login()
    rs = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date=start_date, end_date=end_date,frequency=frequency,adjustflag=adjustflag)
    data_list = []
    while (rs.error_code == '0') & rs.next() :
        data={}
        # 获取一条记录，将记录合并在一起
        rowdata = rs.get_row_data()
        data['date']=rowdata[0]
        data['code']=rowdata[1]
        data['open']=rowdata[2]
        data['high']=rowdata[3]
        data['low']=rowdata[4]
        data['close']=rowdata[5]
        data['preclose']=rowdata[6]
        data['volume']=rowdata[7]
        data['amount']=rowdata[8]
        data['adjustflag']=rowdata[10]
        data['tradestatus']=rowdata[11]
        data['pctChg']=rowdata[12]
        data['isST']=rowdata[13]
        data_list.append(data)
    return data_list
    bs.logout()
    

    