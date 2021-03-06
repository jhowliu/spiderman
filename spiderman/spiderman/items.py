# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HouseInfos(scrapy.Item):
    #ID = scrapy.Field()
    #DateTime = scrapy.Field()
    #CaseFrom = scrapy.Field()
    #CaseNo  = scrapy.Field()
    #CaseURL = scrapy.Field()
    #CaseName = scrapy.Field()
    #Address = scrapy.Field()
    #City = scrapy.Field()
    #Zip = scrapy.Field()
    #Road = scrapy.Field()
    #Living = scrapy.Field()
    #Bed = scrapy.Field()
    #Bath = scrapy.Field()
    #Layout = scrapy.Field()
    #BuildingPing = scrapy.Field()
    #LandPing = scrapy.Field()
    #Latitude = scrapy.Field()
    #Longtitude = scrapy.Field()
    #Price = scrapy.Field()
    #RorS = scrapy.Field()
    #Unit = scrapy.Field()
    #CaseType = scrapy.Field()
    #HouseAge = scrapy.Field()
    idx = scrapy.Field()
    KeyinDate = scrapy.Field()
    CaseFrom = scrapy.Field()
    CaseNo = scrapy.Field()
    CaseName = scrapy.Field()
    CaseUse = scrapy.Field()
    SimpAddress = scrapy.Field()
    City = scrapy.Field()
    District = scrapy.Field()
    Road = scrapy.Field()
    HouseLayout = scrapy.Field()
    Rm = scrapy.Field()
    LivingRm = scrapy.Field()
    BathRm = scrapy.Field()
    spaceRm = scrapy.Field()
    FloorSt = scrapy.Field()
    FloorEn = scrapy.Field()
    UpFloor = scrapy.Field()
    TotalPrice = scrapy.Field()
    OrigPrice = scrapy.Field()
    Unit = scrapy.Field()
    UnitPrice = scrapy.Field()
    UnitPriceUnit = scrapy.Field()
    BuildPin = scrapy.Field()
    LandPin = scrapy.Field()
    CasePic = scrapy.Field()
    CasePicUrl = scrapy.Field()
    CaseUrl = scrapy.Field()
    CaseSystem = scrapy.Field()
    RorS = scrapy.Field()
    ParkSpace = scrapy.Field()
    HouseAge = scrapy.Field()
    Lat = scrapy.Field()
    Lng = scrapy.Field()
    MainPin = scrapy.Field()
    BudName = scrapy.Field()
    ComUsePin = scrapy.Field()
    AttachedPin = scrapy.Field()

class RentInfos(scrapy.Item):
    idx = scrapy.Field()
    KeyinDate = scrapy.Field()
    ContactUser = scrapy.Field()
    ContactStore = scrapy.Field()
    ContactTel = scrapy.Field()
    ContactRole = scrapy.Field()
    ContactAddr = scrapy.Field()
    ContactEMail = scrapy.Field()
    CaseFrom = scrapy.Field()
    RorS = scrapy.Field()
    ManagementFee = scrapy.Field()
    ExpiryDate = scrapy.Field()
    Lease = scrapy.Field()
    Decorating = scrapy.Field()
    ShortRentDeadline = scrapy.Field()

class EnvironmentInfos(scrapy.Item):
    idx = scrapy.Field()
    KeyinDate = scrapy.Field()
    Direction = scrapy.Field()
    PrimarySchool = scrapy.Field()
    HighSchool = scrapy.Field()
    OthersPin = scrapy.Field()
    MrtLine = scrapy.Field()
    Characteristic = scrapy.Field()
    CaseFrom = scrapy.Field()
    RorS = scrapy.Field()
    TotalPin = scrapy.Field()
    Bus = scrapy.Field()
    PublicRatios = scrapy.Field()
    CMC = scrapy.Field()
    BudUrl = scrapy.Field()


