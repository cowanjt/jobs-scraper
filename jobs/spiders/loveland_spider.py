# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request


class LovelandSpiderSpider(scrapy.Spider):
    name = 'loveland_spider'
    allowed_domains = ['recruiting2.ultipro.com']


    def start_requests(self):
        target_headers = {
                'Accept'          : 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding' : 'gzip, deflate, br',
                'Accept-Language' : 'en-US,en;q=0.9',
                'Connection'      : 'keep-alive',
                'Content-Type'    : 'application/json; charset=UTF-8',
                'Host'            : 'recruiting2.ultipro.com',
                'Origin'          : 'https://recruiting2.ultipro.com',
                'Referer'         : 'https://recruiting2.ultipro.com/CIT1029CLO/JobBoard/1a9f4e7d-ecfd-4986-bc53-146c0831d8b3/?q=&o=postedDateDesc',
                'X-Requested-With': 'XMLHttpRequest',
            }

        json_payload = {
            "opportunitySearch": 
                {
                    "Top":50,"Skip":0,"QueryString":"","Filters":
                    [
                        {"t":"TermsSearchFilterDto","fieldName":4,"extra":None,"values":[]},
                        {"t":"TermsSearchFilterDto","fieldName":5,"extra":None,"values":[]},
                        {"t":"TermsSearchFilterDto","fieldName":6,"extra":None,"values":[]}
                    ]
                },
            "matchCriteria":
                {
                    "PreferredJobs":[],"Educations":[],"LicenseAndCertifications":[],"Skills":[],"hasNoLicenses":False,"SkippedSkills":[]
                }
        }
        start_urls = ['https://recruiting2.ultipro.com/CIT1029CLO/JobBoard/1a9f4e7d-ecfd-4986-bc53-146c0831d8b3/?q=&o=postedDateDesc']

        for url in start_urls:
            yield Request(url=url, method='POST', headers=target_headers, body=json.dumps(json_payload), callback=self.parse)

    def parse(self, response):
        base_url = 'https://recruiting2.ultipro.com/CIT1029CLO/JobBoard/1a9f4e7d-ecfd-4986-bc53-146c0831d8b3/?q=&o=postedDateDesc'
        print(response.request.method)
        print(response.request.headers)
        print(response.request.body)
        # for description in response.css('#Opportunities > div:nth-child(3) > div'):
        for description in response.css('#Opportunities'):
            #partial_url = description.css('a::attr(href)').get()
            print(description)
            #yield response.follow(base_url + partial_url, callback=self.parse_job)

    def parse_job(self, response):
        employer = 'City of Loveland'

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'employer': employer,
            'job_title': extract_with_css(''),
            'pay_range': extract_with_css(''),
            'department': extract_with_css(''),
            'is_new_job': None,
            'description_url': response.request.url
        }
