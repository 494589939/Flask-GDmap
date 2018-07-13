#! conding = 'UTF-8' 
import requests
from bs4 import BeautifulSoup
import csv

# 第一歩请求安居客的网页
def get_html(url,headers):#,ip):
	try:
		r = requests.get(url,headers=headers)#,proxies=ip)
		r.raise_for_status()
		r.encoding = "utf-8"
		return r.text
	except EOFError as f:
	 	print("出现错误:",f)

# 解析请求到的网页
def get_text(html,house):
	soup = BeautifulSoup(html,'lxml')
	for home in soup.select('.zu-itemmod'):
    	# 重点！！！！！空字典一定要在for循环内否则数据都是一样的	
		site_dict=dict()
		site_dict['info'] = home.select('.zu-info a')[0].text.strip()
		site_dict['price'] = home.select('.zu-side')[0].text.strip()
		# site_dict['details_item'] = home.select('.details-item')[0].text.strip().replace('\ue147','')
		site_dict['link'] = home.select('.zu-info a')[0].get('href')
		site_dict['address'] = home.select('address.details-item')[0].text.split() #地址需要后续处理一下，然后拿去经纬度
		# bot_tag = home.select('.bot-tag')[0].text # 这个朝向不是很重要可以先忽略
		try:
			# 调用高德API函数获取经纬度 注意！！！经纬度如果无法识别就跳过该条信息
			site_dict['lat_lng'] = GDapi(site_dict['address'][:2])
			print(site_dict['address'],'爬取保存成功：')
		# 将爬取到的数据先存到字典然后存入列表模拟json格式
			house.append(site_dict)	
		except IndexError:
			print(site_dict['address'],'解析失败！！！！跳过该条错误！！！！')
			continue
	print('抓取完毕，保存成功')
	return house
		
# 高德经纬度正向解析 注意个人KEY可以解析6000次每天
def GDapi(site):
    # 注意用city 限定范围否则全国搜索容易出现冲突  
	parameters = { 'address' : site, 'city':'温州','key': 'cf008bb492dcb4abaa0990f0c6c55cc4'}
	base = 'http://restapi.amap.com/v3/geocode/geo' 
	response = requests.get(base, parameters)
	info_site = response.json()
	lat_lng = info_site['geocodes'][0]['location']
	return lat_lng


# 备选方案也可以选择将获取到的文件保存为CSV格式用来给后面的地图解析
def save_csv(rows):
	headers = ['Title','Price','Date','Address','Lat_lng', 'link']
	# newline='' 用来取消csv库空一行的问题
	with open('HOUSE.csv','w',encoding='Utf-8',newline='') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(headers)
		f_csv.writerows(rows)

# 将数据写成json格式文件
def save_json(rows):
	with open(r'C:\Users\49458\OneDrive\python-file\Flask\flaskr\static\js\House.js','w',encoding='Utf-8') as f:
		f.write('var districts =')
		f.write(str(rows))
		f.write(';')

def main():
	headers={
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh;q=0.9',
			'cache-control': 'max-age=0',
			'cookie': 'ajk_bfp=1; aQQ_ajkguid=D733C1ED-5420-744C-5E03-8F01ED2A277D; ctid=106; sessid=D2AFF58B-1060-82FE-986F-4DB7497B1E75; twe=2; ajk_member_captcha=77d155af27375eba55ec641695c82908; propertys=j62135-pbhndb_; lps=http%3A%2F%2Fwww.anjuke.com%2F%7Chttps%3A%2F%2Fwww.google.com%2F',
			'dnt': '1',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
			}

	house=list()
	page = 1
	for i in range(1,page+1):
		url = 'https://wz.zu.anjuke.com/fangyuan/luchengb/p{}/?from_price=800&to_price=1501'.format(str(i))
		html = get_html(url,headers)
		rows = get_text(html,house)
	# save_csv(rows)
	save_json(rows)

if __name__ == '__main__':
    main()
