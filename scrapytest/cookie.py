__author__ = 'DeityLeD'
import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({'username':'89368086@qq.com', 'pwd':'csw89368086'})

loginUrl = 'https://www.baidu.com/'
result = opener.open(loginUrl, postdata)
cookie.save(ignore_expires=True,ignore_discard=True)
gradeUrl = 'http://i.baidu.com/'
result = opener.open(gradeUrl)
print result.read()
