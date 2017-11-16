# -*- coding: utf-8 -*-
import re
import json
import scrapy
import time
from urllib.parse import quote_plus
from datetime import datetime
from scrapy.spiders import Spider
from app.items import AppItem
from app.utils.info import rc
from scrapy.exceptions import CloseSpider


class SoftSpider(Spider):
	name = 'app_360'
	allowed_domains = ['360.cn']
	url = 'http://zhushou.360.cn/detail/index/soft_id/{}'

	def start_requests(self):
		app_ids = ['1','2', '1', '2','3', '4']
		for app_id in app_ids:
		# x = 0
		# while True:
		# 	app_id = rc.rpop('id_360')
		# 	if not app_id:
		# 		x += 1
		# 		if x > 3:
		# 			raise CloseSpider('no datas')
		# 		time.sleep(60)
		# 		continue
			app_item = AppItem()
			app_item['app_id'] = app_id
			url = self.url.format(app_id)
			yield scrapy.Request(url, meta={'app_item': app_item, 'dont_redirect': True})

	def parse(self, response):
		if '获取应用内容失败，请尝试ctrl+f5刷新' in response.text:
			return
		app_item = response.meta.get('app_item', '')
		if not app_item:
			return
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

		app_id = app_item['app_id']

		app_item['pic'] = pic
		app_item['soft_name'] = name
		app_item['is_official'] = is_official
		app_item['score'] = score
		app_item['down_num'] = down_num
		app_item['apk_size'] = size
		app_item['remark'] = remark
		app_item['pac_name'] = pac_name

		app_item['app_cat'] = app_cat
		app_item['des'] = des
		app_item['overview'] = overview
		app_item['auth'] = auth
		app_item['update_time'] = update_time
		app_item['version'] = version
		app_item['sys'] = sys
		app_item['lang'] = lang
		app_item['tag'] = tag

		baike_name1 = re.search(r"'baike_name': '(.+?)'", response.text)

		like_url = 'http://openbox.mobilem.360.cn/Guessyoulike/detail?callback=jQuery17205481610573495184_1502848421258&softId=%s&start=0&count=30' % app_id
		yield scrapy.Request(like_url, callback=self.parse_like,
		                     meta={'app_item': app_item, 'baike_name1': baike_name1})

	def parse_comm(self, response):
		app_item = response.meta.get('app_item', '')
		if not app_item:
			return

		j = json.loads(re.search(r'\((\{.+\}?)\)\;\}', response.text).group(1))

		comm_num = j.get('mesg', '')
		best_num = j.get('best', '')
		good_num = j.get('good', '')
		bad_num = j.get('bad', '')

		app_item['comm_num'] = comm_num
		app_item['best_num'] = best_num
		app_item['good_num'] = good_num
		app_item['bad_num'] = bad_num

		yield app_item

	def parse_like(self, response):
		app_item = response.meta.get('app_item', '')

		if not app_item:
			return
		j = json.loads(re.search(r'\((\{.+\})\)', response.body.decode('utf-8')).group(1))
		like_list = j.get('apps', [])
		likes = []
		for like in like_list:
			soft_id = like.get("soft_id", '')
			soft_name = like.get("soft_name", '')
			likes.append({"soft_id": soft_id, "soft_name": soft_name})
		app_item['likes'] = str(likes)

		baike_name1 = response.meta.get('baike_name1', '')
		if baike_name1:
			baike_name = quote_plus(baike_name1.group(1))
			comm_url = 'http://comment.mobilem.360.cn//comment/getLevelCount?callback=jQuery17206353542417695752_1502791914871&baike=%s&c=message&a=getmessagenum&_=%s' % (
				baike_name, int(time.time()) * 1000)
			yield scrapy.Request(comm_url, callback=self.parse_comm, meta={'app_item': app_item})
		else:
			yield app_item
