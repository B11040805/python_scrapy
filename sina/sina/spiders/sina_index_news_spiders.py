# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
import urllib
import urllib2
import json
import requests
import random
import time
import redis
from scrapy import Request
class SinaSpider(scrapy.Spider):
    name = "sina_index_news"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
       "http://ent.sina.com.cn/" 
    ]
    cookies = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def get_next_url(self):
        return self.start_urls[0]

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)
    

    def parse(self, response): 
        status = response.status
        contentArr = []
        r = redis.Redis(host='127.0.0.1',port=6379)
        for sel in response.xpath('//a'):
            url = sel.extract()
            if 'doc' in url:
                if 'html' in url:
                    urlArr = url.split('"')
                    resUrl = urlArr[1]
                    value = r.get(resUrl)
                    if value < 1:
                        r.setex(resUrl, 1, 86400)
                        r.lpush('newsurllist', resUrl)
                    
        wait = random.randint(30,60)
        time.sleep(wait)
        next_url = self.get_next_url()
        if next_url != None:
            yield Request(next_url, dont_filter = True, callback=self.parse)
        return
