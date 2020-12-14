# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from ..items import EastmoneyItem ,InstitutionJsondataItem,InstitutionDetailJsondataItem,InstitutionDailyJsondataItem
import time
import re
import json
import datetime
#from openpyxl  import load_workbook
#import pandas as pd
import xlrd
from copy import deepcopy




class HsgtInstitutionSpider(scrapy.Spider):

    name = 'hsgt_institution'
    allowed_domains = ['data.eastmoney.com/']
    start_urls = ['http://data.eastmoney.com/hsgtcg/InstitutionQueryMore.aspx']



    

    def parse(self, response):
        item = EastmoneyItem()
        lis = response.xpath('//*[@id="page"]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/div/ul')
        
        for li in lis.xpath('./li'):
            
            item['institution_bxcg_name'] = li.xpath('./a/@title').extract_first()
            url = li.xpath('./a/@href').extract_first()
            
            
            url_info = urljoin(base='http://data.eastmoney.com/',url=url)
            item['institution_bxcg_url'] = url_info
            
            jgcode = re.search('jgCode=(.*)&',url)
            item['institution_bxcg_code'] = jgcode.group(1)
            
            
            yield item
          
    
    
    
class InstitutionjsonSpider(scrapy.Spider):
    
    def get_start_urls(self):
        
        self.start_info = []
        info = {}
        wb = xlrd.open_workbook(r'C:\Users\Administrator\Documents\webspider\data\BXZJ\institution_info.xlsx')
        sheet = wb.sheets()[0]
        for i in range(1,sheet.nrows):
            info = deepcopy(info)
            data_row = sheet.row(i)
            info["jgcode"] = data_row[1].value
            info["url"] = data_row[2].value
            self.start_info.append(info) 
        return(self.start_info)
                
        

       
    name = 'InstitutionjsonSpider'
    allowed_domains = ['data.eastmoney.com/']
    

    def start_requests(self):
        start_info = self.get_start_urls()
        for info in start_info:
            jgcode = info["jgcode"]
            url = info["url"]
            yield scrapy.Request(url=url ,callback=self.parse_info ,dont_filter=True,meta = {"jgcode":deepcopy(jgcode),"url":deepcopy(url)})
   
    def parse_info(self,response):


        jgcode = response.meta["jgcode"]
        token_url = response.xpath('//*[@id="tab_cyszt"]/@data-url').extract_first()
        regx = re.search('token=(.*)&st',token_url)
        token = regx.group(1)
        institution_json_url=f'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTCOMSTA&token={token}&st=HDDATE&sr=-1&p=1&ps=50&js=var%20ajaxdata={{pages:(tp),data:(x)}}&filter=(PARTICIPANTCODE=%27{jgcode}%27)(MARKET=%27N%27)'
        


        
        yield scrapy.Request(url=institution_json_url,callback=self.parse_institution_json,meta={"jgcode":deepcopy(jgcode),"token":deepcopy(token)},dont_filter=True)  
        

    def parse_institution_json(self,response):
        
        item = InstitutionJsondataItem()
        
        text = response.text 

        info = re.search(r'(\[.*\])',text).group(1)  

        jsondatas = json.loads(info)
       

        for jsondata in jsondatas:

            item['institution_bxcg_date_jsondata']=jsondata["HDDATE"]
            item['institution_bxcg_name_jsondata']=jsondata["PARTICIPANTNAME"]
            item['institution_bxcg_code_jsondata']=jsondata["PARTICIPANTCODE"]
            
            
            item['institution_bxcg_num_jsondata']=jsondata["SHAREHOLDCOUNT"]
            item['institution_bxcg_value_jsondata']=jsondata["SHAREHOLDPRICE"]
            item['institution_bxcg_valuechg1_jsondata']=jsondata["SHAREHOLDPRICEONE"]
            
            item['institution_bxcg_valuechg5_jsondata']=jsondata["SHAREHOLDPRICEFIVE"]
            item['institution_bxcg_valuechg10_jsondata']=jsondata["SHAREHOLDPRICETEN"]
            yield item


"""
    机构持股明细

"""      
class InstitutionDetailjsonSpider(scrapy.Spider):

    name = 'InstitutionDetailjson'
    allowed_domains = ['data.eastmoney.com/']
    
    def get_start_urls(self):
        
        self.start_info = []
        info = {}
        wb = xlrd.open_workbook(r'C:\Users\Administrator\Documents\webspider\data\BXZJ\institution_info.xlsx')
        sheet = wb.sheets()[0]
        for i in range(1,sheet.nrows):
            info = deepcopy(info)
            data_row = sheet.row(i)
            info["jgcode"] = data_row[2].value
            date = data_row[0].value
            info["date"] = re.search(r'(.*)T.*',date).group(1)
            self.start_info.append(info) 
        return(self.start_info)
    
    def start_requests(self):
        start_info = self. get_start_urls()
        for info in start_info:
            date = info["date"]
            jgcode = info["jgcode"]
            url = f'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=1&ps=50&js=var%20ajaxdata={{pages:(tp),data:(x)}}&filter=(PARTICIPANTCODE=%27{jgcode}%27)(MARKET%20in%20(%27001%27,%27003%27))(HDDATE=^{date}^)&type=HSGTNHDDET'
            
            yield scrapy.Request(url=url ,callback=self.parse_detail_info ,dont_filter=True,meta = {
                #"jgcode":deepcopy(jgcode),
                #"date":deepcopy(date),
                "p":1
            })

    def parse_detail_info(self,response):
        item = InstitutionDetailJsondataItem()
        p = response.meta["p"]
        
        text = response.text 
        pages =  re.search(r'{pages:(\d.*),data:(\[.*\])}',text).group(1)
       
        if p <= int(pages):
            datas =  re.search(r'{pages:(\d.*),data:(\[.*\])}',text).group(2)

            jsondatas = json.loads(datas)

            for jsondata in jsondatas:

                """机构持股明细"""

                item['institution_bxcg_date_detail'] = jsondata["HDDATE"]
                item['company_stock_hkcode_detail'] = jsondata["HKCODE"]
                item['company_stock_code_detail'] = jsondata["SCODE"]
                item['company_stock_name_detail'] = jsondata["SNAME"]
                item['institution_bxcg_code_detail'] = jsondata["PARTICIPANTCODE"]
                item['institution_bxcg_name_detail'] = jsondata["PARTICIPANTNAME"]
                item['institution_bxcg_stock_num_detail'] = jsondata["SHAREHOLDSUM"]
                item['institution_bxcg_stock_ratio_detail'] = jsondata["SHARESRATE"]
                item['institution_bxcg_stock_value_detail'] = jsondata["SHAREHOLDPRICE"]
                item['institution_bxcg_valuechg1_detail'] = jsondata["SHAREHOLDPRICEONE"]
                item['institution_bxcg_valuechg5_detail'] = jsondata["SHAREHOLDPRICEFIVE"]
                item['institution_bxcg_valuechg10_detail'] = jsondata["SHAREHOLDPRICETEN"]
                yield item 
            p += 1
            next_page = re.sub(r'&p=\d*&',f'&p={p}&',response.url)
            scrapy.Request(url = next_page , callback=self.parse_detail_info,meta={"p":deepcopy(p)},dont_filter=True)



class InstitutionDailyjsonSpider(scrapy.Spider):
    
    name = 'InstitutionDailyjson'
    allowed_domains = ['data.eastmoney.com/']
    
    def get_start_urls(self):
        
        self.start_info = []
        
        wb = xlrd.open_workbook(r'C:\Users\Administrator\Documents\webspider\data\BXZJ\institution_info.xlsx')
        sheet = wb.sheets()[0]
        for i in range(1,sheet.nrows):
            data_row = sheet.row(i)
            jgcode = data_row[2].value
            self.start_info.append(jgcode) 
        return(self.start_info)
    
    def start_requests(self):
        start_info = self. get_start_urls()
        now = datetime.datetime.now()
        yesterday = (now+datetime.timedelta(-1)).strftime("%Y-%m-%d")
        # zeroyesterday = yesterday+"T00:00:00"
        for jgcode in start_info:
            date = yesterday
            
            url = f'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=1&ps=50&js=var%20ajaxdata={{pages:(tp),data:(x)}}&filter=(PARTICIPANTCODE=%27{jgcode}%27)(MARKET%20in%20(%27001%27,%27003%27))(HDDATE=^{date}^)&type=HSGTNHDDET'
            
            yield scrapy.Request(url=url ,callback=self.parse_detail_info ,dont_filter=True,meta = {
                #"jgcode":deepcopy(jgcode),
                #"date":deepcopy(date),
                "p":1
            })

    def parse_detail_info(self,response):
        item = InstitutionDailyJsondataItem()
        p = response.meta["p"]
        
        text = response.text 
        pages =  re.search(r'{pages:(\d.*),data:(\[.*\])}',text).group(1)
        
       
        if p <= int(pages):
            datas =  re.search(r'{pages:(\d.*),data:(\[.*\])}',text).group(2)

            jsondatas = json.loads(datas)

            for jsondata in jsondatas:

                """机构持股明细"""
                date = jsondata["HDDATE"]
                date = re.search(r'(.*)T.*',date).group(1)

                item['institution_bxcg_date_daily'] = date
                item['company_stock_hkcode_daily'] = jsondata["HKCODE"]
                item['company_stock_code_daily'] = jsondata["SCODE"]
                item['company_stock_name_daily'] = jsondata["SNAME"]
                item['institution_bxcg_code_daily'] = jsondata["PARTICIPANTCODE"]
                item['institution_bxcg_name_daily'] = jsondata["PARTICIPANTNAME"]
                item['institution_bxcg_stock_num_daily'] = jsondata["SHAREHOLDSUM"]
                item['institution_bxcg_stock_ratio_daily'] = jsondata["SHARESRATE"]
                item['institution_bxcg_stock_value_daily'] = jsondata["SHAREHOLDPRICE"]
                item['institution_bxcg_valuechg1_daily'] = jsondata["SHAREHOLDPRICEONE"]
                item['institution_bxcg_valuechg5_daily'] = jsondata["SHAREHOLDPRICEFIVE"]
                item['institution_bxcg_valuechg10_daily'] = jsondata["SHAREHOLDPRICETEN"]
                yield item 
            p += 1
            next_page = re.sub(r'&p=\d*&',f'&p={p}&',response.url)
            scrapy.Request(url = next_page , callback=self.parse_detail_info,meta={"p":deepcopy(p)},dont_filter=True)
            
           



      


       
    




            
          
        
        

             
        
 