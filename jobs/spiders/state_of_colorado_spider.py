# -*- coding: utf-8 -*-
import scrapy


class StateOfColoradoSpiderSpider(scrapy.Spider):
    name = 'state_of_colorado_spider'
    allowed_domains = ['governmentjobs.com']
    
    def request(self, url, callback):
        request = scrapy.Request(url=url, callback=callback)
        request.headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
        return request
    
    def start_requests(self):
        url = 'https://www.governmentjobs.com/careers/colorado?department%5B0%5D=Governor%27s%20Office%20of%20Information%20Technology'
        yield self.request(url, self.parse)


    def parse(self, response):
        yield {
            'test': response.css('html')
        }