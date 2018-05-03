#!/usr/bin/env python  
# -*- coding: utf-8 -*-

""" 
@version: v1.0 
@author: SHIFengCN 
@license: Apache Licence  
@contact: shifree@gmail.com
@site: https://github.com/shifengcn 
@software: PyCharm 
@file: taobao_test.py 
@time: 2018/5/2 0002 13:08 
"""
import json
import re
import requests
import time
import xlwt
import urllib

def append_data(data,data_list):
	for item in data_list:
		detail = {
			'title': item['title'],
			'location': item['item_loc'],
			'price': item['view_price'],
			'isTmall': '是' if item['shopcard']['isTmall'] else '否',
		}
		# print(item)
		data.append(detail)
url_search=input('请输入搜索词：')
url_search=urllib.parse.quote(url_search,encoding='utf8')
#print(url_search)
url='https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180502&ie=utf8'.format(url_search,)
response=requests.get(url)
html=response.text
content=re.findall(r'g_page_config = (.*)g_srp_loadCss',html,re.S)#re.S:识别字符串内没有显示的符号，如空格/换行回车等
#取列表的第零项，然后取出两端空格和分好，再转换为字典，提取字典内所需的数据
data_list=json.loads(content[0].strip()[:-1])['mods']['itemlist']['data']['auctions']
data=[]#初始化定义结果列表
append_data(data,data_list)
url='https://s.taobao.com/api?_ksTS=1525237552433_224&callback=jsonp225&ajax=true&m=customized&stats_click=search_radio_all:1&q=sony%20%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%BB%B4%E4%BF%AE&s=36&imgfile=&initiative_id=staobaoz_20180502&bcoffset=0&js=1&ie=utf8&rn=75abace362808e740321381456be88f3'
cookies=response.cookies#需要cookies保持
response=requests.get(url,cookies=cookies)
html=response.text
content=re.findall(r'{.*}',html)
data_list=json.loads(content[0])['API.CustomizedApi']['itemlist']['auctions']
append_data(data,data_list)
#cookies保持
cookies=response.cookies
#翻页(1到10页）
for i in range(1,10):
	#以下内容根据chrome数据请求的headers进行分析得来
	timestamp=time.time()
	_ksTs='%s_%s' % (str(int(timestamp)*1000),str(timestamp)[-3:])
	callback='json%s' % (int(str(timestamp)[-3:])+1)
	data_value=44*i
	url='https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&_ksTS={}&callback={}&q=sony+%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%BB%B4%E4%BF%AE&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180502&ie=utf8&bcoffset=4&p4ppushleft=2%2C48&s=44&ntoffset=4'.format(data_value,_ksTs,callback)
	response=requests.get(url,cookies=cookies)
	html=response.text
	content = re.findall(r'{.*}', html, re.S)  # re.S:识别字符串内没有显示的符号，如空格/换行回车等
	content = json.loads(content[0])  # 转换为字典
	# 获取信息列表
	data_list = content['mods']['itemlist']['data']['auctions']
	append_data(data,data_list)
	cookies = response.cookies#cookies持久化
#数据持久化，写入xls
f=xlwt.Workbook(encoding='utf8')
sheet01=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
sheet01.write(0,0,'品名')
sheet01.write(0,1,'发货地')
sheet01.write(0,2,'价格')
sheet01.write(0,3,'是否天猫')
for i in range(len(data)):
	sheet01.write(i+1,0,data[i]['title'])
	sheet01.write(i+1,1,data[i]['location'])
	sheet01.write(i+1,2,data[i]['price'])
	sheet01.write(i+1,3,data[i]['isTmall'])
f.save('save.xls')

