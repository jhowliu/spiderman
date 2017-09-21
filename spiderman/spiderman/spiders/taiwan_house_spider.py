# -*-coding=utf-8 -*-
import re
import json
import scrapy
import logging

from scrapy.http import FormRequest
from spiderman.spiders import config

class TaiwanSpider(scrapy.Spider):
    name = "taiwan_house"

    def start_requests(self):

        payload = config.TAIWAN_HOUSE_PAYLOAD

        for ix, city in enumerate(config.TAIWAN_HOUSE_CITIES):
            url = config.TAIWAN_HOUSE_ROOT+str(ix+1)
            payload['city'] = city
            meta = {
                'payload': payload
            }

            yield FormRequest(url=url, callback=self.request_pages, formdata=payload, \
                    headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

    def request_pages(self, res):
        json_obj = json.loads(res.body.decode('utf-8'))
        final_page = json_obj['toPag']

        payload = res.meta['payload']

        for page_num in range(1, 3):
            payload['nowpag'] = str(page_num)
            yield FormRequest(url=res.url, callback=self.parse_page, formdata=payload, headers=config.TAIWAN_HOUSE_HEADERS)


    def parse_page(self, res):
        json_obj = json.loads(res.body.decode('utf-8'))
        logging.info("start parsing %s, page: %s" % (res.url, json_obj['nowPag']))
