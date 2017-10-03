# -*- coding: utf-8 -*-
import re

from datetime import datetime
from template import SuperParser, punctuation_cleaner
from utils import find_by_css, find_by_class_name

class R591Parser(SuperParser):

    def init(self):
        self.navigations = self.__get_navigationbar()
        self.infos = self.__get_house_infos()

    def __is_key(self, key):
        if key not in self.infos:
            return False

        return True

    def __get_house_infos(self):
        infos = {}

        attr_raw = find_by_css(self.soup, '.labelList .one')
        value_raw = find_by_css(self.soup, '.labelList .two')

        for attr, value in zip(attr_raw, value_raw):
            infos[attr.text] = value.text.replace(u'：', '')


        rows = find_by_css(self.soup, 'ul.attr li')
        for row in rows:
            clean_text = punctuation_cleaner.sub('', row.text)
            attr, value = clean_text.split(':')
            infos[attr] = value

        return infos

    def __get_navigationbar(self):
        navigations = []
        # bs4 不能用css selector 找id
        raw = self.soup.find('div', { 'id': 'propNav'}).find_all('a')

        if len(raw) == 0:
            print("cannot find navigationbar by class name.")
            return navigations

        navigations = [nav.text for nav in raw]

        return navigations

    def get_host_name(self):
        raw = find_by_css(self.soup, 'div.avatarRight i')
        name = raw[0].text if raw else ""

        return name

    # need using OCR
    def get_host_phonenumber(self):
        pass

    def get_host_role(self):
        raw = find_by_css(self.soup, 'div.avatarRight')
        role = re.search(u'屋主|仲介|代理人', raw[0].text).group() if raw else ""

        return role

    def get_host_company(self):
        raw = find_by_css(self.soup, 'div.auatarSonBox')
        clean_text = punctuation_cleaner.sub('', raw[0].text) if raw else ''
        m = re.search(u'公司名：(\W+)分店：(\W+)', clean_text)

        company = m.group(1) if m else ""
        branch  = m.group(2) if m else ""

        return ' '.join([company, branch] )

    def get_price(self):
        raw = find_by_css(self.soup, 'div.price')
        price = re.search('\d+', punctuation_cleaner.sub('', raw[0].text)) \
                  .group() if raw else 0.0

        raw = find_by_css(self.soup, 'div.price b')
        unit = raw[0].text if raw else u"元/月"

        return float(price), unit

    def get_price_per_pings(self):
        return 0, ''

    def get_separating_address(self, address):
        city = district = road = ''

        if len(self.navigations) == 0:
            print('navigation list is empty')
            return city, district, road

        city = self.navigations[2]
        district = self.navigations[3]
        road = address.replace(city, '').replace(district, '')

        return city, district, road

    def get_case_name(self):
        raw = find_by_css(self.soup, 'span.houseInfoTitle')
        return raw[0].text if raw else ""

    def get_case_number(self):
        m = re.search('(\d+.).html$', self.url)
        case_number = 'R'+m.group(1) if m else ''

        return case_number

    def get_address(self):
        raw = find_by_css(self.soup, 'span.addr')
        addr = raw[0].text if raw else ''

        return addr

    def get_building_pings(self):
        key = u'坪數'
        pings = self.infos[key] if self.__is_key(key) else ''

        return pings

    def get_house_usage(self):
        key = u'型態'
        usage = self.infos[key] if self.__is_key(key) else ''

        return usage

    def get_parking_space(self):
        key = u'車位'
        parking_space = self.infos[key] if self.__is_key(key) else u'無'

        return parking_space

    def get_short_rent(self):
        key = u'最短租期'
        shortest_rent = self.infos[key] if self.__is_key(key) else ''

        return shortest_rent

    def get_house_direction(self):
        key = u'朝向'
        direction = self.infos[key] if self.__is_key(key) else ''

        return direction

    def get_house_layout(self):
        key = u'格局'
        layout = self.infos[key] if self.__is_key(key) else ''

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

    def get_expire_date(self):
        raw = find_by_css(self.soup, 'span.ft-rt')
        expire_date = raw[0].text.replace(u'有效期：', '')

        return expire_date

