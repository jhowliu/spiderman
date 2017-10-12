# -*- coding: utf-8 -*-
import math
import json
import scrapy
import logging
import requests

from bs4 import BeautifulSoup

from scrapy.http import FormRequest
from spiderman.items import HouseInfos

from spiderman.spiders import config
from spiderman.spiders.worker import Worker
from spiderman.spiders.parser import RSinYiParser


class MainSpider(scrapy.Spider):
    name = "sy-spider"
    def __init__(self, port=4445, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        #self.worker = Worker(port)

        self.cities = self._get_cities()

    def _get_cities(self):
        cities = []
        resp = requests.get(config.R_SINYI_HOST)
        soup = BeautifulSoup(resp.text, 'html.parser')

        elements = soup.select('.dist a')

        _ = [cities.append((ele['id'], ele['title'])) for ele in elements]

        return cities

    def start_requests(self):
        start_urls = {
            'R_SinYi' : config.R_SINYI_API
        }

        for task, url in start_urls.items():
            meta = { 'task': task }

            for ix, city in self.cities:
                meta['city'] = city
                page_url = url+'?search=1&b=%s' % ix
                yield scrapy.Request(url=page_url, callback=self.request_pages, meta=meta)


    # 取得頁面 for only taiwan
    def request_pages(self, response):
        meta = response.meta
        task = meta['task']

        total = response.css('.counter span::text').extract_first()
        final_page = math.ceil(int(total.replace(',', ''))/20.0)

        for page_num in range(1, int(final_page)+1):
            logging.info('%s - %s - Start Parse Page %d/%d' % \
                    (task, meta['city'], page_num, final_page))

            url = response.url+'&page=%d' % page_num
            yield scrapy.Request(url=url, callback=self.parse_entries, meta=meta)


    # 取得每頁的物件PAGE
    def parse_entries(self, response):
        meta = response.meta
        task = meta['task']

        entries = response.css('li.entry')

        for entry in entries:
            url = entry.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

    # 解析物件內容
    def parse_fields(self, response):
        task = response.meta['task']

        title = response.css('div.main div.top h1::text').extract_first()
        logging.info("%s - Start parsing %s - Title: %s" % (task, response.url, title))
        parser = RSinYiParser(response.body, response.url, u'出租', 'SinYi')
        schema = parser.start_parse()

        yield HouseInfos(schema['HouseInfos'])
