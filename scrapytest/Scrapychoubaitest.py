# -*- coding:utf-8 -*-
__author__ = 'DeityLeD'
import urllib
import  urllib2
import  re

page=1
url = 'http://www.qiushibaike.com/hot/page'+str(page)
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
header = {'User-Agent': user_agent}
try:
    req = urllib2.Request(url, headers=header)
    responce = urllib2.urlopen(req)
   # print responce.read()
except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    if hasattr(e, 'reason'):
        print e.reason
content = responce.read().decode('utf-8')
article = '<div class="author">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?</div>\
.*?<div class="content">(.*?)</div>\
(.*?)<div class="stats">.*?class="number">(.*?)</i>'
pattern = re.compile(article, re.S)
#pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
#                     '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
items = re.findall(pattern,content)
for item in items:
    haveImg = re.search("img",item[2])
    if not haveImg:
        print item[0],item[1],item[3]
