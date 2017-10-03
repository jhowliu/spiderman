# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from datetime import datetime
from template import SuperParser, punctuation_cleaner
from utils import find_by_css, split_address

class RSinYiParser(SuperParser):

    def init(self):
        self.infos = self.__get_house_infos()

    def __is_key(self, key):
        if key not in self.infos:
            return False

        return True

    def __get_house_infos(self):
        infos = {}

        attr_raw = find_by_css(self.soup, '#mainInfo th')
        value_raw = find_by_css(self.soup, '#mainInfo td')

        for attr, value in zip(attr_raw, value_raw):
            key = attr.text.replace(u'\u3000', '')

            if key in infos: continue
            infos[key] = value.text.strip()

        return infos


    def get_host_name(self):
        raw = find_by_css(self.soup, 'div.landlord')
        name = raw[0].text if raw else ''

        return name

    def get_host_phonenumber(self):
        phone = ''
        raws = find_by_css(self.soup, '.tel span')
        for raw in raws:
            text = raw['class'][0]
            m = re.search('\d', text)
            phone += m.group() if m else ''

        return phone

    def get_host_role(self):
        raw = find_by_css(self.soup, '.status')
        role = raw[0].text if raw else ''

        role = u'屋主' if u'房東' in role else '仲介'

        return role

    def get_host_company(self):
        company = ''
        if self.get_host_role() == u'仲介':
            raw = find_by_css('#sideMenu section li span')
            company = ' '.join([self.get_host_name, raw[-1].text])

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
        raw = find_by_css(self.soup, 'div.top h1')
        case_name = raw[0].text if raw else ''
        case_name = punctuation_cleaner.sub('', case_name)

        return case_name

    def get_case_number(self):
        m = re.search('itemid=([a-zA-Z0-9]+)', self.url)
        case_number = m.group(1) if m else ''

        return case_number

    def get_address(self):
        key = u'地址'
        addr = self.infos[key] if self.__is_key(key) else ''

        return addr

    def get_building_pings(self):
        key = u'建物坪數'
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
        short_rent = self.infos[key] if self.__is_key(key) else ''

        return short_rent

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

        m = re.search(u'(\d+)室', house_layout)
        if m is not None:
            num_of_balcony = int(m.group(1))

        return num_of_room, num_of_living, num_of_bath, num_of_balcony

    def get_latitude_longtitude(self):
        raw = find_by_css(self.soup, '#static_map2')
        text = raw[0]['src']

        lat_lng_pattern = re.compile(r'(\d+\.\d+)_(\d+\.\d+).png')
        m = lat_lng_pattern.search(text)

        lat = float(m.group(1)) if m else 0.
        lng = float(m.group(2)) if m else 0.

        return lat, lng


