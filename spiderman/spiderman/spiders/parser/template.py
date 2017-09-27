# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from lib.wrapper import get_table_schema

import re
import time

# only keep chinese words
clean = re.compile(r'[\u064B-\u0652\u06D4\u0670\u0674\u06D5-\u06ED| ]+')

# punctuation filter
punctuation_cleaner = re.compile(r'[,，【】（）()\n\xa0 ]')

class SuperParser(object):
    def __init__(self, content_html=None, url=None, rent_or_sale=None):
        self.url = url
        self.html = content_html
        self.date = time.strftime("%Y-%m-%d")
        self.time = time.strftime("%H:%M:%S")
        self.init()

    def start_parse(self):
        pass
    def init(self):
        pass

    def get_host_name(self):
        pass
    def get_host_phonenumber(self):
        pass
    def get_host_role(self):
        pass
    def get_host_mail(self):
        mail_pattern = re.compile(r'([\w.]+@[\w]+\.[a-zA-Z]{2,4}\.?[a-zA-Z]{0,4})')
        pass
    def get_host_company(self):
        pass
    def get_community(self):
        pass
    def get_price(self):
        pass
    def get_price_per_pings(self):
        pass
    def get_separating_address(self, address):
        pass
    def get_case_name(self):
        pass
    def get_case_number(self):
        pass
    def get_address(self):
        pass
    def get_parking_space(self):
        pass
    # 建坪
    def get_building_pings(self):
        pass
    # 地坪
    def get_floor_pings(self):
        pass
    # 主建物坪數
    def get_main_building_pings(self):
        pass
    # 附屬建物坪數
    def get_attached_building_pings(self):
        pass
    # 公設
    def get_public_utilities_pings(self):
        pass
    # 公設比
    def get_public_utilities_ratio(self):
        pass
    def get_house_age(self):
        pass
    def get_house_usage(self):
        pass
    def get_house_type(self):
        pass
    def get_decorating_level(self):
        pass
    def get_lease_state(self):
        pass
    def get_house_direction(self):
        pass
    def get_house_layout(self):
        pass
    # there might have a better solution
    def get_separating_layout(self):
        pass
    def get_latitude_longtitude(self):
        pass

    def fill_data_into_schema(self):
        city, district, road = self.get_separating_address(self.get_address())
        num_of_room, num_of_living, num_of_bath, num_of_balcony = self.get_separating_layout()
        price, unit = self.get_price()
        price_per_pings, unit_per_pings = self.get_price_per_pings()
        lat, lng = self.get_latitude_longtitude()

        schema = get_table_schema()

        # WebHouseCase 物件資訊
        house_info_key_list = [
            'idx', 'CaseFrom', 'CaseNo',
            'CaseName', 'CaseUse', 'SimpAddress',
            'City', 'District', 'Road',
            'HouseLayout', 'Rm', 'LivingRm',
            'BathRm', 'spaceRm', 'TotalPrice',
            'OrigPrice', 'Unit', 'UnitPrice',
            'UnitPriceUnit', 'BuildPin', 'LandPin',
            'CaseUrl', 'RorS', 'HouseAge',
            'Lat', 'Lng', 'MainPin',
            'ComUsePin', 'AttachedPin', 'ParkSpace'
        ]

        house_info_value_list = [
            self.id_, self.casefrom, self.get_case_number(),
            self.get_case_name(), self.get_house_usage(), self.get_address(),
            city, district, road,
            self.get_house_layout(), num_of_room, num_of_living,
            num_of_bath, num_of_balcony, price,
            price, unit, price_per_pings,
            unit_per_pings, self.get_building_pings(), self.get_floor_pings(),
            self.url, self.rent_or_sale, self.get_house_age(),
            lat, lng, self.get_main_building_pings(),
            self.get_public_utilities_pings(), self.get_attached_building_pings(), self.get_parking_space()
        ]


        # WebHouseCasePart2 屋主資訊
        host_info_key_list = [
            'idx', 'ContactUser', 'ContactStore',
            'ContactTel', 'ContactRole', 'ContactEMail',
            'CaseFrom', 'RorS', 'Lease',
            'Decorating'
        ]

        host_info_value_list = [
            self.id_, self.get_host_name(), self.get_host_company(),
            self.get_host_phonenumber(), self.get_host_role(), self.get_host_mail(),
            self.casefrom, self.rent_or_sale, self.get_lease_state(),
            self.get_decorating_level()
        ]

        # WebHouseCasePart3
        house_pros_key_list = [
            'idx', 'Direction', 'CaseFrom',
            'TotalPin', 'RorS', 'PublicRatios',
            'CMC'
        ]

        house_pros_value_list = [
            self.id_, self.get_house_direction(), self.casefrom,
            self.get_building_pings(), self.rent_or_sale, self.get_public_utilities_ratio(),
            self.get_public_utilities_ratio()
        ]

        for (key, value) in zip(house_info_key_list, house_info_value_list):
            schema['WebHouseCase'][key] = value

        for (key, value) in zip(host_info_key_list, host_info_value_list):
            schema['WebHouseCasePart2'][key] = value

        for (key, value) in zip(house_pros_key_list, house_pros_value_list):
            schema['WebHouseCasePart3'][key] = value

        return schema
