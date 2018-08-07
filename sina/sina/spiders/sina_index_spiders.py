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
        if not data :
            newurl = oldUrl
            print newurl
            return oldUrl
        if status != 200 :
            newurl = oldUrl
            print newurl
            return oldUrl
        l = oldUrl.split('_')  #用等号分割字符串
        oldIdStr = l[3].split('.')
        oldID = int(oldIdStr[0])
        newID = oldID + 1
        #if newID == 286470:
        #    return 
        newurl = l[0] + '_' + l[1] + '_' + l[2] + '_' + str(newID) + '.' + oldIdStr[1]
        print newurl
        return str(newurl)

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)
    
    def toutiao_create(self, title, data):
        post_url = 'http://180.76.135.235/toutiao/create';
        data_get = json.dumps(data)
        data_f = {'content':data_get,'title':title}
        #print data_f
        response = requests.get("http://180.76.135.235/toutiao/create", params=data_f)
        #req = urllib2.Request(post_url)
        #response = urllib2.urlopen(req,urllib.urlencode({'content':data}))
        #print response

    def parse(self, response):
        #print response.body
        #sys.exit()    
        status = response.status
        contentArr = []
        r = redis.Redis(host='127.0.0.1',port=6379)
        #r.set('name','hello')
        #print (r.get('name').decode('utf8'))
        for sel in response.xpath('//a'):
            #print sel
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
                        r.set(resUrl, 1)
                        r.lpush('urllist', resUrl)
                        
       
        
        wait = random.randint(30,60)
        time.sleep(wait)
        next_url = self.get_next_url(response.url, status, contentArr)
        if next_url != None:
            yield Request(next_url, dont_filter = True, callback=self.parse)
        return
       #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
