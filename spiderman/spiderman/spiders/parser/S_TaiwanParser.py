# -*- coding:utf-8 -*-
import re
import time

from template import punctuation_cleaner, SuperParser
from utils import find_by_css

class STaiwanParser(SuperParser):

    def init(self):
        self.infos = self.__get_house_infos()

    def start_parse(self, infos):
        self.infos.update(infos)
        schema = self.fill_data_into_schema()

        return schema

    def __is_key(self, key):
        if key not in self.infos:
            #print('Cannot find the key: %s' % key)
            return False

        return True


    def __get_house_infos(self):
        infos = {}

        rows = find_by_css(self.soup, 'div.object-list li')

        for row in rows:
            clean_text = punctuation_cleaner.sub('', row.text)
            if ':' in clean_text:
                attr, value = clean_text.split(':')
                infos[attr] = value

        return infos


    def get_host_name(self):
        raw = find_by_css(self.soup, 'span.font_15_r')
        name = raw[0].text if raw else ''

        return name

    def get_host_phonenumber(self):
        raw = find_by_css(self.soup, 'span.font_13_666_tel')
        phone = raw[0].text if raw else ''

        return phone

    def get_host_role(self):
        return u'仲介'

    def get_host_company(self):
        raw = find_by_css(self.soup, 'span.font_15_r')
        company = raw[0].text if raw else ''

        return company

    def get_price(self):
        key = 'pay'
        price = self.infos[key] if self.__is_key(key) else "0"

        return float(price), u'萬/元'

    def get_price_per_pings(self):
        return 0, ''

    def get_separating_address(self, address):
        road = self.infos['add']
        city = self.infos['city']
        area = self.infos['area']

        return city, area, road

    def get_case_name(self):
        case_name = self.infos['tit'] if self.__is_key('tit') else ''
        return case_name

    def get_case_number(self):
        case_number = self.infos['no'] if self.__is_key('no') else ''
        return case_number

    def get_address(self):
        city, area, road = self.get_separating_address('')
        addr = city+area+road

        return addr

    def get_building_pings(self):
        pings = self.infos['pin'] if self.__is_key('pin') else ''

        return pings

    def get_floor_pings(self):
        landing = self.infos['landpin'] if self.__is_key('landpin') else ''

        return landing

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


    def get_house_direction(self):
        key = u'座向'
        direction = self.infos[key] if self.__is_key(key) else ''

        return direction

    def get_house_layout(self):
        room, living, bath, _ = self.get_separating_layout()
        layout = '%d房%d廳%d衛' % (room, living, bath)

        return layout

    def get_management_fee(self):
        key = u'管理費'
        fee = self.infos[key] if self.__is_key(key) else u'無'

        return fee

    # there might have a better solution
    def get_separating_layout(self):
        num_of_living = self.infos['liv'] if self.__is_key('liv') else 0
        num_of_room = self.infos['bed'] if self.__is_key('bed') else 0
        num_of_bath = self.infos['bat'] if self.__is_key('bed') else 0

        return int(float(num_of_room)), int(float(num_of_living)), int(float(num_of_bath)), 0

    def get_latitude_longtitude(self):
        lat = self.infos['x'] if self.__is_key('x') else 0.0
        lng = self.infos['y'] if self.__is_key('y') else 0.0

        return lat, lng
