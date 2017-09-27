# -*- coding=utf-8 -*-
import re
import time
import hashlib

CASEFROM = "Taiwan"
def Parse(response):
    global CASEFROM

    case_type = ""
    house_age = ""

    for list_ in response.css('div.object-list li'):
        text = (''.join(list_.css('::text').extract()).strip())

        if u'類型 :' in text:
            case_type = text.replace(u'類型 :', '').strip()
        if u'屋齡 :' in text:
            house_age = text.replace(u'屋齡 :', '').strip()

    infos = response.meta['infos']

    date = time.strftime("%Y-%m-%d")
    case_name = infos['tit']
    case_no = infos['no']

    id_ = hashlib.sha1("%s-%s-%s" % (CASEFROM, case_no, date)).hexdigest()

    price = infos['pay']
    road = infos['add']
    city = infos['city']
    district = infos['area']
    addr = city+district+road

    building_pings = infos['pin']
    landing_pings = infos['landpin']

    num_of_living = infos['liv']
    num_of_bed = infos['bed']
    num_of_bath = infos['bat']

    layout = u'%s房%s廳%s衛' % (num_of_bed, num_of_living, num_of_bath)

    lat = infos['x']
    lng = infos['y']

    url = response.url

    items = {
        'ID': id_,
        'DateTime': date,
        'CaseNo': case_no,
        'CaseURL': url,
        'CaseFrom': CASEFROM,
        'CaseName': case_name,
        'CaseType': case_type,
        'HouseAge': house_age,
        'Address': addr,
        'City': city,
        'Zip': district,
        'Road': road,
        'Living': num_of_living,
        'Bed': num_of_bed,
        'Bath': num_of_bath,
        'Layout': layout,
        'BuildingPing': building_pings,
        'LandPing': landing_pings,
        'Latitude': lat,
        'Longtitude': lng,
        'Price': price,
        'Unit': u'萬/元',
        'RorS': u'出售',
    }

    return items

def taiwan_rent(infos):
    pass
