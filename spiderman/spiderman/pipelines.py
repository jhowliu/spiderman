# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from spiderman.items import HouseInfos

class SpidermanPipeline(object):
    def process_item(self, item, spider):
        logging.info("Coming items: %s\n" % item)
        return item
