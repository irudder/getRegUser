#coding:utf-8
import sys
import urllib
import urllib2
import re
 
class FetchUrl:
    """This a BaiduCrawler for get subUrl of PageContent"""
    
    def __init__(self, strKeyword, iPages = 1):
        '''Some Inition'''
        self.m_strKeyword = strKeyword
        self.m_iPages = iPages
        
    def GetSubPageUrlList(self, url, comreg):
        '''Fetch subUrl of Pages'''
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            print "******Get A HTTPError, Try again*****"
            response = urllib2.urlopen(url)
        except urllib2.URLError, e:
            print "******Get An URLError, Try again*****"
            response = urllib2.urlopen(url)
        htmlpage = response.read()
        infoList1 = re.findall(comreg, htmlpage)
        #将列表去重之后返回
        return list(set(infoList1))
 
    def GetUrlList(self):
        '''获取结果页面中指定页数的子链接'''
        mainList = [];
        reg = r'http://www.baidu.com/link\?url=.[^\"]+'
        comreg = re.compile(reg)
        print "任务的关键词为：%s" % self.m_strKeyword
        #将关键词进行url编码
        encodeKeyword = urllib.quote(self.m_strKeyword)
        i = 0
        while i <= self.m_iPages:
            url = 'http://www.baidu.com/s?wd=%s&pn=%d&tn=baiduhome_pg&ie=utf-8&usm=0' % (encodeKeyword, i)
            subList = self.GetSubPageUrlList(url, comreg)
            mainList += subList
            print url
            i += 10
        return mainList
 
    def FetchRealUrl(self, urlList):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        i = 0
        bFind = False
        print "一共有%d个链接" % len(urlList)
        for url in urlList:
            print url
            req = urllib2.Request(url, headers = headers)
            try:
                response = urllib2.urlopen(req)
                #获取页面的真实的链接
                strRealUrl = response.geturl()
                w = open('log.txt', 'a')
                w.write("%s\n" % strRealUrl)
                w.close()
                print "Real Url:" + strRealUrl
                print "-----------------------------------"
            except urllib2.HTTPError, e:
                print "******Get A HTTPError, skip to next url*****"
                continue
            except urllib2.URLError, e:
                print "******Get An URLError, skip to next url*****"
                continue
    
'''解析启动参数'''
for i in range(1,10):

	crawler = FetchUrl("intitle:找回密码",i)
	urlList = crawler.GetUrlList()
	crawler.FetchRealUrl(urlList)