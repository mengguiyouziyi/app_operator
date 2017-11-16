# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from app.items import YYBItem
from app.utils.info import rc
from scrapy.exceptions import CloseSpider


class AppsSpider(scrapy.Spider):
	name = 'app_ybb'
	allowed_domains = ['sj.qq.com']
	start_url = 'http://sj.qq.com/myapp/searchAjax.htm?kw={}&pns=&sid='
	base_url = 'http://sj.qq.com/myapp/searchAjax.htm?kw='

	def start_requests(self):
		# x = 0
		# while True:
		# 	word_yyb = rc.rpop('word_yyb')
		# 	if not word_yyb:
		# 		x += 1
		# 		if x > 3:
		# 			raise CloseSpider('no datas')
		# 		time.sleep(60)
		# 		continue
			word_yyb = '百度魔图'
			url = self.start_url.format(word_yyb)
			yield scrapy.Request(url, meta={'chi': word_yyb})

	def parse(self, response):
		j = json.loads(response.text)
		if not j.get('success', ''):
			return
		obj = j.get('obj', {})
		items = obj.get('items', [])
		for ite in items:
			item = YYBItem()

			# apkMd5 = appDetail.get('apkMd5', '')
			appDetail = ite.get('appDetail', {})
			appId = appDetail.get('appId', '')
			iconUrl = appDetail.get('iconUrl', '')
			pkgName = appDetail.get('pkgName', )
			appName = appDetail.get('appName', '')
			flag = appDetail.get('flag', '')
			isGf = (flag >> (1 * 2)) & 3
			if isGf == 1:
				isOfficial = '是'
			elif isGf == 2:
				isOfficial = '否'
			else:
				isOfficial = '未知'

			appRatingInfo = appDetail.get('appRatingInfo', {})
			averageRating = appRatingInfo.get('averageRating', 0)
			ratingCount = appRatingInfo.get('ratingCount', 0)

			appDownCount = appDetail.get('appDownCount', '')
			fileSize = appDetail.get('fileSize', '')

			categoryId = appDetail.get('categoryId', '')
			categoryName = appDetail.get('categoryName', '')

			images = appDetail.get('images', [])
			# versionCode = appDetail.get('versionCode', '')
			versionName = appDetail.get('versionName', '')
			apkPublishTime = appDetail.get('apkPublishTime', '')

			authorId = appDetail.get('authorId', '')
			authorName = appDetail.get('authorName', '')

			description = appDetail.get('description', '')
			# newFeature = appDetail.get('newFeature', '')
			# editorIntro = appDetail.get('editorIntro', '')
			item['appId'] = appId
			item['iconUrl'] = iconUrl
			item['pkgName'] = pkgName
			item['appName'] = appName
			item['isOfficial'] = isOfficial
			item['averageRating'] = averageRating
			item['ratingCount'] = ratingCount
			item['appDownCount'] = appDownCount
			item['fileSize'] = fileSize
			item['categoryId'] = categoryId
			item['categoryName'] = categoryName
			item['images'] = str(images)
			item['versionName'] = versionName
			item['apkPublishTime'] = apkPublishTime
			item['authorId'] = authorId
			item['authorName'] = authorName
			item['description'] = description
			# apkUrl = appDetail.get('apkUrl', '')
			# http://sj.qq.com/myapp/detail.htm?apkName=com.qihoo360.mobilesafe
			detai_url = 'http://sj.qq.com/myapp/detail.htm?apkName=' + pkgName
			yield scrapy.Request(detai_url, callback=self.parse_detail, meta={'item': item})

		pageNumberStack = obj.get('pageNumberStack', '')
		hasNext = obj.get('hasNext', 0)
		if hasNext != 0:
			word_yyb = response.meta.get('chi', '')
			next_url = self.base_url + word_yyb + "&pns=" + pageNumberStack + '&sid=0'
			print(next_url)
			yield scrapy.Request(next_url, meta={'chi': word_yyb})

	def parse_detail(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		sameList = []
		same_tags = response.xpath('//a[@class="T_ComEventAppIns com-install-btn"]')
		for tag in same_tags:
			appName = tag.xpath('./@appname').extract_first()
			pkgName = tag.xpath('./@apk').extract_first()
			# http://pp.myapp.com/ma_icon/0/icon_10577594_1502939660/256
			iconUrl = tag.xpath('./@appicon').extract_first()
			appId_un = re.search(r'icon_(\d+?)_', iconUrl) if iconUrl else 0
			appId = appId_un.group(1) if appId_un else 0
			sameList.append({"appId": appId, "pkgName": pkgName, "appName": appName})
		item['sameList'] = str(sameList)
		yield item
