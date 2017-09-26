# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HouseInfos(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    DateTime = scrapy.Field()
    CaseFrom = scrapy.Field()
    CaseNo  = scrapy.Field()
    CaseURL = scrapy.Field()
    CaseName = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    Zip = scrapy.Field()
    Road = scrapy.Field()
    Living = scrapy.Field()
    Bed = scrapy.Field()
    Bath = scrapy.Field()
    Layout = scrapy.Field()
    BuildingPing = scrapy.Field()
    LandPing = scrapy.Field()
    Latitude = scrapy.Field()
    Longtitude = scrapy.Field()
    Price = scrapy.Field()
    RorS = scrapy.Field()
    Unit = scrapy.Field()
    CaseType = scrapy.Field()
    HouseAge = scrapy.Field()
