import logging

from spiderman.orm.schema import *
from spiderman.orm.engine import sess
{
'Address': u'\u57fa\u9686\u5e02\u4e2d\u6b63\u5340\u65b0\u8c50\u8857',
'Bath': u'2.0',
'Bed': u'3',
'BuildingPing': u'39.32',
'CaseName': u'\u666e\u7f85\u65fa\u4e16\u6642\u5c1a\u5b85',
'CaseNo': u'TC01643443',
'CaseURL': 'http://www.twhg.com.tw/house_TC01643443.html',
'City': u'\u57fa\u9686\u5e02',
'Latitude': u'25.1377277',
'Layout': u'3\u623f2\u5ef32.0\u885b',
'Living': u'2',
'Longtitude': u'121.7855072',
'Price': u'698.0',
'Road': u'\u65b0\u8c50\u8857',
'Zip': u'\u4e2d\u6b63\u5340'
}

def insert_items(item):

    value = HouseInfo1(CaseName=item.CaseName,
                       CaseNo=item.CaseNo,
                       SimpAddress=item.Address,
                       CaseUrl=item.CaseUrl,
                       City=item.City,
                       Road=item.Road,
                       District=item.Zip,)

    logging.info("<INSERT> - %s" % item)
