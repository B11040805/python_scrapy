import urllib
import urllib2
import json
import requests
post_url = 'http://180.76.135.235/toutiao/create'
  
postData  = {'content':'aaa','b':'bbb','c':'ccc','d':'ddd'}

#data = json.dumps(postData)
       
#req = urllib2.Request(post_url)
#response = urllib2.urlopen(req,urllib.urlencode({'sku_info':data}))

d = requests.post(post_url, data=postData)
print(d.text)

#response = requests.get("http://180.76.135.235/toutiao/create", params=postData)

#response = requests.get("http://180.76.135.235/toutiao/create")
#print response.text
#response = requests.get("http://www.baidu.com")
#print(type(response.status_code),response.status_code)

#print response.read()
