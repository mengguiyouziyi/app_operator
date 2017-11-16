# -*- coding: utf-8 -*-
import scrapy
import re
import time
from app.items import HwItem
from app.utils.info import rc
from scrapy.exceptions import CloseSpider


class AppsSpider(scrapy.Spider):
	name = 'app_hw'
	allowed_domains = ['appstore.huawei.com']
	start_url = 'http://appstore.huawei.com/app/C{}'

	def start_requests(self):
		# x = 0
		# while True:
		# 	id_hw = rc.rpop('id_hw')
		# 	if not id_hw:
		# 		x += 1
		# 		if x > 3:
		# 			raise CloseSpider('no datas')
		# 		time.sleep(60)
		# 		continue
			id_hw = '290'
			url = self.start_url.format(id_hw)
			yield scrapy.Request(url)

	def parse(self, response):
		# print(response.url)
		if '抱歉，找不到您要的页' in response.text or '对不起！没有您要的数据！' in response.text:
			return
		item = HwItem()
		x = re.search(r'/C(\d+)$', response.url)
		soft_id = int(x.group(1)) if x else -1
		logo_url = response.xpath('//img[@class="app-ico"]/@src').extract_first()
		soft_name = response.xpath(
			'//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first()
		dlurl = response.xpath('//a[@class="mkapp-btn mab-install"]/@dlurl').extract_first()
		pname = re.search(r'/([^/]+?)\.apk', dlurl).group(1) if dlurl else ''
		down_num = response.xpath(
			'//ul[@class="app-info-ul nofloat"]/li/p/span[@class="grey sub"]/text()').extract_first()
		soft_score_un = response.xpath(
			'//ul[@class="app-info-ul nofloat"]/li/p/span[starts-with(@class, "score")]/@class').extract_first()
		soft_score = soft_score_un.replace('score_', '') if soft_score_un else ''

		li = response.xpath('//li[@class="ul-li-detail"]/span/text()').extract()
		soft_size = li[0] if len(li) == 4 else ''
		create_date = li[1] if len(li) == 4 else ''
		l = response.xpath('//li[@class="ul-li-detail"]')
		auth = l[2].xpath('./span/@title').extract_first() if len(li) == 4 else ''
		version = li[3] if len(li) == 4 else ''

		pic_url = response.xpath('.//*[@id="contentImages"]/ul/li/a/img[@class="showimg"]/@src').extract()
		des_list = response.xpath(".//*[@id='app_strdesc']/text()").extract()
		des = ''.join(des_list) if des_list else ''
		comm_word = response.xpath(".//*[@id='commentForm']/h4/span/text()").extract_first()
		s = re.search(r'\d+', comm_word) if comm_word else ''
		comm_num = s.group() if s else ''

		item['soft_id'] = soft_id
		item['logo_url'] = logo_url
		item['soft_name'] = soft_name
		item['pname'] = pname
		item['down_num'] = down_num
		item['soft_score'] = soft_score
		item['soft_size'] = soft_size
		item['create_date'] = create_date
		item['auth'] = auth
		item['version'] = version
		item['pic_url'] = str(pic_url) if pic_url else ''
		item['des'] = des
		item['comm_num'] = comm_num
		yield item
