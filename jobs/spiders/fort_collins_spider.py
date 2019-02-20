# -*- coding: utf-8 -*-
import scrapy
import re


class FortCollinsSpiderSpider(scrapy.Spider):
    name = 'fort_collins_spider'
    allowed_domains = ['fcgov.csod.com']
    start_urls = ['https://fcgov.csod.com/ats/careersite/search.aspx?site=1&c=fcgov']

    def parse(self, response):
        employer = 'City of Fort Collins'

        base_url = 'https://fcgov.csod.com/ats/careersite/'
        pattern = r'JobDetails.aspx\?site\=[0-9]\&id\=[0-9][0-9][0-9][0-9]'

        for list_item in response.css('div#ctl00_siteContent_widgetLayout_rptWidgets_ctl00_widgetContainer_ctl00_ctl00 ul li'):
            partial_url = re.search(pattern, list_item.css('a::attr(href)').get())

            yield {
                'employer': employer,
                'job_title': list_item.css('a::text').get(default='').strip(),
                'pay_range': 'See Job Description',
                'department': 'See Job Description',
                'is_new_job': None,
                'description_url': base_url + partial_url.group()
            }

        # base_url = 'https://fcgov.csod.com/ats/careersite/'
        # pattern = r'JobDetails.aspx\?site\=[0-9]\&id\=[0-9][0-9][0-9][0-9]'

        # for list_item in response.css('div#ctl00_siteContent_widgetLayout_rptWidgets_ctl00_widgetContainer_ctl00_ctl00 ul li'):
        #     partial_url = re.search(pattern, list_item.css('a::attr(href)').get())
        #     yield response.follow(base_url + partial_url.group(), self.parse_job)

    # Todo: Figure out how to traverse inconsitent DOMs. 
    # def parse_job(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).get(default='').strip()

    #     yield {
    #         'job_title': extract_with_css('div.cs-atscs-jobdet-rtpane strong:nth-child(1)::text'),
    #         'pay_range': extract_with_css('//*[@id="ctl00_careerSiteContainer"]/div[3]/div[3]/p[1]/span/font[1]/strong[2]'),
    #         'department': extract_with_css('//*[@id="ctl00_careerSiteContainer"]/div[3]/div[3]/p[1]/span/font[1]/strong[contains(.,\'Department\')]'),
    #     }