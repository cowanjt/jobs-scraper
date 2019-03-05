# -*- coding: utf-8 -*-
import scrapy
import re


class WellingtonSpiderSpider(scrapy.Spider):
    name = 'wellington_spider'
    allowed_domains = ['wellingtoncolorado.gov']
    start_urls = ['http://wellingtoncolorado.gov/jobs.aspx?CatID=104']
    download_delay = 1.5

    def parse(self, response):
        base_url = 'http://wellingtoncolorado.gov/'

        for description in response.css('div#104 div h3'):
            partial_url = description.css('a::attr(href)').get()
            yield response.follow(base_url + partial_url, callback=self.submit_form)
    
    # Working with ASP.NET Web Forms, so we need to navigate to the scraped URL,
    # then submit the form to generate the actual data. 
    def submit_form(self, response):
        # Defining headers for POST.
        target_headers = {
                'Accept'          : '*/*',
                'Accept-Encoding' : 'gzip, deflate',
                'Accept-Language' : 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
                'Connection'      : 'keep-alive',
                'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer'         : response.url,
                'Host'            : 'wellingtoncolorado.gov',
                'Origin'          : 'http://wellingtoncolorado.gov',
                'X-Requested-With': 'XMLHttpRequest',
                'X-MicrosoftAjax' : 'Delta=true',
            }

        # Data we're POSTing to the server.
        form_data = {
                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').get(),

                # RegEx pulls the JobID from the end of the response URL object
                'ctl00$ctl00$MainContent$ModuleContent$ctl00$hdnJobId': re.match('.*?([0-9]+)$', response.url).group(1),
            }
        yield scrapy.FormRequest(response.url, method='POST', meta=response.meta, headers=target_headers, formdata=form_data, callback=self.parse_job)

    def parse_job(self, response):
        employer = 'Town of Wellington'

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'employer': employer,
            'job_title': extract_with_css('h2.withSocial::text'),
            'pay_range': extract_with_css('div#divSideBar div dl dd:nth-child(7)::text'),
            'department': extract_with_css('div#divSideBar div dl dd:nth-child(2)::text'),
            'is_new_job': None,
            'description_url': response.request.url
        }
