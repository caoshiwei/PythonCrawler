# -*- coding:utf-8 -*-
__author__ = 'DeityLeD'


import urllib
import urllib2
import re
import cookielib
import webbrowser

class SDU:

    def __init__(self):
        self.loginUrl = 'http://yjxt.bupt.edu.cn/UserLogin.aspx?exit=1'
        self.cookies = cookielib.CookieJar()
        self.post = {
            'UserName': '2013110323',
            'PassWord': 'csw89368086'
        }
        self.postdata = urllib.urlencode(self.post)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def needIdenCode(self):
        #第一次登录获取验证码尝试，构建request
        request = urllib2.Request(url=self.loginUrl,data=self.postdata)
        #得到第一次登录尝试的相应
        response = self.opener.open(request)
        #获取其中的内容
        content = response.read().decode('utf-8')
        #获取状态吗
        status = response.getcode()
        print content
        #状态码为200，获取成功
        if status == 200:
            return content
        else:
            print u"获取请求失败"

    #得到验证码图片
    def getIdenCode(self,page):
        #得到验证码的图片
        pattern = re.compile('<input type="image" name="ValidateImage".*?src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False
    #输入验证码，重新请求，如果验证成功，则返回J_HToken
    def loginWithCheckCode(self):
        #提示用户输入验证码
        checkcode = raw_input(u'请输入验证码:')
        #将验证码重新添加到post的数据中
        self.post['ValidateCode'] = checkcode
        #对post数据重新进行编码
        print self.post
        postdata = urllib.urlencode(self.post)
        try:
            #再次构建请求，加入验证码之后的第二次登录尝试
            request = urllib2.Request(url=self.loginUrl,data=postdata)
            #得到第一次登录尝试的相应
            response = self.opener.open(request)
            #获取其中的内容
            content = response.read().decode('utf-8')
            print content
            #检测验证码错误的正则表达式，\u9a8c\u8bc1\u7801\u9519\u8bef 是验证码错误五个字的编码
            pattern = re.compile(u'\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            #如果返回页面包括了，验证码错误五个字
            if result:
                print u"验证码输入错误"
                return False
            else:
                #返回结果直接带有J_HToken字样，说明验证码输入成功，成功跳转到了获取HToken的界面
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                #如果匹配成功，找到了J_HToken
                if tokenMatch:
                    print u"验证码输入正确"
                    print tokenMatch.group(1)
                    return tokenMatch.group(1)
                else:
                    #匹配失败，J_Token获取失败
                    print u"J_Token获取失败"
                    return False
        except urllib2.HTTPError, e:
            print u"连接服务器出错，错误原因",e.reason
            return False
    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needIdenCode()
        #请求获取失败，得到的结果是None
        if not needResult ==None:
            if not needResult == False:
                print u"您需要手动输入验证码"
                idenCode = self.getIdenCode(needResult)
                imageurl = 'yjxt.bupt.edu.cn/'+idenCode
                #得到了验证码的链接
                if not imageurl == False:
                    print u"验证码获取成功"
                    print u"请在浏览器中输入您看到的验证码"
                    webbrowser.open_new_tab(imageurl)
                    J_HToken = self.loginWithCheckCode()
                    print "J_HToken",J_HToken
                #验证码链接为空，无效验证码
                else:
                    print u"验证码获取失败，请重试"
            else:
                print u"不需要输入验证码"
        else:
            print u"请求登录页面失败，无法确认是否需要验证码"

sdu = SDU()
sdu.main()