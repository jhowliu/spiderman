# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from datetime import datetime
from template import SuperParser, punctuation_cleaner
from utils import find_by_css, split_address

class RTaiwanParser(SuperParser):

    def init(self):
        #self.navigations = self.__get_navigationbar()
        self.infos = self.__get_house_infos()

    def __is_key(self, key):
        if key not in self.infos:
            print('Cannot find the key: %s' % key)
            return False

        return True

    def __get_house_infos(self):
        infos = {}

        attr_raw = find_by_css(self.soup, 'td.td-center')
        value_raw = find_by_css(self.soup, 'td.td-white')

        for attr, value in zip(attr_raw, value_raw):
            if attr.text in infos: continue
            infos[attr.text] = value.text.strip()

        return infos


    def get_host_name(self):
        raw = find_by_css(self.soup, 'div.infoblock span')
        name = raw[0].text if raw else self.get_host_company()

        return name

    def get_host_phonenumber(self):
        raw = find_by_css(self.soup, 'div.infoblock h2')
        phone = raw[0].text if raw else ""

        return phone

    def get_host_role(self):
        role = u'屋主'
        company = self.get_host_company()
        if company != '': role = u'仲介'

        return role

    def get_host_company(self):
        raw = find_by_css(self.soup, 'div.infoblock h3')
        company = raw[0].text.strip() if raw else ""

        return company

    def get_price(self):
        key = u'租金'
        price = self.infos[key] if self.__is_key(key) else "0"
        price = punctuation_cleaner.sub('', price)

        price = re.search('\d+', price).group()

        return float(price), u'元/月'

    def get_price_per_pings(self):
        return 0, ''

    def get_separating_address(self, address):
        result = split_address(address)

        return result['city'], result['area'], result['road']

    def get_case_name(self):
        case_no = self.get_case_number()

        raw = find_by_css(self.soup, 'div.h1table h1')
        case_name = raw[0].text.replace(case_no, '') if raw else ''
        case_name = punctuation_cleaner.sub('', case_name)

        return case_name

    def get_case_number(self):
        raw = find_by_css(self.soup, 'div.h1table span.color-gray')
        case_number = punctuation_cleaner.sub('', raw[0].text) if raw else ''
        return case_number

    def get_address(self):
        key = u'地址'
        addr = self.infos[key] if self.__is_key(key) else ''

        return addr

    def get_building_pings(self):
        key = u'坪數'
        pings = self.infos[key] if self.__is_key(key) else ''

        return pings

    def get_house_usage(self):
        key = u'類型'
        usage = self.infos[key] if self.__is_key(key) else ''

        return usage

    def get_house_age(self):
        key = u'屋齡'
        age = self.infos[key] if self.__is_key(key) else ''

        return age

    def get_parking_space(self):
        key = u'車位'
        parking_space = self.infos[key] if self.__is_key(key) else u'無'

        return parking_space

    def get_short_rent(self):
        key = u'最短租期'
        shortest_rent = self.infos[key] if self.__is_key(key) else ''

        return shortest_rent

    def get_house_direction(self):
        key = u'座向朝向'
        direction = self.infos[key] if self.__is_key(key) else ''

        return direction

    def get_house_layout(self):
        key = u'格局'
        layout = self.infos[key].replace(' ','') if self.__is_key(key) else ''

        return layout

    def get_management_fee(self):
        key = u'管理費'
        fee = self.infos[key] if self.__is_key(key) else u'無'

        return fee

    # there might have a better solution
    def get_separating_layout(self):
        house_layout = self.get_house_layout()

        num_of_bath = num_of_living = num_of_room = num_of_balcony = 0

        if house_layout == "":
            return num_of_room, num_of_living, num_of_bath, num_of_balcony

        m = re.search(u'(\d+)房', house_layout)
        if m is not None:
            num_of_room = int(m.group(1))

        m = re.search(u'(\d+)廳', house_layout)
        if m is not None:
            num_of_living = int(m.group(1))

        m = re.search(u'(\d+)衛', house_layout)
        if m is not None:
            num_of_bath = int(m.group(1))

        m = re.search(u'(\d+)陽台', house_layout)
        if m is not None:
            num_of_balcony = int(m.group(1))

        return num_of_room, num_of_living, num_of_bath, num_of_balcony

    def get_latitude_longtitude(self):
        lat_lng_pattern = re.compile(r'q=(\d.*?),(\d.*?)&')
        m = lat_lng_pattern.search(self.html)

        lat = float(m.group(1)) if m else 0
        lng = float(m.group(2)) if m else 0

        return lat, lng


