# -*- coding=utf-8 -*-
import re
import json
import scrapy
import logging

from scrapy.http import FormRequest
from spiderman.spiders import config
from spiderman.items import HouseInfos

from spiderman.spiders.parser import tw

class MainSpider(scrapy.Spider):
    name = "spiderman"

    def start_requests(self):
        start_urls = {
            'S_Taiwan' : config.TAIWAN_HOUSE_HOME,
        }

        for task, url in start_urls.items():

            if task == 'S_Taiwan':
                payload = config.TAIWAN_HOUSE_FORMDATA['sale']
                for ix, city in enumerate(config.CITIES[:1]):
                    payload['city'] = city
                    meta = { 'formdata': formdata, 'task': task }

                    url = config.TAIWAN_HOUSE_ROOT+str(ix+1)
                    yield FormRequest(url=url, callback=self.request_pages, formdata=formdata, \
                            headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

    # 取得頁面
    def request_pages(self, response):

        task = response.meta['task']

        if task== 'S_Taiwan':
            formdata = response.meta['formdata']
            data = json.loads(response.body.decode('utf-8'))

            final_page = data['toPag']

            for page_num in range(1, final_page+1):
                formdata['nowpag'] = str(page_num)

                yield FormRequest(url=response.url, callback=self.parse_entities, formdata=formdata, \
                        headers=config.TAIWAN_HOUSE_HEADERS, meta=response.meta})

    # 取得每頁的物件PAGE
    def parse_entities(self, response):

        task = response.meta['task']

        if task == 'S_Taiwan':
            data = json.loads(response.body.decode('utf-8'))
            entities = data['obj']

            for ix, entry in enumerate(entities):
                entry_id = entry['no']
                meta = { 'infos': entry, 'task': task }

                url = config.TAIWAN_HOUSE_HOST+'/house_{}.html'.format(entry_id)
                logging.info("Start crawl %s." % url)

                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

    # 解析物件內容
    def parse_fields(self, response):
        task = response.meta['task']
        infos = response.meta['infos']

        if task == 'S_Taiwan':
            logging.info("Start parsing %s, title: %s" % (response.url, infos['tit']))
            items = tw.taiwan_sale(response)

            yield HouseInfos(items)

