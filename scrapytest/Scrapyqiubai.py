# _*_ coding:utf-8 _*_
__author__ = 'DeityLeD'

import urllib2
import string
import urllib
import re
import thread
import time

class QSBK:

    def __init__(self):
        self.pageIndex = 1
        #self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
        #self.header = {'User_Agent': self.user_agent}
        self.stores = []
        self.enable = False
    def getPage(self, pageIndex):
        url = 'http://www.qiushibaike.com/hot/page/'+str(pageIndex)
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
            return None
        content = responce.read().decode('utf-8')
        return content

    def getPagaItems(self, pageIndex):
        content = self.getPage(pageIndex)
        if not content:
            print "页面加载失败"
            return None
        article = '<div class="author">.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?</div>.*?<div class="content">(.*?)</div>(.*?)<div class="stats">.*?class="number">(.*?)</i>'
        pattern = re.compile(article, re.S)
        #content = content.replace('<br/>', '\n')
        items = re.findall(pattern, content)
        pageStore = []
        for item in items:
            haveImg = re.search("img", item[2])
            a=item[1]
            a=a.replace('<br/>', '\n')
            if not haveImg:
                pageStore.append([item[0].strip(),a.strip(),item[3].strip()])
        return pageStore

    def loadPage(self):
        if self.enable == True:
            if len(self.stores) < 2:
                pageStore = self.getPagaItems(self.pageIndex)
                if pageStore:
                    self.stores.append(pageStore)
                    self.pageIndex += 1

    def getOneStory(self, pageStores, page):
        for story in pageStores:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable=False
                return
            print u'第%d页\t发布人: %s\n%s\n赞%s' %(page,story[0],story[1],story[2])

    def start(self):
        print u"读取糗百，回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stores) > 0:
                pageStores = self.stores[0]
                nowPage += 1
                del self.stores[0]
                self.getOneStory(pageStores, nowPage)

spider = QSBK()
spider.start()