# -*- coding: utf-8 -*-
import scrapy


class LarimerCountySpiderSpider(scrapy.Spider):
    name = 'larimer_county_spider'

    start_urls = [
        'https://careers-larimer.icims.com/jobs/search?pr=0&schemaId=&o=&amp&in_iframe=1',
    ]

    def parse(self, response):
        def extract_with_css(job_description, query):
            return job_description.css(query).get(default='').strip()

        for description in response.css('ul li'):
            department = extract_with_css(description, 'div.col-xs-12.additionalFields > div > dl:nth-child(5) > dd > span::text')
            if department == 'Information Technology':
                yield {
                    'job_title': extract_with_css(description, 'div.col-xs-12.title > a > span:nth-child(2)::text'),
                    'pay_range': extract_with_css(description, 'div.col-xs-12.additionalFields > div > dl:nth-child(3) > dd > span::text'),
                    'department': extract_with_css(description, 'div.col-xs-12.additionalFields > div > dl:nth-child(5) > dd > span::text'),
                }

        # Recursively navigate anything with pagination
        # Scrapy uses the href attribute from anchor tags w/o selecting
        # the href attribute directly
        for a in response.css('div.iCIMS_Paginator_Bottom > div > a:nth-child(4)'):
            yield response.follow(a, callback=self.parse)