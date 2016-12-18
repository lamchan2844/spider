# -*- coding: utf-8 -*-
# @Author: chenlin
# @Date:   2016-12-17 23:04:18
# @Last Modified by:   chenlin
# @Last Modified time: 2016-12-18 00:39:44
import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
import os
import re
def crawl_jyzp_content(title,date,url,url_base = 'http://see.xidian.edu.cn'):
	if not os.path.exists('../data/jyzp'):
		os.makedirs('../data/jyzp')
	if not os.path.exists('../data/jyzp/article'):
		os.makedirs('../data/jyzp/article')
	print url
	pattern = re.compile(r'\d+.html')
	match = pattern.search(url)
	try:
		article_id = str(match.group())
		article_id = article_id[:-5]
	except:
		print url,'wrong!-----------------'
	#print article_id
	page = urllib2.urlopen(url)
	html = BeautifulSoup(page,'lxml')
	article = html.find(id = 'article')
	article_content = article.find(id = 'article_content')
	#print article_content.text.encode('utf-8')
	target_file = '../data/jyzp/article/jyzb'+article_id+'.txt'
	open(target_file,'wb').write(title+'\n'+date+'\n')
	open('../data/jyzp/article/jyzb'+article_id+'.txt','ab+').write(article_content.text.encode('utf-8'))
	insertfile_hrefs = ''
	insertfile_all = article_content.find_all(attrs={'class':'ke-insertfile'})
	for insertfile in insertfile_all:
		insertfile_hrefs = insertfile_hrefs + ' ' + url_base+insertfile['href']
	insertfile_hrefs = insertfile_hrefs.strip()
	result = [target_file,insertfile_hrefs]
	return result
	 



if __name__ == '__main__':
	article_all = []
	with open('../data/jyzp_title.csv','rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			date,title,href =  row
			#print row
			content = crawl_jyzp_content(title,date,href)
			row.extend(content)
			article_all.append(row)

	with open('../data/jyzp.csv','wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerows(article_all)

			
			

'''
#url = 'http://www.xidian.edu.cn/'
url = 'http://see.xidian.edu.cn/html/news/8579.html'
#url = 'http://www.baidu.com/'
date_re = re.compile("\d+-\d+-\d+")  
#response = requests.get(url)
page = urllib2.urlopen(url)
#print response.text.decode('utf-8').encode('utf-8')
html = BeautifulSoup(page,'lxml')
article = html.find(id = 'article')

article_title = article.h1.text
article_detail = article.find(id = 'article_detail')
article_data =  article_detail.find(text=date_re)

article_content = article.find(id = 'article_content')
insertfile = article_content.find(attrs={'class':'ke-insertfile'})
insertfile_href = article_content.a['href']

'''