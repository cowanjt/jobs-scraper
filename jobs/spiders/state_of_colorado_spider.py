# -*- coding: utf-8 -*-
import scrapy


class StateOfColoradoSpiderSpider(scrapy.Spider):
    name = 'state_of_colorado_spider'
    allowed_domains = ['governmentjobs.com']
    
    def request(self, url, callback):
        request = scrapy.Request(url=url, callback=callback)
        request.headers['X-Requested-With'] = 'XMLHttpRequest'
        return request
    
    # Ugly. There has to be a way to navigate the pagination that's done via AJAX.
    def start_requests(self):
        start_urls = [
            'https://www.governmentjobs.com/careers/home/index?agency=colorado&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291&page=1',
            'https://www.governmentjobs.com/careers/home/index?agency=colorado&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291&page=2',
            'https://www.governmentjobs.com/careers/home/index?agency=colorado&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291&page=3',
            'https://www.governmentjobs.com/careers/home/index?agency=colorado&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291&page=4',
            'https://www.governmentjobs.com/careers/home/index?agency=colorado&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291&page=5',
            'https://www.governmentjobs.com/careers/home/index?agency=colorado&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291&page=6',
        ]
        for url in start_urls:
            yield self.request(url, self.parse)


    def parse(self, response):
        def extract_with_css(job_description, query):
            return job_description.css(query).get(default='').strip()

        for description in response.css('div.search-results-grid-container > table > tbody tr'):
            yield {
                'job_title': extract_with_css(description, 'h3 a::text'),
                'pay_range': extract_with_css(description, 'td.job-table-salary::text'),
                'department': 'Information Technology',
            }        