# -*- coding: utf-8 -*-
import re
import json
import time
import scrapy
import logging

from bs4 import BeautifulSoup

from scrapy.http import FormRequest
from spiderman.items import HouseInfos

from spiderman.spiders import config
from spiderman.spiders.worker import Worker
from spiderman.spiders.parser import S_TaiwanParser, S591Parser, R591Parser


class MainSpider(scrapy.Spider):
    name = "591-spider"

    # part: 第幾Part資料,總共有三Part. part = (1,2,3)

    def __init__(self, part=-1, port=4445, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.part = int(part)
        self.workers = {
            'R_591' : Worker(port),
            'S_591' : Worker(int(port)+1)
        }

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
            'R_591' : config.R_591_HOST,
            'S_591' : config.S_591_HOST,
        }

        for task, url in start_urls.items():
            meta = { 'task': task }

            if task == 'S_591':
                meta['options_css'] = 'div.filter-location-btn'
                meta['city_css'] = 'div.region-list-item a'

            elif task == 'R_591':
                meta['close_css'] = 'a.area-box-close'
                meta['options_css'] = 'span.search-location-span'
                meta['city_css'] = 'li.city-li'

            yield scrapy.Request(url=url, callback=self.start_591_flow, meta=meta)

    # 591 Start Request Control Flow 
    def start_591_flow(self, response):
        meta = response.meta

        task = meta['task']
        options_css = meta['options_css']
        city_css = meta['city_css']

        worker = self.workers[task]

        worker.get(response.url)

        if 'close_css' in meta:
            worker.execute_script('$("%s")[0].click()' % meta['close_css'])

        for ix, _ in self.cities:
            worker.execute_script('$("%s")[0].click()' % options_css)

            city_btns = worker.execute_script('return $("%s")' % city_css)

            if len(city_btns):
                city = city_btns[ix].text

                worker.execute_script('$("%s")[%d].click()' % (city_css, ix))
                final_page = worker.execute_script('return $("a.pageNum-form")')[-1].text.strip()

                # sync request pages (move here to solve selenium async problem)
                for i in range(0, int(final_page)):
                    logging.info("%s - %s - Page: %d/%s" % (task, city, i+1, final_page))

                    meta['soup'] = BeautifulSoup(worker.execute_script('return document.body.innerHTML'), \
                                        'html.parser')
                    if (not worker.execute_script('$("a.pageNext")[0].click()')): continue

                    yield scrapy.Request(url=worker.url, callback=self.parse_entries, \
                                    meta=meta, dont_filter=True)

    # 取得每頁的物件PAGE
    def parse_entries(self, response):
        meta = response.meta

        soup = meta['soup']
        task = meta['task']

        if task == 'S_591':
            entries = soup.select('div.z-hastag div.houseList-item-title a')

            for entry in entries:
                url = config.S_591_HOST+entry['href'].strip()
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

        elif task == 'R_591':
            entries = soup.select('li.infoContent h3 a')

            for entry in entries:
                url = 'https:'+entry['href'].strip()
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

    # 解析物件內容
    def parse_fields(self, response):
        task = response.meta['task']

        if task == 'S_591':
            title = response.css('h1.detail-title-content::text').extract_first()
            logging.info("%s - Start Parsing %s, title: %s" % (task, response.url, title.strip()))
            parser = S591Parser(response.body, response.url, u'出售', '591')
            schema = parser.start_parse()

            yield HouseInfos(schema['HouseInfos'])

        elif task == 'R_591':
            title = response.css('span.houseInfoTitle::text').extract_first()
            logging.info("%s - Start Parsing %s, title: %s" % (task, response.url, title))
            parser = R591Parser(response.body, response.url, u'出租', '591')
            schema = parser.start_parse()

            yield HouseInfos(schema['HouseInfos'])

