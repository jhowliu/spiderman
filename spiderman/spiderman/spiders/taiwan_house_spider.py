# -*- coding=utf-8 -*-
import re
import json
import scrapy
import logging

from scrapy.http import FormRequest
from spiderman.spiders import config
from spiderman.items import HouseInfos

class TaiwanSpider(scrapy.Spider):
    name = "taiwan_house_sale"

    def start_requests(self):
        payload = config.TAIWAN_HOUSE_PAYLOAD['sale']

        for ix, city in enumerate(config.TAIWAN_HOUSE_CITIES[:2]):
            payload['city'] = city
            meta = { 'payload': payload }

            url = config.TAIWAN_HOUSE_ROOT+str(ix+1)
            yield FormRequest(url=url, callback=self.request_pages, formdata=payload, \
                    headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

    def request_pages(self, response):
        data = json.loads(response.body.decode('utf-8'))
        payload = response.meta['payload']

        final_page = data['toPag']

        for page_num in range(1, 3):
            payload['nowpag'] = str(page_num)

            yield FormRequest(url=response.url, callback=self.parse_entities, formdata=payload, \
                    headers=config.TAIWAN_HOUSE_HEADERS)


    def parse_entities(self, response):
        data = json.loads(response.body.decode('utf-8'))
        entities = data['obj']

        for ix, entry in enumerate(entities[:1]):
            houseid = entry['no']
            meta = { 'infos': entry }

            url = config.TAIWAN_HOUSE_HOST+'/house_'+houseid+'.html'
            yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

    def parse_fields(self, response):
        infos = response.meta['infos']
        logging.info("start parsing %s, title: %s" % (response.url, infos['tit']))

        price = infos['pay']
        case_no = infos['no']
        case_name = infos['tit']
        road = infos['add']
        city = infos['city']
        district = infos['area']
        addr = city+district+road

        building_pings = infos['pin']
        landing_pings = infos['landpin']

        num_of_living = infos['liv']
        num_of_bed = infos['bed']
        num_of_bath = infos['bat']

        layout = '%s房%s廳%s衛' % (num_of_bed, num_of_living, num_of_bath)

        lat = infos['x']
        lng = infos['y']

        items = {
            'CaseNo': case_no,
            'CaseURL': response.url,
            'CaseName': case_name,
            'Address': addr,
            'City': city,
            'Zip': district,
            'Road': road,
            'Living': num_of_living,
            'Bed': num_of_bed,
            'Bath': num_of_bath,
            'Layout': layout,
            'BuildingPing': building_pings,
            'Latitude': lat,
            'Longtitude': lng,
            'Price': price
        }

        yield items
