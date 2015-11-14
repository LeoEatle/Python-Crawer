# coding=utf-8

import urllib2
import re
import codecs
import socket
import jieba
import jieba.analyse
from bs4 import BeautifulSoup


class Crawer:
    def __init__(self, baseUrl):
        socket.setdefaulttimeout(10.0)  # 设置全局超时时间
        self.url = baseUrl
        try:
            request = urllib2.Request(baseUrl)
        except urllib2.HTTPError, e:  # 获取404错误或者其他错误
            print 'Error code: {0} '.format(e.code)
        except urllib2.URLError, e:
            print 'Error reason: ' + e.reason
        response = urllib2.urlopen(request)
        self.data = response.read()
        # 指定要保存数据的文件
        self.fp = codecs.open("text.txt", "w", "utf-8")
        self.key_file = codecs.open("key_word_file.txt","w","utf-8")

    def findurl(self):
        self.link_list = re.findall(r"http\:.+?\.shtml", self.data)  # 使用正则表达式
        self.result = set([])
        for url in self.link_list:
            if url in self.result:  # 避免重复的URL
                continue
            else:
                self.result.add(url)

    def usebs(self):
        soup = BeautifulSoup(self.data, "html.parser")  # 使用beautifulsoup
        # print type(soup)
        a_list = soup.find_all("a")
        self.urls = []
        for a_target in a_list:
            # print a_target.get('href')
            if a_target.get('href') is None:
                continue
            if a_target.get('href') in self.urls:
                continue
            # if a_target.get('href') == 'javascript:void(0)':
            #     continue
            success = re.match(r"http\:\/\/mil\.sohu\.com\/\d{8}.+?\.shtml", a_target.get('href'))  # 匹配符合要求的URL
            if success:
                self.urls.append(a_target.get('href'))

    def analyse(self):

        page_num = 0

        for url in self.urls:
            print('\nnow read ' + url + ' \n')
            #self.fp.write('\nnow read ' + url + ' \n')
            request = urllib2.Request(url)
            try:
                response = urllib2.urlopen(request)
                content = response.read()
            except urllib2.HTTPError, e:  # 获取404错误或者其他错误
                print 'Error code: {0} '.format(e.code)
                continue
            except urllib2.URLError, e:
                print 'Error reason: ' + format(e.reason)
                continue
            except socket.error, e:
                print('socket error')
                continue


            soup = BeautifulSoup(content, "html.parser", from_encoding='gb18030')
            print soup.original_encoding
            # article = soup.findall(attrs={"itemprop": "articleBody"})这条完全失效

            this_page = ""#这是这个页面爬出来的全部文字字符串


            all_pages = soup.select(".sele-con > ul > li > a")  # 检测是否有其他页面

            if len(all_pages) == 0:  # 这是没有其他页的情况
                article = soup.select(('#contentText > div > p'))
                # 有些网页的正文的P结点直接在id为contentText的div下面,所以把他添加上去
                if len(soup.select('#contentText > p')) > 0:
                    for eachp in soup.select('#contentText > p'):
                        article.append(eachp)
                for str in article:
                    if str.find('strong') is None and str.find('a') is None:  # 去除衍生阅读的链接
                        print(str.get_text())
                        self.fp.write(str.get_text() + '\n')
                        this_page = this_page+str.get_text()
                        continue

                        # 爬取图片配文部分
                for link in soup.select('.text-pic-tt > a'):  # 销毁图片配文的链接节点
                    link.decompose()
                article3 = soup.select(".text-pic-tt")
                print "Now print description of images"
                #self.fp.write("Now print description of images" + '\n')
                for string in article3:
                    print(string.get_text())
                    self.fp.write(string.get_text() + '\n')
                    this_page = this_page+string.get_text()

                page_num+=1
                self.extract(this_page,page_num)

                continue

            num = 0
            for each_link in all_pages:  # 如果有其他页面,找到这个新闻的所有页面
                num = num + 1
                print "\nnow read page {0} \n".format(num)
                #self.fp.write('\nnow read page {0} \n'.format(num))
                address = each_link.get('href')
                request2 = urllib2.Request(address)
                try:
                    response2 = urllib2.urlopen(request2)
                    content2 = response2.read()
                except urllib2.HTTPError, e:  # 获取404错误或者其他错误
                    print 'Error code: {0} '.format(e.code)
                    continue
                except urllib2.URLError, e:
                    print 'Error reason: ' + e.reason
                    continue
                except socket.error:
                    print 'socket error'
                    continue

                soup2 = BeautifulSoup(content2, 'html.parser', from_encoding='gb18030')
                article2 = soup2.select('#contentText > div > p')

                # 有些网页的正文的P结点直接在id为contentText的div下面,所以把他添加上去
                if len(soup2.select('#contentText > p')) > 0:
                    for eachp in soup2.select('#contentText > p'):
                        article2.append(eachp)

                for str in article2:
                    if str.find('strong') is None and str.find('a') is None:  # 去除衍生阅读的链接
                        print(str.get_text())
                        self.fp.write(str.get_text() + '\n')
                        this_page = this_page+str.get_text()
                        continue

                # 爬取图片配文部分,注意这是在有分几个页面的情况下
                for link in soup2.select('.text-pic-tt > a'):  # 销毁图片配文的链接节点
                    link.decompose()
                article3 = soup2.select(".text-pic-tt")
                print "Now print the description of images"
                for str in article3:
                    print str.get_text()
                    self.fp.write(str.get_text() + '\n')
                    this_page = this_page+str.get_text()


            page_num+=1
            self.extract(this_page,page_num)

    def output(self):
        for url in self.urls:
            print url
            #self.fp.write(url)
            #self.fp.write(('\n'))
        print len(self.urls)
        #self.fp.write("{0}".format(len(self.urls)))

    def fenci(self):
        print 'start divding Chinese by jieba...'
        file_writer = codecs.open(top_file, "w", "utf-8")
        content = codecs.open('text.txt', 'r','utf-8').read()
        content.strip('abcdefghijklmnopqrstuvwxyz')
        tags = jieba.analyse.extract_tags(content, top_num, withWeight=True)
        num = 0
        for tag in tags:
            num = num + 1
            line = str(num) +"\t\t"+ tag[0] + "\t\t"+ str(tag[1])
            file_writer.writelines(line+'\n')

    def fenci2(self):
        print 'start dividing Chinese by jieba...'
        file_writer = codecs.open(top_file,"w","utf-8")
        content = codecs.open('text.txt','r','utf-8').read()
        #output = re.sub('\w',' ',content)#去掉所有英文描述
        dic = {}
        seg_list = jieba.cut(content, cut_all = False)
        print seg_list
        for word in seg_list:
            word = u''.join(word.split())
            if not dic.has_key(word):

                dic[word] = 0
            dic[word]+=1

        dic = sorted(dic.items(),key = lambda asd:asd[1],reverse = True)
        num = 0
        for i in dic:
            num+=1
            if num == 30:
                continue
            info = str(num) + '\t' + i[0]+'\t'+str(i[1])
            print info
            file_writer.writelines(info)
        file_writer.close()

    def extract(self,this_page,page_num):
        print("This is the key words: ")
        tags = jieba.analyse.extract_tags(this_page, top_num, withWeight=False)
        output = "Website: "+str(page_num)+": "+"/".encode("utf-8").join(tags)
        self.key_file.write(output+'\n')
        print(output)








def fen_sort():
    print 'start dividing Chinese by jieba...'
    file_writer = codecs.open(top_file,"w","utf-8")
    content = codecs.open('text.txt','r','utf-8').read()
    #output = re.sub(' .+','',content)#去掉所有英文描述
    dic = {}
    seg_list = jieba.cut(content, cut_all = True)
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    print seg_list
    for word in seg_list:
        match = zhPattern.search(word)#筛选出中文的词,因为分词结果包含了很多空格
        if match:

            if not dic.has_key(word):
                dic[word] = 0
            dic[word]+=1
        if not match:
            continue

    dic = sorted(dic.items(),key = lambda asd:asd[1],reverse = True)
    num = 0
    for i in dic:
        num+=1
        if num == 31:
            break
        info = str(num) + '\t' + i[0]+'\t'+str(i[1])
        print info
        file_writer.writelines(info)
    file_writer.close()

top_num = 30
top_file = "top_file.txt"

key_word_file = "key_word_file.txt"

s = sohu_crawer = Crawer("http://mil.sohu.com/")
sohu_crawer.usebs()
sohu_crawer.output()
sohu_crawer.analyse()
sohu_crawer.fp.close()
fen_sort()