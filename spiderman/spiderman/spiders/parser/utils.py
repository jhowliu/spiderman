# -*-coding:utf-8 -*-
import json
import re
import os

from city import CN_CITY_LIST

def find_by_class_name(soup, tag, class_name):
    raw = soup.find(tag, class_=class_name)

    if raw is None:
        print("there is no class name: %s" % class_name)
        return None

    return raw

def find_by_css(soup, css_pattern):
    raw = soup.select(css_pattern)

    if not len(raw):
        print("failed to find css pattern: %s" % css_pattern)
        return None

    return raw

def load_data():
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, 'data.json')) as fp:
        data = json.load(fp)

    area_list = [[area['AreaName'] for area in city['AreaList']] for city in data]
    city_list = [city['CityName'] for city in data]

    return city_list, area_list


CITY_LIST, AREA_LIST = load_data()

def split_address(address):
    target = {}

    for ix, city in enumerate(CITY_LIST):
        if city in address or CN_CITY_LIST[ix] in address:
            target['city'] = city
            address = address.replace(city, '').replace(CN_CITY_LIST[ix], '')
            for area in AREA_LIST[ix]:
                if area in address:
                    target['area'] = area
                    address = address.replace(area, '')
                    break
    target['road'] = address

    return target

