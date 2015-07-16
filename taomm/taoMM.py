#-*- coding:utf-8 -*-
__author__ = 'DeityLeD'

import re
import urllib2
import os
import tool

class taoMM:
    def __init__(self):
        self.baseUrl ='http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()

    def getPage(self,pageNum):
        try:
            URL = self.baseUrl+'?page='+str(pageNum)
            user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64)'
            header = {'User_Agent': user_agent}
            req = urllib2.Request(URL, headers=header)
            response = urllib2.urlopen(req)
            #print response.read().decode('gbk')
            return response.read().decode('gbk')
        except urllib2.URLError, e:
            if hasattr(e,'reason'):
                print u"连接失败，失败原因：", e.reason
                return None

    def getContent(self,pageNum):
        page = self.getPage(pageNum)
        patternStr='<div.*?pic-word.*?<a href="(.*?)" target.*?<img src="(.*?)".*?<a class.*?"_blank">(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
        pattern = re.compile(patternStr, re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            print item[0],item[1],item[2],item[3],item[4]
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents
    def getMMpage(self,infoURL):
        respose = urllib2.urlopen(infoURL)
        return respose.read().decode('gbk')

    def getBrief(self,page):
        patstr = '<div class="mm-aixiu-content".*?>(.*?)<!--'
        pattern = re.compile(patstr, re.S)
        result = re.search(pattern,page)
        return self.tool.replace(result.group(1))

    def getAllImg(self,page):
        patstr = '<div class="mm-aixiu-content".*?>(.*?)<!--'
        pattern = re.compile(patstr,re.S)
        content = re.search(pattern,page)
        patImg = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(patImg,content.group(1))
        return images

    def saveImgs(self,images,name):
        number = 1
        print u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail)>3:
                fTail = "jpg"
            fileName = name + '/' +str(number) + '.' +fTail
            self.saveImg(imageURL,fileName)
            number+=1

    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split(".")
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    def saveImg(self, imgURL, fileName):
        try:
            print imgURL
            u = urllib2.urlopen(imgURL)
            data = u.read()
            f = open(fileName,'wb')
            f.write(data)
            print u'保存一张照片为：',fileName
            f.close()
        except:
            return

    def saveBrief(self,content,name):
        fileName = name+'/'+name+'.txt'
        f = open(fileName,'w+')
        print u'保存个人信息为：',fileName
        f.write(content.encode('utf-8'))

    def mkdir(self,path):
        path = path.strip()
        isExist=os.path.exists(path)
        if not isExist:
            print u"创建了文件：",path
            os.makedirs(path)
            return True
        else:
            print path,u"文件已经创建成功"
            return False

    def savePageInfo(self,pageIndex):
        contents = self.getContent(pageIndex)
        for item in contents[1:]:
            print u"model名字:",item[2],u"年龄:",item[3],u"地址",item[4]
            print u"正在保存",item[2],u"的信息"
            print u"其个人地址",item[0]
            detailRUL = item[0]
            detailPage = self.getMMpage(detailRUL)
            brief = self.getBrief(detailPage)
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            self.saveBrief(brief,item[2])
            self.saveIcon(item[1],item[2])
            self.saveImgs(images,item[2])

    def savePagesInfo(self, start, end):
        for i in range(start,end+1):
            print u"正在寻找第", i, u"页"
            self.savePageInfo(i)

mm = taoMM()
mm.savePagesInfo(1, 1)
