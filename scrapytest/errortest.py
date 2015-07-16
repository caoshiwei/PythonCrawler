#coding=utf-8
import urllib2

request = urllib2.Request('http://www.baidu.com')

try:
    urllib2.urlopen(request)
#except urllib2.HTTPError, e:
#    print e.code
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
else:
    print "OK"