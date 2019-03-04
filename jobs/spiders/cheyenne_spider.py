# -*- coding: utf-8 -*-
import scrapy


class CheyenneSpiderSpider(scrapy.Spider):
    name = 'cheyenne_spider'
    allowed_domains = ['www.cheyennecity.org']
    start_urls = ['https://www.cheyennecity.org/jobs.aspx?CommunityJobs=False&CatID=Professional-86']
    #start_urls = ['https://www.cheyennecity.org/jobs.aspx?CommunityJobs=False&CatID=Operations-Maintenance-85']
    download_delay = 1.5

    def parse(self, response):
        base_url = 'https://www.cheyennecity.org'

        for description in response.css('div#86 div h3'):
            partial_url = description.css('a::attr(href)').get()
            print('Follow URL:' + base_url + partial_url)
            yield response.follow(base_url + partial_url, callback=self.submit_form)
    
    def submit_form(self, response):
        print('called')
        target_headers = {
                'Accept'          : '*/*',
                'Accept-Encoding' : 'gzip, deflate',
                'Accept-Language' : 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
                'Connection'      : 'keep-alive',
                'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer'         : self.start_urls[0],
                'X-Requested-With': 'XMLHttpRequest',
                'X-MicrosoftAjax' : 'Delta=true',
            }
        yield scrapy.FormRequest.from_response(response, method='POST', meta=response.meta, headers=target_headers, callback=self.parse_job)

    def parse_job(self, response):
        employer = 'City of Cheyenne'

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'employer': employer,
            'job_title': extract_with_css('h2.withSocial::text'),
            'pay_range': extract_with_css('div#divSideBar div dl dd:nth-child(2)::text'),
            'department': extract_with_css('div#divSideBar div dl dd:nth-child(7)::text'),
            'is_new_job': None,
            'description_url': response.request.url
        }