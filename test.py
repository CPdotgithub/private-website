class A(object):
    def func(self,num):
        b = num**2
        return b
class B(A):
    def func2(self):
        print(self.func(10))

B().func2()






# import baostock as bs
# import pandas as pd
# ls = bs.login()
# rs = bs.query_history_k_data_plus(code,
#     "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
#     start_date='2017-07-01', end_date='2017-12-31',
#     frequency="d", adjustflag="3")
# data_list = []
# while (rs.error_code == '0') & rs.next() :
#     data={}
#     # 获取一条记录，将记录合并在一起
#     rowdata = rs.get_row_data()
#     data['date']=rowdata[0]
#     data['code']=rowdata[1]
#     data['open']=rowdata[2]
#     data['high']=rowdata[3]
#     data['low']=rowdata[4]
#     data['close']=rowdata[5]
#     data['preclose']=rowdata[6]
#     data['volume']=rowdata[7]
#     data['amount']=rowdata[8]
#     data['adjustflag']=rowdata[10]
#     data['tradestatus']=rowdata[11]
#     data['pctChg']=rowdata[12]
#     data['isST']=rowdata[13]
#     data_list.append(data)
# return data_list
# lo = bs.logout()

