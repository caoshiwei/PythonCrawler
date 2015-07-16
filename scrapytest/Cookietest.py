__author__ = 'DeityLeD'
import urllib2
import cookielib

#cookie = cookielib.CookieJar()

#filename = 'cookie.txt'
#cookie = cookielib.MozillaCookieJar(filename)
#handler = urllib2.HTTPCookieProcessor(cookie)
#opener = urllib2.build_opener(handler)
#responce = opener.open('http://www.baidu.com')
#cookie.save(ignore_discard=True, ignore_expires=True)
#for item in cookie:
#    print 'Name = '+item.name
#    print 'Value = '+item.value
cookie = cookielib.MozillaCookieJar()
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
req = urllib2.Request("http://www.baidu.com")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()
