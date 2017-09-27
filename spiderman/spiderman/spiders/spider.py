# -*- coding=utf-8 -*-
import re
import json
import time
import scrapy
import logging

from bs4 import BeautifulSoup

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from scrapy.http import FormRequest
from spiderman.items import HouseInfos

from spiderman.spiders import config
from spiderman.spiders.utils import R591_spider, worker
from spiderman.spiders.parser import S_TaiwanParser

class MainSpider(scrapy.Spider):
    name = "estate-spider"

    def start_requests(self):
        start_urls = {
            #'S_Taiwan' : config.TAIWAN_HOUSE_HOME,
            'R_591'    : config.R_591_HOST,
        }

        for task, url in start_urls.items():
            meta = { 'task': task }

            if task == 'S_Taiwan':
                formdata = config.TAIWAN_HOUSE_FORMDATA['sale']
                for ix, city in enumerate(config.CITIES[:1]):
                    formdata['city'] = city
                    meta['formdata'] = formdata

                    url = config.TAIWAN_HOUSE_ROOT+str(ix+1)
                    yield FormRequest(url=url, callback=self.request_pages, formdata=formdata, \
                            headers=config.TAIWAN_HOUSE_HEADERS, meta=meta)

            elif task == 'R_591':
                R591_spider.get(url)
                close_btn = R591_spider.find_element_by_css_selector('a.area-box-close')
                close_btn.click()

                options_btn = R591_spider.find_element_by_css_selector('span.search-location-span')

                for ix, _ in enumerate(config.CITIES[:1]):
                    options_btn.click()
                    city_btns = R591_spider.find_elements_by_css_selector('li.city-li')

                    if len(city_btns):
                        logging.info("Click %s" % city_btns[ix].text)
                        city_btns[ix].click()
                        cookies=R591_spider.get_cookies()
                        time.sleep(2)

                        yield scrapy.Request(url=url, cookies=cookies, callback=self.request_pages, \
                                meta=meta, dont_filter=True)


    # 取得頁面
    def request_pages(self, response):

        task = response.meta['task']

        if task == 'S_Taiwan':
            formdata = response.meta['formdata']
            data = json.loads(response.body.decode('utf-8'))

            final_page = data['toPag']

            for page_num in range(1, final_page+1):
                formdata['nowpag'] = str(page_num)

                yield FormRequest(url=response.url, callback=self.parse_entities, formdata=formdata, \
                        headers=config.TAIWAN_HOUSE_HEADERS, meta=response.meta)

        elif task == 'R_591':
            meta = response.meta
            total = response.css('span.R::text').extract_first()
            final_page = int(total)/30+1

            for cookie in response.request.cookies :
                worker.add_cookie({k: cookie[k] for k in cookie.keys() })

            worker.get(response.url)
            time.sleep(0.5)

            for i in range(1, 3):
                meta['soup'] = BeautifulSoup(worker.execute_script('return document.body.innerHTML'), 'html.parser')

                yield scrapy.Request(url=worker.current_url, callback=self.parse_entities, \
                        meta=meta, dont_filter=True)
                worker.execute_script('$("a.pageNext").click()')
                time.sleep(0.5)



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

        elif task == 'R_591':
            soup = response.meta['soup']
            entries = soup.select('li.infoContent h3 a')

            for entry in entries:
                url = 'https:'+entry['href'].strip()
                yield scrapy.Request(url=url, callback=self.parse_fields, meta={'task': task})

    # 解析物件內容
    def parse_fields(self, response):
        task = response.meta['task']

        if task == 'S_Taiwan':
            infos = response.meta['infos']
            logging.info("Start parsing %s, title: %s" % (response.url, infos['tit']))
            items = S_TaiwanParser.taiwan_sale(response)

            yield HouseInfos(items)

        elif task == 'R_591':
            title = response.css('span.houseInfoTitle::text').extract_first()
            logging.info("Start Parsing %s, title: %s" % (response.url, title))
