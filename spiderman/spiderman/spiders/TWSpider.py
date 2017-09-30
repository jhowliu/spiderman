# -*- coding: utf-8 -*-
import math
import json
import scrapy
import logging

from bs4 import BeautifulSoup

from scrapy.http import FormRequest
from spiderman.items import HouseInfos

from spiderman.spiders import config
from spiderman.spiders.worker import Worker
from spiderman.spiders.parser import STaiwanParser, RTaiwanParser


class MainSpider(scrapy.Spider):
    name = "tw-spider"

    # part: 第幾Part資料,總共有三Part. part = (1,2,3)
    def __init__(self, part=1, port=4445, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.part = int(part)
        self.worker = Worker(port)

        if self.part == -1:
            self.cities = config.CITIES
        else:
            parts = self._divide_parts()
            self.cities = config.CITIES[parts[self.part-1]:parts[self.part]]

    def _divide_parts(self):
        total = len(config.CITIES)
        step = total/3
        return range(0, total+1, step)

    def start_requests(self):
        start_urls = {
            'S_Taiwan' : config.S_TAIWAN_HOST,
            #'R_Taiwan' : config.R_TAIWAN_HOST
        }

        for task, url in start_urls.items():
            meta = { 'task': task }

            formdata = config.TAIWAN_FORMDATA[task]
            '''
            if task == 'S_Taiwan':
                for ix, city in self.cities:
                    formdata['city'] = city
                    meta['formdata'] = formdata

                    url = config.S_TAIWAN_API+str(ix+1)
                    yield FormRequest(url=url, callback=self.request_pages, formdata=formdata, \
                            headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)
            else:
                for ix, city in self.cities:
                    formdata['rCountyCity'] = city
                    meta['formdata'] = formdata

                    url = config.R_TAIWAN_API+'/searchList.php'
                    yield FormRequest(url=url, callback=self.request_pages, formdata=formdata, \
                            headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)
            '''
            for ix, city in self.cities:
                if task == 'S_Taiwan':
                    formdata['city'] = city
                    url = config.S_TAIWAN_API+str(ix+1)
                else:
                    formdata['rCountyCity'] = city
                    url = config.R_TAIWAN_API+'/searchList.php'

                meta['formdata'] = formdata
                meta['city'] = city

                yield FormRequest(url=url, callback=self.request_pages, formdata=formdata, \
                        headers=config.TAIWAN_HOUSE_HEADERS, meta=meta, dont_filter=True)

    # 取得頁面 for only taiwan
    def request_pages(self, response):
        meta = response.meta

        task = meta['task']
        formdata = meta['formdata']

        if task == 'S_Taiwan':
            #formdata = response.meta['formdata']
            data = json.loads(response.body.decode('utf-8'))

            final_page = data['toPag']

            for page_num in range(1, 3):
                formdata['nowpag'] = str(page_num)
                logging.info('%s - %s - Start Parse Page %d/%d' % \
                        (task, meta['city'], page_num, final_page))

                yield FormRequest(url=response.url, callback=self.parse_entries, formdata=formdata, \
                        headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

        else:
            total = response.css('div.pagetotal span.pricered::text').extract_first()
            final_page = int(math.ceil(int(total)/10.0))

            for page_num in range(1, 3):
                logging.info('%s - %s - Start Parse Page %d/%d' % \
                        (task, meta['city'], page_num, final_page))

                url = config.R_TAIWAN_API+'?page=%d' % page_num

                yield scrapy.Request(url=url, cookies=response.request.cookies, \
                        callback=self.parse_entries, meta=meta, dont_filter=True)


    # 取得每頁的物件PAGE
    def parse_entries(self, response):
        meta = response.meta
        task = meta['task']

        if task == 'S_Taiwan':
            data = json.loads(response.body.decode('utf-8'))
            entries = data['obj']

            for ix, entry in enumerate(entries):
                meta['infos'] = entry
                url = config.S_TAIWAN_HOST+'/house_%s.html' % (entry['no'])
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

        else:
            paths = response.css('div#list-block a.link-orange::attr(href)').extract()

            for path in paths:
                url = '/'.join([config.R_TAIWAN_HOST, path])
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)


    # 解析物件內容
    def parse_fields(self, response):
        task = response.meta['task']

        if task == 'S_Taiwan':
            infos = response.meta['infos']
            logging.info("%s - Start parsing %s - Title: %s" % (task, response.url, infos['tit']))
            parser = STaiwanParser(response.body, response.url, u'出售', 'Taiwan')
            schema = parser.start_parse(infos)

            yield HouseInfos(schema['HouseInfos'])

        else:
            title = response.css('div.h1table h1::text').extract_first()
            logging.info("%s - Start parsing %s - Title: %s" % (task, response.url, title))
            parser = RTaiwanParser(response.body, response.url, u'出租', 'Taiwan')
            schema = parser.start_parse()

            yield HouseInfos(schema['HouseInfos'])
