# -*- coding: utf-8 -*-
import re
import time

from template import SuperParser
from template import punctuation_cleaner, clean

class S591Parser(SuperParser):

    def init(self):
        self.infos = self.__get_house_infos()
        self.navigations = self.__get_navigationbar()

    def __find_by_class_name(self, tag, class_name):
        raw = self.soup.find(tag, class_=class_name)

        if raw is None:
            print("there is no class name: %s" % class_name)
            return None

        return raw

    def __is_key(self, key):

        if key not in self.infos:
            print("cannot find the key: %s" % key)
            return False

        return True

    # use for floating number
    def __extract_floating_number(self, text):
        target = 0.0
        m = re.search(r'(\d+.\d+)', text)

        try:
            target = float(m.group(1))
        except Exception as e:
            print(e)
            target = 0.0

        return target

    def __get_house_infos(self):
        infos = {}
        # 591 designer is funny
        key_list = ['info-addr-key', 'info-floor-value', 'detail-house-key']
        value_list = ['info-addr-value', 'info-floor-key', 'detail-house-value']
        tag_list = ['span', 'div', 'div']

        attributes = []
        values = []

        for key, value, tag in zip(key_list, value_list, tag_list):
            attributes.extend([raw.text for raw in self.soup.find_all(tag, class_=key)])
            values.extend([raw.text for raw in self.soup.find_all(tag, class_=value)])
        for (key, value) in zip(attributes, values):
            infos[key] = value

        return infos

    def __get_house_nearby_infos(self):
        pass

    def __get_navigationbar(self):
        navigations = []
        raw = self.soup.find('div', class_='breadList').find_all('a')

        if raw is None:
            print("cannot find navigationbar by class name.")
            return navigations

        navigations = [nav.text for nav in raw]

        return navigations


    def get_host_name(self):
        raw = self.__find_by_class_name('span', 'info-span-name')
        host_name = raw.text if raw is not None else ""

        return host_name

    def get_host_phonenumber(self):
        raw = self.__find_by_class_name('span', 'info-host-word')
        phonenumber = raw.text if raw is not None else ""

        return phonenumber

    def get_host_role(self):
        raw = self.__find_by_class_name('span', 'info-span-msg')

        host_role = raw.text if raw is not None else ""
        host_role = punctuation_cleaner.sub('', host_role)

        return host_role

    def get_host_mail(self):
        mail_pattern = re.compile(r'([\w.]+@[\w]+\.[a-zA-Z]{2,4}\.?[a-zA-Z]{0,4})')
        raw = self.__find_by_class_name('div', 'info-host-three')

        m = mail_pattern.search(raw.text) if raw is not None else ""

        try:
            mail = m.group(1)
        except Exception as e:
            print(e)
            mail = ""

        return mail

    def get_host_company(self):
        host_store = ""
        raw = self.__find_by_class_name('div', 'info-detail-show')

        text = clean.sub('', raw.text) if raw is not None else ""
        text = punctuation_cleaner.sub('', text)

        m = re.search(u'公司名：(\W+)分公司：(\W+)', text)

        try:
            headquarter = m.group(1)
            branch = m.group(2)
            host_store = " ".join([headquarter, branch])
        except Exception as e:
            print(e)

        return host_store

    def get_community(self):
        community = self.infos[u'社區'] if self.__is_key(u'社區') else ""
        return community

    def get_price(self):
        price = 0.0
        unit = ""

        raw = self.soup.find('span', class_='info-price-num')
        unit = self.soup.find('span', class_='info-price-unit')

        if raw is None or unit is None:
            print("cannot find price by class name.")
            return price, unit

        m = re.search('\d+', raw.text)
        price = float(m.group().strip()) if m else 0.0
        unit = clean.sub('', unit.text)

        return price, unit

    def get_price_per_pings(self):
        price = 0
        unit = ""

        raw = self.__find_by_class_name('div', 'info-price-per')

        # get the price field
        text = raw.text.split(' ')[0] if raw is not None else ""

        m = re.search(r'(\d+.\d+)(\W+)', text)

        try:
            price = float(m.group(1))
            unit = m.group(2)
        except Exception as e:
            ping = 0

        return price, unit

    def get_separating_address(self, address):
        city = district = road = ""

        if len(self.navigations) == 0:
            print("navigation list is empty.")
            return city, district, road

        city = self.navigations[2]
        district = self.navigations[3]
        road = address.replace(city, '').replace(district, '')

        return city, district, road

    def get_case_name(self):
        raw = self.__find_by_class_name('h1', 'detail-title-content')

        name = clean.sub('', raw.text) if raw is not None else ""
        name = punctuation_cleaner.sub('', name)


        return name

    def get_case_number(self):
        raw = self.__find_by_class_name('span', 'breadList-last')

        name = re.sub(r'[^a-zA-Z0-9]', '', raw.text) if raw is not None else ""

        return name


    def get_address(self):
        address = self.infos[u'地址'] if self.__is_key(u'地址') else ""
        return address

    def get_parking_space(self):
        parking_space = self.infos[u'車位'] if self.__is_key(u'車位') else ""
        return parking_space

    # 建坪
    def get_building_pings(self):
        building_pings = self.infos[u'權狀坪數'] if self.__is_key(u'權狀坪數') else 0
        if building_pings == 0: return building_pings
        building_pings = self.__extract_floating_number(building_pings)

        return building_pings

    # 地坪
    def get_floor_pings(self):
        floor_pings = self.infos[u'基地面積'] if self.__is_key(u'基地面積') else 0
        floor_pings = self.infos[u'土地坪數'] if self.__is_key(u'土地坪數') else 0
        if floor_pings == 0: return floor_pings
        floor_pings = self.__extract_floating_number(floor_pings)

        return floor_pings

    # 主建物坪數
    def get_main_building_pings(self):
        main_building_pings = self.infos[u'主建物'] if self.__is_key(u'主建物') else 0

        if main_building_pings == 0: return main_building_pings
        main_building_pings = self.__extract_floating_number(main_building_pings)

        return main_building_pings

    # 附屬建物坪數
    def get_attached_building_pings(self):
        attached_building_pings = self.infos[u'附屬建物'] if self.__is_key(u'附屬建物') else 0

        if attached_building_pings == 0: return attached_building_pings
        attached_building_pings = self.__extract_floating_number(attached_building_pings)

        return attached_building_pings

    # 公設
    def get_public_utilities_pings(self):
        public_utilities_pings = self.infos[u'共用部分'] if self.__is_key(u'共用部分') else 0

        if public_utilities_pings == 0: return public_utilities_pings
        public_utilities_pings = self.__extract_floating_number(public_utilities_pings)

        return public_utilities_pings

    # 公設比
    def get_public_utilities_ratio(self):
        public_utilities_ratio = self.infos[u'公設比'] if self.__is_key(u'公設比') else ""
        return public_utilities_ratio

    def get_house_age(self):
        house_age = self.infos[u'屋齡'] if self.__is_key(u'屋齡') else ""
        return house_age

    def get_house_usage(self):
        house_usage = self.infos[u'法定用途'] if self.__is_key(u'法定用途') else ""
        return house_usage

    def get_house_type(self):
        house_type = self.infos['型態'] if self.__is_key(u'型態') else ""

        return house_type

    def get_decorating_level(self):
        decorating_level = self.infos[u'裝潢程度'] if self.__is_key(u'裝潢程度') else ""
        return decorating_level

    def get_lease_state(self):
        lease_state = self.infos[u'帶租約'] if self.__is_key(u'帶租約') else ""
        return lease_state

    def get_house_direction(self):
        house_direction = self.infos[u'朝向'] if self.__is_key(u'朝向') else ""
        return house_direction


    def get_house_layout(self):
        house_layout = self.infos[u'格局'] if self.__is_key(u'格局') else ""
        return house_layout

    # there might have a better solution
    def get_separating_layout(self):
        house_layout = self.get_house_layout()

        num_of_bath = num_of_living = num_of_room = num_of_balcony = 0

        if house_layout == "":
            return num_of_room, num_of_living, num_of_bath, num_of_balcony

        m = re.search(r'(\d+)房', house_layout)
        if m is not None:
            num_of_room = int(m.group(1))

        m = re.search(r'(\d+)廳', house_layout)
        if m is not None:
            num_of_living = int(m.group(1))

        m = re.search(r'(\d+)衛', house_layout)
        if m is not None:
            num_of_bath = int(m.group(1))

        m = re.search(r'(\d+)陽台', house_layout)
        if m is not None:
            num_of_balcony = int(m.group(1))

        return num_of_room, num_of_living, num_of_bath, num_of_balcony

    def get_latitude_longtitude(self):
        lat_lng_pattern = re.compile(r'q=(\d.*?),(\d.*?)&')
        m = lat_lng_pattern.search(self.html)

        try:
            lat = float(m.group(1))
            lng = float(m.group(2))
        except Exception as e:
            print("cannot get the latitude and longtitude")
            lat = lng = 0

        return lat, lng

