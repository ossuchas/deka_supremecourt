# -*- coding: utf-8 -*-
import scrapy


class DekaSpider(scrapy.Spider):
    name = 'deka'
    allowed_domains = ['deka.supremecourt.or.th']
    start_urls = ['http://deka.supremecourt.or.th/']

    def parse(self, response):
        pass
