# -*- coding: utf-8 -*-
import scrapy


class WindsorSpiderSpider(scrapy.Spider):
    name = 'windsor_spider'
    allowed_domains = ['governmentjobs.com']

    def request(self, url, callback):
        request = scrapy.Request(url=url, callback=callback)
        request.headers['X-Requested-With'] = 'XMLHttpRequest'
        return request
    
    # Ugly. There has to be a way to navigate the pagination that's done via AJAX.
    def start_requests(self):
        start_urls = [
            'https://www.governmentjobs.com/careers/home/index?agency=windsorgov&_=1551722500110&page=1',
            'https://www.governmentjobs.com/careers/home/index?agency=windsorgov&_=1551722500110&page=2',
            'https://www.governmentjobs.com/careers/home/index?agency=windsorgov&_=1551722500110&page=3',
            'https://www.governmentjobs.com/careers/home/index?agency=windsorgov&_=1551722500110&page=4',
            'https://www.governmentjobs.com/careers/home/index?agency=windsorgov&_=1551722500110&page=5',
            'https://www.governmentjobs.com/careers/home/index?agency=windsorgov&_=1551722500110&page=6',
        ]
        for url in start_urls:
            yield self.request(url, self.parse)


    def parse(self, response):
        base_url = 'https://www.governmentjobs.com'
        employer = 'Town of Windsor'

        def extract_with_css(job_description, query):
            return job_description.css(query).get(default='').strip()

        for description in response.css('div.search-results-grid-container > table > tbody tr'):
            department = extract_with_css(description, 'td.job-table-department::text')
            # Determine what the Town of Windsor calls their IT department
            if department == 'Information Technology':
                yield {
                    'employer': employer,
                    'job_title': extract_with_css(description, 'h3 a::text'),
                    'pay_range': extract_with_css(description, 'td.job-table-salary::text'),
                    'department': 'Information Technology',
                    'is_new_job': None,
                    'description_url': base_url + extract_with_css(description, 'h3 a::attr(href)')
                }
