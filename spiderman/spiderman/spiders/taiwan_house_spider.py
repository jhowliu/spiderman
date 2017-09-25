# -*- coding=utf-8 -*-
import re
import json
import scrapy
import logging

from scrapy.http import FormRequest
from spiderman.spiders import config
from spiderman.items import HouseInfos

from spiderman.spiders.parser import tw

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
        infos['CaseURL'] = response.url
        logging.info("start parsing %s, title: %s" % (response.url, infos['tit']))

        tw.taiwan_sale(infos)

        yield HouseInfos(items)
