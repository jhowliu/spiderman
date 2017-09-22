# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HouseInfos(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CaseNo  = scrapy.Field()
    CaseURL = scrapy.Field()
    CaseName = scrapy.field()
    Address = scrapy.field()
    City = scrapy.field()
    Zip = scrapy.field()
    Road = scrapy.field()
    Living = scrapy.field()
    Bed = scrapy.field()
    Bath = scrapy.field()
    Layout = scrapy.field()
    BuildingPing = scrapy.field()
    Latitude = scrapy.field()
    Longtitude = scrapy.field()
    Price = scrapy.field()
