# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from bs4 import BeautifulSoup
import requests
import random





class NeteasemusicSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    ip_list = []

    def __init__(self):
        web_data = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        self.ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            if tds[5].text.lower() == 'http':
                self.ip_list.append(tds[1].text + ':' + tds[2].text)
        print self.ip_list
    
    def get_random_ip(self, ip_list):
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        return proxy_ip

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
         # Set the location of the proxy
         request.meta['proxy'] = self.get_random_ip(self.ip_list)
