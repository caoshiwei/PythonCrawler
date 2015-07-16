# _*_ coding:utf-8 _*_
__author__ = 'DeityLeD'

import urllib2
import re


class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceBR = re.compile('<br><br>|<br>')
    #replaceTD= re.compile('<td>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,'',x)
      #  x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,'\n',x)
        return x.strip()

class BDTB:
    def __init__(self,baseUrl,onlyLZ,floorTag):
        self.baseUrl = baseUrl
        self.onlyLZ = '?see_lz=' + str(onlyLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle=u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self, pageNum):
        try:
            url = self.baseUrl+str(self.onlyLZ)+'?pn='+str(pageNum)
            user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
            header = {'User_Agent': user_agent}
            req = urllib2.Request(url, headers=header)
            response = urllib2.urlopen(req)
            #print response.read().decode('utf-8')
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e, 'reason'):
                print U"链接到百度贴吧失败，失败原因：",e.reason
                return None

    def getTitle(self, page):
        titileRe = '<title>(.*?)</title>'
        titlePattern = re.compile(titileRe,re.S)
        title = re.search(titlePattern,page)
        if title:
            #print title.group(1)
            return title.group(1).strip()
        else:
            return None

    def getPageNum(self,page):
        NumRe = '<span class="red">(.*?)</span>'
        NumPattern = re.compile(NumRe,re.S)
        Num = re.search(NumPattern,page)
        if Num:
            #print Num.group(1)
            return Num.group(1).strip()
        else:
            return None

    def getContent(self, page):
        contentRe = '<div id="post_content_.*?j_d_post_content ">(.*?)</div>'
        pattern = re.compile(contentRe, re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "\n"+self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        if title:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle+ ".txt", 'w+')

    def writeData(self,contents):
        for item in contents:
            if self.floorTag =='1':
                floorLine = '\n'+str(self.floor)+u'------------------------------------------------------------\n'
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        print pageNum
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum is None:
            print u'URL已失效'
            return
        try:
            print u'帖子共'+str(pageNum)+u'页'
            for i in range(1,int(pageNum)+1):
                print u'正在写入第'+str(i)+u'页'
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError,e:
            print u"写入异常，原因"+e.message
        finally:
            print u"完成！"


baseUrl='http://tieba.baidu.com/p/3138733512'
print u'帖子：'+ baseUrl
onlyLz = raw_input(u'是否只看楼主：是1，否0：\n')
floorTag = raw_input(u"是否写入楼层信息，是1，否0：\n")
bdtb = BDTB(baseUrl, onlyLz, floorTag)
bdtb.start()
#bdtb.getPage(1)
#bdtb.getContent()
#bdtb.getPageNum()
#bdtb.getTitle()
