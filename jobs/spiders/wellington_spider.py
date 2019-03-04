# -*- coding: utf-8 -*-
import scrapy


class WellingtonSpiderSpider(scrapy.Spider):
    name = 'wellington_spider'
    allowed_domains = ['wellingtoncolorado.gov']
    start_urls = ['http://wellingtoncolorado.gov/']

    def parse(self, response):
        pass
