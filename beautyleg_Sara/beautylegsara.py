#-*- coding:utf-8 -*-
__author__ = 'DeityLeD'

import urllib2
import re
import os

class beautyleg:

    def __init__(self):
        self.page = 1

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

    def getPage(self,URL):
        req = urllib2.Request(URL)
        response = urllib2.urlopen(req)
        page = response.read().decode('utf-8')
        return page

    def getModel(self,page):
        model = '<td align="center" valign="middle".*?<a href="(.*?no.*?)".*?src="(.*?)".*?alt="(.*?)".*?/>'
        pattern = re.compile(model, re.S)
        items = re.findall(pattern, page)
        return items


    def getSara(self,models):
        sara = 'Sara'
        pattern = re.compile(sara, re.S)
        imgURL = []
        for item in models:
            isSara = re.search(pattern, item[2])
            if isSara:
                imgURL.append([item[0],item[2]])
        return imgURL

    def getImgs(self, page):
        pattern = re.compile('<img src="(.*?.jpg)".*?>', re.S)
        Imgs = re.findall(pattern,page)
        return Imgs

    def saveImgs(self,Imgs,name):
        number = 1
        print name,u"照片",len(Imgs),u"张"
        for img in Imgs:
            splitPath = img.split('.')
            fTail = splitPath.pop()
            if len(fTail)>3:
                fTail = "jpg"
            fileName = name + '/' +str(number) + '.' +fTail
            self.saveImg(img,fileName)
            number +=1

    def saveImg(self,img,fileName):
        try:
            u = urllib2.urlopen(img)
            data = u.read()
            f = open(fileName,'wb')
            f.write(data)
            print u'保存一张照片：', fileName
            f.close()
        except:
            return

    def start(self):
        URL =  'http://www.beautyleg.com/list_album.php'
        page = self.getPage(URL)
        models = self.getModel(page)
        imgURL = self.getSara(models)
        for item in imgURL:
            print item[1]
            #pattern = re.compile('BEAUTYLEG (.*?)', re.S)
            name = re.search('BEAUTYLEG (.*)', item[1])
            path = name.group(1)
            print u'保存',path
            imgPage = self.getPage(item[0])
            Imgs = self.getImgs(imgPage)
            self.mkdir(path)
            self.saveImgs(Imgs,path)




mm = beautyleg()
mm.start()
