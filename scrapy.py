#! /usr/bin/python
# -*- coding:utf-8 -*-
#Author:xq17

import sys
import itertools
import urlparse
import requests
import itertools
import re
import datetime
from pymongo import MongoClient
from lxml import etree


def dowload(url,user_agent='wswp',num_retries=2):
	print "Dowloading:",url
	try:
		headers = {'User-Agent':user_agent}
		response = requests.get(url,headers=headers)
		html = response.text
		code = response.status_code
		response.raise_for_status() #抛出异常 处理4xx 5xx的错误请求
		# print 'ok'
	except requests.exceptions.HTTPError as e:
		print "Dowload error",e
		html = None
		if num_retries > 0:
			if 500 <= code < 600:
				return dowload(url,user_agent,num_retries-1)
	return html
#正则匹配页面内链接
def get_link(html):
	try:
		webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.I)
		return webpage_regex.findall(html)
	except:
		pass

#基于id的爬虫连续遇到5次错误才停止继续爬(ps:爬死自己博客系列)
def crawbyid(url):
	#maximum number
	max_errors = 5
	#num_errors
	num_errors = 0
	for i in itertools.count(1):
		payload = '?p={}'.format(i)
		response = dowload(url+payload)
		print response
		if response is None:
			num_errors += 1
			if num_errors > max_errors:
				break
		else:
			#success 
			num_errors = 0
#链接爬虫
def link_crawler(seed_url,link_regex='',max_depth=2):
	#given seed URL
	crawl_queue = [seed_url]
	seen  = {seed_url:0}
	while crawl_queue:
		try:
			url = crawl_queue.pop()
			depth = seen[url]
			html = dowload(url)
			if depth != max_depth:
				for link in get_link(html):
					# if re.match(link_regex,link):
					link = urlparse.urljoin(seed_url,link)
					if link not in seen:
						seen[link] = depth + 1 
						crawl_queue.append(link)
		except:
			pass

def data_handle(text,id = 0):
	#使用Xpath解析 修正模块
	html = etree.HTML(text)#返回一个解析对象
	analy_html = etree.HTML(etree.tostring(html,encoding="utf-8"))
	title = html.xpath('//*[@id="wrapper"]/main/div//header/h5/a/text()')
	category = html.xpath('//*[@id="wrapper"]/main/div//header/section/a/text()')
	article_time = html.xpath('//*[@id="wrapper"]/main/div//header/section/span/time[1]/@datetime')
	# //*[@id="wrapper"]/main/header/section/span/time[2]
	# print title
	# print category
	# print time
	#取前5天到现在的文章
	article_data = []
	start_time =  datetime.date.today() - datetime.timedelta(days=5)
	for (title_,category_,time_) in zip(title,category,article_time):
		#格式化时间
		article_t = datetime.datetime.strptime(time_,"%Y-%m-%d").date()
		if article_t > start_time:
			#用,分隔后期方便入库处理
			article_data.append(title_+","+ category_ + "," + time_)
		else:
			return article_data+[None]
	return article_data

#加载url和列表
def paperload(url):
	for i in itertools.count(1):
		page_url= url + '?page={}'.format(i)
		html = dowload(page_url)
		for article_ in data_handle(html):
			if article_ is not None:
				#入库操作
				table =  db_connect()
				#for content in article_.split(','):
				content = article_.split(',')
				data = {'title':content[0],'category':content[1],'time':content[2]}
				table.insert(data)
			else:
				#退出循环
				return 0

def db_connect():
	client = MongoClient("localhost",27017)
	#没有就自动创建
	db = client.paper
	collection = db.article
	return collection
'''
代码测试区域
def test():
	test_list = [1,2,3,4,5,6,7,8]
	seen = {}
	url = 'ss'
	depth = seen[url]
	print depth
	print test_list.pop()
	print seen
	print test_list
	test_list.append(9)
	print seen
'''

def  main():
	url = "https://paper.seebug.org/"
	#crawbyid(url)
	# test()
	# html = dowload(url)
	# print html
	# print get_link(html)
	# link_crawler(url)
	# data_handle(url)
	paperload(url)


if __name__ == '__main__':
	main()