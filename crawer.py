import urllib2
import re

class Crawer:

    def __init__(self,baseUrl):
		self.url = baseUrl
		request = urllib2.Request(baseUrl)
		response = urllib2.urlopen(request)
		self.data = response.read()

    def findurl(self):
		self.link_list =re.findall(r"http\:.+?\.shtml" ,self.data)
		self.result = set([])
		for url in self.link_list:
			if url in self.result:
				continue
			else:
				self.result.add(url)


    def output(self):
		for url in self.result:
			print url
		print '\n'
		print len(self.result)


sohu_crawer = Crawer("http://mil.sohu.com/")
sohu_crawer.findurl()
sohu_crawer.output()




# request = urllib2.Request("http://mil.sohu.com/")
# response = urllib2.urlopen(request)
# data = response.read()
# # print data

# link_list =re.findall(r"http\:.+?\.com" ,data)
# result = set([])
# for url in link_list:
# 	if url in result:
# 		continue
# 	else:
# 		result.add(url)
# for url in result:
# 	print url
