# -*- coding: utf-8 -*-
import scrapy


class StateOfColoradoSpiderSpider(scrapy.Spider):
    name = 'state_of_colorado_spider'
    allowed_domains = ['governmentjobs.com']
    
    # AJAX call populates the data to be scraped
    # AJAX call URL is https://www.governmentjobs.com/careers/home/index?agency=colorado&sort=PositionTitle&isDescendingSort=false&department=Governor%27s%20Office%20of%20Information%20Technology
    # How does Scrapy make the AJAX call? Are the request headers correct?
    # SETTING ALL OF THE HEADERS WORKS... but if tokens or session ids expire, we're screwed.
    # Todo: Run spider and see if data still comes back
    def request(self, url, callback):
        request = scrapy.Request(url=url, callback=callback)
        request.headers['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5.0.3578.98 Safari/537.36')
        request.headers['Host'] = ('www.governmentjobs.com')
        request.headers['GET'] = '/careers/home/index?agency=colorado&sort=PositionTitle&isDescendingSort=false&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291 HTTP/1.1'
        request.headers['Host'] = 'www.governmentjobs.com'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Accept'] = '*/*'
        request.headers['X-Requested-With'] = 'XMLHttpRequest'
        request.headers['Content-Type'] = 'text/html'
        request.headers['Referer'] = 'https://www.governmentjobs.com/careers/colorado?department%5B0%5D=Governor%27s%20Office%20of%20Information%20Technology'
        request.headers['Accept-Encoding'] = 'gzip, deflate, br'
        request.headers['Accept-Language'] = 'en-US,en;q=0.9'
        request.headers['Cookie'] = '__RequestVerificationToken=p6JIiTnQefnmN1sK3FaQY0Ltm6qPIyahogO-HEDswFjZJJOvq14fTZYk8khOVIgdZvLiV9XpLF1hr8zraNz6T7R1ah8WlVeOveGc_VNf-2Zl-cixm9UfQXYgrK8b5p_eBo97Yw2; _ga=GA1.2.1910993778.1550295161; _gid=GA1.2.1900312419.1550295161; employer-ga=GA1.2.614792504.1550295161; employer-ga_gid=GA1.2.1635790091.1550295161; _RCRTX03=47c8f99631ac11e98379d3961dff6ca4efd4696d547a4af887c58aa54277c35c; CookieConsent=true; ASP.NET_SessionId=h3nupijtx3xqmdxfait4pk1e; __atuvc=12%7C7; __atuvs=5c67a07778b7fc2300b; ADRUM=s=1550297348085&r=https%3A%2F%2Fwww.governmentjobs.com%2Fcareers%2Fhome%2Findex%3F-1074713280'
        print request.headers
        return request
    
    def start_requests(self):
        url = 'https://www.governmentjobs.com/careers/home/index?agency=colorado&sort=PositionTitle&isDescendingSort=false&department=Governor%27s%20Office%20of%20Information%20Technology&_=1550298837291'
        yield self.request(url, self.parse)


    def parse(self, response):
        yield {
            'test': response.css('ul li h3 a')
        }