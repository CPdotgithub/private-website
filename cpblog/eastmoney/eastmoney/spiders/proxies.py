# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import EastmoneyItem
import json
from copy import deepcopy



class ProxiesSpider(scrapy.Spider):
    name = 'proxies'
    allowed_domains = ['https://www.kuaidaili.com/free/']
    
    
    start_urls = ['https://www.kuaidaili.com/free/inha/%d/'%p for p in range(1,6)]

    def parse(self, response):
        test_url = "http://data.eastmoney.com/"
        trs = response.xpath('//*[@id="list"]/table/tbody/tr')
        for tr in trs:
            IP = tr.xpath('./td[1]/text()').extract_first()
            PORT = tr.xpath('./td[2]/text()').extract_first()
            httptype = tr.xpath('./td[4]/text()').extract_first()
            RTIME = tr.xpath('./td[6]/text()').extract_first()
            RTIME = re.sub(r'秒',"",RTIME)
            
            proxy = f"{httptype}://{IP}:{PORT}/"
            if float(RTIME) <2:
                yield scrapy.Request(url=test_url,meta={"proxy":deepcopy(proxy)},dont_filter=True)
            
               

    def verify_proxy(self,response):
        item = EastmoneyItem()
        
        proxy = response.meta["proxy"] 
        if response.status :
            item["proxies"] = proxy
            yield item

        
            
            
        
        
       

          
