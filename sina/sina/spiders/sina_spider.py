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
    name = "sina"
    allowed_domains = ["sina.com.cn"]
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
        r = redis.Redis(host='127.0.0.1',port=6389)
        url = r.rpop('urllist')
        return url

    def start_requests(self):
        r = redis.Redis(host='127.0.0.1',port=6389)
        url = r.rpop('urllist')


        yield Request(url, callback=self.parse)

    def toutiao_create(self, title, data):
        post_url = 'http://180.76.135.235/toutiao/create';
        data_get = json.dumps(data)
        print data_get
        print title
        #sys.exit()
        data_f = {'content':data_get,'title':title}
        #print data_f
        #response = requests.get("http://180.76.135.235/toutiao/create", params=data_f)
        #req = urllib2.Request(post_url)
        #response = urllib2.urlopen(req,urllib.urlencode(data_f))
        response = requests.post(post_url, data = data_f)
        print 'fanhui'
        print response
        print response.text
    def parse(self, response):
        status = response.status
        contentArr = []
        for sel in response.xpath('//title'):
            title = sel.extract()
            title = title.replace('<title>','');
            title = title.replace('</title>','');
            print title

        for sel in response.xpath('//dl'):
           # print sel
            line = sel.xpath('dd/text()').extract()
            #for item in line:
            content = {}
            content['p'] = line[4]
            content['img'] = line[0]
            contentArr.append(content)
            #print line[0], line[4]

        self.toutiao_create(title,contentArr)
        #sys.exit()
        wait = random.randint(60,300)
        time.sleep(wait)
        next_url = self.get_next_url(response.url, status, contentArr)
        if next_url != None:
            yield Request(next_url, dont_filter = True, callback=self.parse)
        else:
            time.sleep(wait)
            next_url = self.get_next_url(response.url, status, contentArr)
            yield Request(next_url, dont_filter = True, callback=self.parse)
        return