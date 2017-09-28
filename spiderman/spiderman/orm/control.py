import logging

from spiderman.orm.schema import *
from spiderman.orm.engine import sess
from spiderman.orm.util import is_exist

def insert_items(item):

    logging.info("<INSERT> - %s" % item['idx'])
    '''
    value = HouseInfo1(idx=item['ID'],
                       RorS=item['RorS'],
                       KeyinDate=item['DateTime'],
                       CaseName=item['CaseName'],
                       CaseNo=item['CaseNo'],
                       CaseFrom=item['CaseFrom'],
                       CaseUse=item['CaseType'],
                       SimpAddress=item['Address'],
                       CaseUrl=item['CaseURL'],
                       City=item['City'],
                       Road=item['Road'],
                       District=item['Zip'],
                       HouseLayout=item['Layout'],
                       Rm=item['Bed'],dd
                       LivingRm=item['Living'],
                       BathRm=item['Bath'],
                       TotalPrice=item['Price'],
                       OrigPrice=item['Price'],
                       Unit=item['Unit'],
                       BuildPin=item['BuildingPing'],
                       LandPin=item['LandPing'],
                       Lat=item['Latitude'],
                       Lng=item['Longtitude'],
                       HouseAge=item['HouseAge'])
    '''

    value = HouseInfos(**item)

    #row = is_exist(HouseInfo1, item['ID'])
    row = sess.query(HouseInfos).filter_by(idx=item['idx']).first()

    if (not row):
        sess.add(value)
        sess.commit()
