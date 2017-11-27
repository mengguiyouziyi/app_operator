# -*- coding: utf-8 -*-
import re
import json
import scrapy
import time
from urllib.parse import quote_plus
from scrapy.spiders import Spider
from scrapy.selector import Selector
from app.items import AppItem
from app.utils.info import startup_nodes
from rediscluster import StrictRedisCluster
from scrapy.exceptions import CloseSpider


class SoftSpider(Spider):
	name = 'app_360_search'
	allowed_domains = ['360.cn']
	url = 'http://zhushou.360.cn/search/index/?kw={}'
	id_url = 'http://zhushou.360.cn/detail/index/soft_id/{}'

	def __init__(self):
		self.rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

	def start_requests(self):
		# while True:
		# 	search_word = self.rc.rpop('360_word')
		# 	if not search_word:
		# 		raise CloseSpider('no datas')
			search_word = '水果泡泡'
			item = AppItem()
			item['search_word'] = search_word
			url = self.url.format(search_word)
			yield scrapy.Request(url, meta={'item': item, 'dont_redirect': True})

	def parse(self, response):
		# print(response.url)
		if '抱歉，没有找到与' in response.text:
			return
		select = Selector(text=response.text)
		ids = select.xpath('//div[@class="download comdown"]/a[position()<6]/@sid').extract()
		for id in ids:
			item = response.meta.get('item', '')
			# app_id = re.search(r'data\-(\d+)', id).group(1)
			print(id)
			item['app_id'] = id
			url = self.id_url.format(id)
			yield scrapy.Request(url, meta={'item': item, 'dont_redirect': True}, callback=self.parse_detail)

	def parse_detail(self, response):
		print(response.url)
		if '获取应用内容失败，请尝试ctrl+f5刷新' in response.text:
			return
		item = response.meta.get('item', '')
		pic = response.xpath('//*[@id="app-info-panel"]//dl[@class="clearfix"]/dt/img/@src').extract_first()
		name = response.xpath('//*[@id="app-name"]/span/@title').extract_first()
		official_tag = response.xpath('//cite[@class="verify_tag"]').extract_first()
		if official_tag:
			is_official = '是'
		else:
			is_official = '否'
		score = response.xpath('//span[@class="s-1 js-votepanel"]/text()').extract_first()

		span = response.xpath('//span[@class="s-3"]/text()').extract()
		down_num = span[0] if span and len(span) == 2 else ''
		size = span[1] if span and len(span) == 2 else ''

		remark = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/p/text()').extract_first()

		apk_url = response.xpath('//a[contains(@class, "js-downLog")]/@href').extract_first()
		if apk_url:
			pac_name1 = re.search(r'.+\/(.+?)\.apk$', apk_url)
			if pac_name1:
				pac_name = pac_name1.group(1)
			else:
				pac_name = ''
		else:
			pac_name1 = re.search(r"'pname': \"(.+?)\"", response.text)
			if pac_name1:
				pac_name = pac_name1.group(1)
			else:
				pac_name = ''

		# app_id = response.xpath('//a[contains(@class, "js-downLog")]/@data-sid').extract_first()

		cat = response.xpath('//li[@class="cur"]/a/@href').extract_first()
		if '/game/' == cat:
			app_cat = 'game'

		elif '/soft/' == cat:
			app_cat = 'soft'

		else:
			app_cat = ''

		des1 = response.xpath('//*[@id="html-brief"]/p/text()|//*[@id="sdesc"]/div[@class="breif"]/text()').extract()
		x = [d.strip() for d in des1]
		des = ''.join(x) if des1 else ''
		overview = str(response.xpath('//*[@id="html-brief"]//img/@src|//div[@class="overview"]/img/@src').extract())

		base_info = response.xpath('//div[@class="base-info"]/table/tbody/tr/td/text()').extract()
		auth = base_info[0] if base_info and len(base_info) == 5 else ''
		update_time = base_info[1] if base_info and len(base_info) == 5 else ''
		version = base_info[2] if base_info and len(base_info) == 5 else ''
		sys = base_info[3] if base_info and len(base_info) == 5 else ''
		lang = base_info[4] if base_info and len(base_info) == 5 else ''

		tag = str(response.xpath('//div[@class="app-tags"]/a/text()').extract())

		app_id = item['app_id']

		item['pic'] = pic
		item['soft_name'] = name
		item['is_official'] = is_official
		item['score'] = score
		item['down_num'] = down_num
		item['apk_size'] = size
		item['remark'] = remark
		item['pac_name'] = pac_name

		item['app_cat'] = app_cat
		item['des'] = des
		item['overview'] = overview
		item['auth'] = auth
		item['update_time'] = update_time
		item['version'] = version
		item['sys'] = sys
		item['lang'] = lang
		item['tag'] = tag

		baike_name1 = re.search(r"'baike_name': '(.+?)'", response.text)

		like_url = 'http://openbox.mobilem.360.cn/Guessyoulike/detail?callback=jQuery17205481610573495184_1502848421258&softId=%s&start=0&count=30' % app_id
		yield scrapy.Request(like_url, callback=self.parse_like,
		                     meta={'item': item, 'baike_name1': baike_name1})

	def parse_comm(self, response):
		item = response.meta.get('item', '')
		if not item:
			return

		j = json.loads(re.search(r'\((\{.+\}?)\)\;\}', response.text).group(1))

		comm_num = j.get('mesg', '')
		best_num = j.get('best', '')
		good_num = j.get('good', '')
		bad_num = j.get('bad', '')

		item['comm_num'] = comm_num
		item['best_num'] = best_num
		item['good_num'] = good_num
		item['bad_num'] = bad_num

		yield item

	def parse_like(self, response):
		item = response.meta.get('item', '')

		if not item:
			return
		j = json.loads(re.search(r'\((\{.+\})\)', response.body.decode('utf-8')).group(1))
		like_list = j.get('apps', [])
		likes = []
		for like in like_list:
			soft_id = like.get("soft_id", '')
			soft_name = like.get("soft_name", '')
			likes.append({"soft_id": soft_id, "soft_name": soft_name})
		item['likes'] = str(likes)

		baike_name1 = response.meta.get('baike_name1', '')
		if baike_name1:
			baike_name = quote_plus(baike_name1.group(1))
			comm_url = 'http://comment.mobilem.360.cn//comment/getLevelCount?callback=jQuery17206353542417695752_1502791914871&baike=%s&c=message&a=getmessagenum&_=%s' % (
				baike_name, int(time.time()) * 1000)
			yield scrapy.Request(comm_url, callback=self.parse_comm, meta={'item': item})
		else:
			yield item
