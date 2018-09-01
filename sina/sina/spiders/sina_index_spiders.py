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
    # 爬取新浪图集的首页，获得链接
    name = "sina_index"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
       "http://slide.photo.sina.com.cn"
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

    def get_next_url(self, oldUrl, status, data):
        return 'http://slide.photo.sina.com.cn'

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        #print response.body
        #sys.exit()
        status = response.status
        contentArr = []
        r = redis.Redis(host='127.0.0.1',port=6389)
        #r.set('name','hello')
        #print (r.get('name').decode('utf8'))
        for sel in response.xpath('//a'):
        #    print sel
            url = sel.extract()
            #title = title.replace('<title>','');
            #title = title.replace('</title>','');
            #print url
            if 'slide' in url:
                if 'html' in url:
                    #print url
                    urlArr = url.split('"')
                    resUrl = urlArr[1]
                    print resUrl
                    value = r.get(resUrl)
                    if value < 1:
                        r.setex(resUrl, 1, 6400)
                        r.lpush('urllist', resUrl)

        wait = random.randint(30,60)
        time.sleep(wait)
        next_url = self.get_next_url(response.url, status, contentArr)
        if next_url != None:
            yield Request(next_url, dont_filter = True, callback=self.parse)
        return