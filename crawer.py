#coding=utf-8

import urllib2
import re
from bs4 import BeautifulSoup

class Crawer:

    def __init__(self,baseUrl):
        self.url = baseUrl
        try:
            request = urllib2.Request(baseUrl)
        except urllib2.HTTPError, e:  #获取404错误或者其他错误
            print 'Error code: {0} '.format(e.code)
        except urllib2.URLError, e:
            print 'Error reason: ' + e.reason
        response = urllib2.urlopen(request)
        self.data = response.read()

    def findurl(self):
        self.link_list =re.findall(r"http\:.+?\.shtml" ,self.data) #使用正则表达式
        self.result = set([])
        for url in self.link_list:
            if url in self.result:#避免重复的URL
                continue
            else:
                self.result.add(url)

    def usebs(self):
        soup = BeautifulSoup(self.data,"html.parser") #使用beautifulsoup
        #print type(soup)
        a_list = soup.find_all("a")
        self.urls = []
        for a_target in a_list:
            #print a_target.get('href')
            if a_target.get('href') is None:
                continue
            if a_target.get('href') in self.urls:
                continue
            # if a_target.get('href') == 'javascript:void(0)':
            #     continue
            success = re.match(r"http\:\/\/mil\.sohu\.com\/\d{8}.+?\.shtml",a_target.get('href'))#匹配符合要求的URL
            if success:
                self.urls.append(a_target.get('href'))

    def analyse(self):

        for url in self.urls:
            print('\nnow read '+ url + ' \n')
            try:
                request = urllib2.Request(url)
            except urllib2.HTTPError, e:  #获取404错误或者其他错误
                print 'Error code: {0} '.format(e.code)
                continue
            except urllib2.URLError, e:
                print 'Error reason: ' + e.reason
                continue
            response = urllib2.urlopen(request)
            content = response.read()
            soup = BeautifulSoup(content,"html.parser",from_encoding='gb18030')
            print soup.original_encoding
            #article = soup.findall(attrs={"itemprop": "articleBody"})这条完全失效


            all_pages = soup.select(".sele-con > ul > li > a")#检测是否有其他页面





            if len(all_pages) == 0: #这是没有其他页的情况
                article = soup.select(('#contentText > div > p'))
                #有些网页的正文的P结点直接在id为contentText的div下面,所以把他添加上去
                if len(soup.select('#contentText > p')) > 0:
                    for eachp in soup.select('#contentText > p'):
                        article.append(eachp)
                for str in article:
                    if str.find('strong') is None and str.find('a') is None:#去除衍生阅读的链接
                        print(str.get_text())
                        continue

                 #爬取图片配文部分
                for link in soup.select('.text-pic-tt > a' ): #销毁图片配文的链接节点
                    link.decompose()
                article3 = soup.select(".text-pic-tt")
                for string in article3:
                    print(string.get_text())
                continue



            num = 0
            for each_link in all_pages: #如果有其他页面,找到这个新闻的所有页面
                num = num + 1
                print "\nnow read page {0} \n".format(num)
                address = each_link.get('href')
                request2 = urllib2.Request(address)
                response2 = urllib2.urlopen(request2)
                content2 = response2.read()
                soup2 = BeautifulSoup(content2,'html.parser',from_encoding='gb18030')
                article2 = soup2.select('#contentText > div > p')

                 #有些网页的正文的P结点直接在id为contentText的div下面,所以把他添加上去
                if len(soup2.select('#contentText > p')) > 0:
                    for eachp in soup2.select('#contentText > p'):
                        article2.append(eachp)

                for str in article2:
                     if str.find('strong') is None and str.find('a') is None:#去除衍生阅读的链接
                        print(str.get_text())
                        continue

                #爬取图片配文部分,注意这是在有分几个页面的情况下
                for link in soup2.select('.text-pic-tt > a' ): #销毁图片配文的链接节点
                    link.decompose()
                article3 = soup2.select(".text-pic-tt")
                for str in article3:
                    print str.get_text()


    def output(self):
        for url in self.urls:
            print url
        print '\n'
        print len(self.urls)


s = sohu_crawer = Crawer("http://mil.sohu.com/")

sohu_crawer.usebs()
sohu_crawer.output()
sohu_crawer.analyse()




