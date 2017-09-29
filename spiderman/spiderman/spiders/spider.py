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
from spiderman.spiders.utils import spider, worker
from spiderman.spiders.parser import S_TaiwanParser, S591Parser, R591Parser


class MainSpider(scrapy.Spider):
    name = "estate-spider"

    # part: 第幾Part資料,總共有三Part. part = (1,2,3)
    def __init__(self, part=1, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.part = int(part)

        if self.part == -1:
            self.cities = config.CITIES
        else:
            parts = self._divide_parts()
            self.cities = config.CITIES[parts[self.part-1]:parts[self.part]]

    def _divide_parts(self):
        total = len(config.CITIES)
        step = total/3
        return range(0, total+1, step)

    # 591 Start Request Control Flow 
    def _591_start_flow(self, response):
        spider.get(response.url)

        meta = response.meta
        options_css = meta['options_css']
        city_css = meta['city_css']

        if 'close_css' in meta:
            close_btn = spider.find_element_by_css_selector(meta['close_css'])
            close_btn.click()

        #options_btn = spider.find_element_by_css_selector(options_css)

        for ix, _ in self.cities:

            spider.execute_script('$("%s")[0].click()' % options_css)
            time.sleep(0.5)
            city_btns = spider.execute_script('return $("%s")' % city_css)

            if len(city_btns):
                logging.info("Click %s" % city_btns[ix].text)
                meta = {
                    'city': city_btns[ix].text,
                    'task': meta['task']
                }

                spider.execute_script('$("%s")[%d].click()' % (city_css, ix))
                spider.refresh()
                time.sleep(1)

                cookies=spider.get_cookies()
                yield scrapy.Request(url=spider.current_url, cookies=cookies, callback=self.request_pages, \
                        meta=meta, dont_filter=True)

    def start_requests(self):
        start_urls = {
            #'S_Taiwan' : config.TAIWAN_HOUSE_HOME,
            'R_591' : config.R_591_HOST,
            #'S_591' : config.S_591_HOST,
        }

        for task, url in start_urls.items():
            meta = { 'task': task }

            if task == 'S_Taiwan':
                formdata = config.TAIWAN_HOUSE_FORMDATA['sale']
                for ix, city in self.cities:
                    formdata['city'] = city
                    meta['formdata'] = formdata

                    url = config.TAIWAN_HOUSE_ROOT+str(ix+1)
                    yield FormRequest(url=url, callback=self.request_pages, formdata=formdata, \
                            headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

            elif task == 'S_591':
                meta['options_css'] = 'div.filter-location-btn'
                meta['city_css'] = 'div.region-list-item a'

                yield scrapy.Request(url=url, callback=self._591_start_flow, meta=meta)

            elif task == 'R_591':
                meta['close_css'] = 'a.area-box-close'
                meta['options_css'] = 'span.search-location-span'
                meta['city_css'] = 'li.city-li'

                yield scrapy.Request(url=url, callback=self._591_start_flow, meta=meta)


    # 取得頁面
    def request_pages(self, response):
        meta = response.meta
        task = meta['task']

        if task == 'S_Taiwan':
            formdata = response.meta['formdata']
            data = json.loads(response.body.decode('utf-8'))

            final_page = data['toPag']

            for page_num in range(1, final_page+1):
                formdata['nowpag'] = str(page_num)

                yield FormRequest(url=response.url, callback=self.parse_entries, formdata=formdata, \
                        headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

        # Sale and Rent have the same control flow at paging
        elif '591' in task:
            worker.get(response.url)
            # add cookie after load page (if add cookie before load page, that will be fucked)
            for cookie in response.request.cookies :
                worker.add_cookie({k: cookie[k] for k in cookie.keys() })
            worker.refresh()

            time.sleep(1)
            final_page = worker.execute_script('return $("a.pageNum-form")')[-1].text.strip()
            logging.info("[%s] Final page: %s" % (meta['city'], final_page))

            for i in range(0, int(final_page)):
                logging.info("[%s] page: %d" % (meta['city'], i))

                meta['soup'] = BeautifulSoup(worker.execute_script('return document.body.innerHTML'), \
                                    'html.parser')
                time.sleep(0.5)
                yield scrapy.Request(url=worker.current_url, callback=self.parse_entries, \
                                meta=meta, dont_filter=True)

                worker.execute_script('$("a.pageNext")[0].click()')
                time.sleep(1)


    # 取得每頁的物件PAGE
    def parse_entries(self, response):
        meta = response.meta
        task = meta['task']

        if task == 'S_Taiwan':
            data = json.loads(response.body.decode('utf-8'))
            entries = data['obj']

            for ix, entry in enumerate(entries):
                meta['infos'] = entry
                url = config.TAIWAN_HOUSE_HOST+'/house_%s.html' % (entry['no'])
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

        elif task == 'S_591':
            soup = response.meta['soup']
            entries = soup.select('div.z-hastag div.houseList-item-title a')

            for entry in entries:
                url = config.S_591_HOST+entry['href'].strip()
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

        elif task == 'R_591':
            soup = response.meta['soup']
            entries = soup.select('li.infoContent h3 a')

            for entry in entries:
                url = 'https:'+entry['href'].strip()
                #logging.info('START URL: %s' % url)
                yield scrapy.Request(url=url, callback=self.parse_fields, meta=meta)

    # 解析物件內容
    def parse_fields(self, response):
        task = response.meta['task']

        if task == 'S_Taiwan':
            infos = response.meta['infos']
            logging.info("[%s] Start parsing %s, title: %s" % (task, response.url, infos['tit']))
            items = S_TaiwanParser.Parse(response)

            yield HouseInfos(items)

        elif task == 'S_591':
            title = response.css('h1.detail-title-content::text').extract_first()
            logging.info("[%s] Start Parsing %s, title: %s" % (task, response.url, title.strip()))
            parser = S591Parser(response.body, response.url, u'出售', '591')
            schema = parser.start_parse()

            yield HouseInfos(schema['HouseInfos'])

        elif task == 'R_591':
            title = response.css('span.houseInfoTitle::text').extract_first()
            logging.info("[%s] Start Parsing %s, title: %s" % (task, response.url, title))
            parser = R591Parser(response.body, response.url, u'出租', '591')
            schema = parser.start_parse()

            yield HouseInfos(schema['HouseInfos'])

