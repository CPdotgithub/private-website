# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EastmoneyItem(scrapy.Item):

    proxies = scrapy.Field()
 
    
    
    
  

    """
    外资机构
    """ 
    institution_bxcg_name=scrapy.Field()
    institution_bxcg_code=scrapy.Field()
    institution_bxcg_url=scrapy.Field()


class InstitutionJsondataItem(scrapy.Item):

    institution_bxcg_name_jsondata=scrapy.Field()
    institution_bxcg_code_jsondata=scrapy.Field()
    institution_bxcg_url_jsondata =scrapy.Field() 
    institution_bxcg_date_jsondata = scrapy.Field()
    institution_bxcg_num_jsondata = scrapy.Field()
    institution_bxcg_value_jsondata = scrapy.Field()
    institution_bxcg_valuechg1_jsondata = scrapy.Field()
    institution_bxcg_valuechg5_jsondata = scrapy.Field()
    institution_bxcg_valuechg10_jsondata = scrapy.Field()

class InstitutionDetailJsondataItem(scrapy.Item):
    
    institutiondetaildata = scrapy.Field()

    institution_bxcg_date_detail = scrapy.Field()
    company_stock_hkcode_detail=scrapy.Field()
    company_stock_code_detail=scrapy.Field()
    company_stock_name_detail=scrapy.Field()
    
    institution_bxcg_code_detail =scrapy.Field()
    institution_bxcg_name_detail =scrapy.Field()
    institution_bxcg_stock_num_detail = scrapy.Field()
    institution_bxcg_stock_ratio_detail = scrapy.Field()

    institution_bxcg_stock_value_detail = scrapy.Field()
    institution_bxcg_valuechg1_detail = scrapy.Field()
    institution_bxcg_valuechg5_detail = scrapy.Field()
    institution_bxcg_valuechg10_detail = scrapy.Field()

    



class InstitutionDailyJsondataItem(scrapy.Item):
    
    institutiondetaildata = scrapy.Field()

    institution_bxcg_date_daily = scrapy.Field()
    company_stock_hkcode_daily=scrapy.Field()
    company_stock_code_daily=scrapy.Field()
    company_stock_name_daily=scrapy.Field()
    
    institution_bxcg_code_daily =scrapy.Field()
    institution_bxcg_name_daily =scrapy.Field()
    institution_bxcg_stock_num_daily = scrapy.Field()
    institution_bxcg_stock_ratio_daily = scrapy.Field()

    institution_bxcg_stock_value_daily = scrapy.Field()
    institution_bxcg_valuechg1_daily = scrapy.Field()
    institution_bxcg_valuechg5_daily = scrapy.Field()
    institution_bxcg_valuechg10_daily = scrapy.Field()


class BkzjItem(scrapy.Item):

    bkname = scrapy.Field()
    bkcode = scrapy.Field()
    stockname = scrapy.Field()
    stockcode = scrapy.Field()




    