__author__ = 'DeityLeD'
import urllib
import urllib2

enable_proxy = True
proxy_handler = urllib2.ProxyHandler({"http":'http://some-proxy.com:8080'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)
values={'username':'89368086@qq.com', 'password':'csw89368086'}
data = urllib.urlencode(values)
user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64)"
headers = {'User_agent': user_agent, 'Referer':'http://www.zhihu.com/articles'}
url2 = "http://www.zhihu.com"
url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
#geturl=url+'?'+data
#print geturl
request = urllib2.Request(url2, data, headers)
response = urllib2.urlopen(request,timeout=20)
print response.read()