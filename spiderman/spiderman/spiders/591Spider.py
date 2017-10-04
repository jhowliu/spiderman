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

    def __init__(self, port=4445, RorS='ALL', *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)

        self.cities = config.CITIES

        self.workers = {
            'R_591' : Worker(port),
            'S_591' : Worker(int(port)+1)
        }
        self.start_urls = {
            'R_591' : config.R_591_HOST,
            'S_591' : config.S_591_HOST
        }

        if RorS == 'S':
            self.start_urls.pop('R_591', None)
        elif RorS == 'R':
            self.start_urls.pop('S_591', None)

    def start_requests(self):

        for task, url in self.start_urls.items():
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

        for ix, _ in self.cities:
            retry_times = 3
            # make get website more robust
            while retry_times > 0:
                worker.get(response.url)
                option_clicked = worker.execute_script('$("%s")[0].click()' % options_css)
                # If failed to get option object, go to reopen selenium and wait 10 mins.
                if option_clicked != False: break

                logging.warning('Selenium has problem, wait for 10 mins to resume.')
                worker.reopen()
                retry_times-=1
                time.sleep(600)

            if 'close_css' in meta:
                worker.execute_script('$("%s")[0].click()' % meta['close_css'])

            city_btns = worker.execute_script('return $("%s")' % city_css)

            if len(city_btns):
                city = city_btns[ix].text

                worker.execute_script('$("%s")[%d].click()' % (city_css, ix))
                try:
                    final_page = worker.execute_script('return $("a.pageNum-form")', 0.25)
                    final_page = final_page[-1].text.strip() if len(final_page) else 0
                except:
                    final_page = 0

                # sync request pages (move here to solve selenium async problem)
                for i in range(1, int(final_page)):
                    logging.info("%s - %s - Page: %d/%s" % (task, city, i+1, final_page))

                    html = worker.execute_script('return document.body.innerHTML', 0.25)
                    # If failed to get html page, just give up current city to continue crawling.
                    if (html == False): break

                    meta['soup'] = BeautifulSoup(html, 'html.parser')

                    yield scrapy.Request(url=worker.url, callback=self.parse_entries, \
                                    meta=meta, dont_filter=True)

                    clicked = worker.execute_script('$("a.pageNum-form:contains(%d)")[0].click()' % (i+1), 0.25)
                    # If failed to get click button, just give up current city to continue crawling.
                    if (clicked == False): break

            # threw up the old selenium and open the new after current city crawling over
            worker.reopen()
        # make sure selenium closed
        worker.close()


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

