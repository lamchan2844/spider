# -*- coding: utf-8 -*-
# @Author: chenlin
# @Date:   2016-12-17 00:02:31
# @Last Modified by:   chenlin
# @Last Modified time: 2016-12-18 00:19:34

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
import re
import os
import pandas as pd

date_re = re.compile("\d{4}-\d{2}-\d{2}")  
def crawl_jiuyezhaopin(url = 'http://see.xidian.edu.cn/html/category/8.html'):
	jiuyezhaopin_notification = []
	page_count =  find_page_count(url)
	for i in range(1,page_count+1):
		url_add = url.replace('.html','/%d.html'%i)
		print url_add
		page_jiuyezhaopin_all = urllib2.urlopen(url_add)
		html_jiuyezhaopin_all = BeautifulSoup(page_jiuyezhaopin_all,'lxml')
		jiuyezhaopin_list = html_jiuyezhaopin_all.find(id = 'list_area')
		jiuyezhaopin_list_all = jiuyezhaopin_list.find_all(attrs = {'class' : 'list_item'})
		for jiuyezhaopin_item in jiuyezhaopin_list_all:
			href = jiuyezhaopin_item['href']
			date = jiuyezhaopin_item.find(text = date_re)[1:-1]
			title = jiuyezhaopin_item.text[12:]
			jiuyezhaopin_notification.append([date,title,href])
	if not os.path.exists('../data'):
		os.makedirs('../data')
	with open('../data/jyzp_title.csv','wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerows(jiuyezhaopin_notification)
	
def find_page_count(url):
	page_jiuyezhaopin_all = urllib2.urlopen(url)
	html_jiuyezhaopin_all = BeautifulSoup(page_jiuyezhaopin_all,'lxml')
	page_count_bstring = html_jiuyezhaopin_all.find(id = 'div_page')
	page_count_beg = page_count_bstring.text.find('/')+1
	page_count_end = page_count_bstring.text.find('页',page_count_beg)
	page_count =  int(page_count_bstring.text[page_count_beg:page_count_end])
	return page_count

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
	print article_id
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
	crawl_jiuyezhaopin()
