# -*- coding: utf-8 -*-
import scrapy
import xlrd
#from copy import deepcopy
from ..items import BkzjItem
import re
import json
from copy import deepcopy
import logging

logger = logging.getLogger()


class BkzjSpider(scrapy.Spider):
    name = 'bkzj'
    allowed_domains = ['data.eastmoney.com/']


    def get_start_urls(self):
        
        wb = xlrd.open_workbook(r'D:\Github\CPdotgithub\Python\study code\A-python\历史数据\data\bkzj.xlsx')
        sheet = wb.sheets()[0]
        for i in range(1,sheet.nrows):
            data_row = sheet.row(i)
            bkname = data_row[0].value
            bkcode = data_row[1].value
            url = f'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=300&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid=f62&fs=b:{bkcode}&stat=1&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124'

            logger.info(url)
           
            yield scrapy.Request(url=url ,callback=self.parse_json,dont_filter=True,meta={'bkname':deepcopy(bkname),'bkcode':deepcopy(bkcode)})
    
    def parse_json(self, response):
        item = BkzjItem()
        logger.info(response.url,response.status,"\n"*4)
        bkname = response.meta['bkname']
        bkcode = response.meta['bkname']
        text = response.text
        jsondatas = re.search(r'"diff":(\[.*\])}}',text).group(1) 
        jsondatas = json.loads(jsondatas)
        for data in jsondatas:
            item["bkname"] = bkname
            item["bkcode"] = bkcode
            item['stockcode'] =  data["f12"]
            item['stockname'] = data["f14"]
            yield item

