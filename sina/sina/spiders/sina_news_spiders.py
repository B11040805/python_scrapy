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
    name = "sina_news"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://slide.sports.sina.com.cn/star/slide_2_730_189939.html"
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
        r = redis.Redis(host='127.0.0.1',port=6379)
        url = r.rpop('urllist')
        return url
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
        #r = redis.Redis(host='127.0.0.1',port=6379)
        #url = r.rpop('newsurllist') 
        url = 'http://ent.sina.com.cn/v/m/2018-08-06/doc-ihhhczfc5437378.shtml'
        print url
        yield Request(url, callback=self.parse)
    
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
        for sel in response.xpath('//title'):
            title = sel.extract()
            title = title.replace('<title>','');
            title = title.replace('</title>','');
            print title
           
        for sel in response.xpath('//div[@class="article"]'):
            #print sel
            #line = sel.extract()
            
            #print line
            for item in sel.xpath('//p/text()'):
                print item.extract()
            #content = {}
            #content['p'] = line[4]
            #content['img'] = line[0]
            #contentArr.append(content)
            #print line[0], line[4]
        for sel in response.xpath('//div[@class="img_wrapper"]'):
            for item in sel.xpath('//img/@src'):
                print item.extract()
        sys.exit()    
        self.toutiao_create(title,contentArr)
        #sys.exit()
        wait = random.randint(60,300)
        time.sleep(wait)
        next_url = self.get_next_url(response.url, status, contentArr)
        if next_url != None:
            yield Request(next_url, dont_filter = True, callback=self.parse)
        else:
            time.sleep(wait)
            next_url = 'http://slide.ent.sina.com.cn/film/h/slide_4_704_211.html' #self.get_next_url(response.url, status, contentArr)
            yield Request(next_url, dont_filter = True, callback=self.parse)
        return
       #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
