# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
	search_word = scrapy.Field()
	pic = scrapy.Field()
	soft_name = scrapy.Field()
	is_official = scrapy.Field()
	score = scrapy.Field()
	down_num = scrapy.Field()
	apk_size = scrapy.Field()
	remark = scrapy.Field()
	pac_name = scrapy.Field()
	app_id = scrapy.Field()
	app_cat = scrapy.Field()
	des = scrapy.Field()
	overview = scrapy.Field()
	auth = scrapy.Field()
	update_time = scrapy.Field()
	version = scrapy.Field()
	sys = scrapy.Field()
	lang = scrapy.Field()
	tag = scrapy.Field()
	likes = scrapy.Field()

	comm_num = scrapy.Field()
	best_num = scrapy.Field()
	good_num = scrapy.Field()
	bad_num = scrapy.Field()


# class LikeItem(scrapy.Item):
# 	app_id = scrapy.Field()
#
# 	soft_id = scrapy.Field()
# 	pname = scrapy.Field()
# 	soft_name = scrapy.Field()
# 	download_urls = scrapy.Field()
# 	download_times = scrapy.Field()
# 	apk_sizes = scrapy.Field()
# 	logo_url = scrapy.Field()
# 	vote_scores = scrapy.Field()
# 	rate = scrapy.Field()
# 	apk_md5 = scrapy.Field()
# 	cnxhtype = scrapy.Field()
# 	app_cat = scrapy.Field()
# 	diadian = scrapy.Field()
# 	soft_sub_name = scrapy.Field()
# 	origin = scrapy.Field()


class HwItem(scrapy.Item):
	soft_id = scrapy.Field()
	logo_url = scrapy.Field()
	soft_name = scrapy.Field()
	pname = scrapy.Field()
	down_num = scrapy.Field()
	soft_score = scrapy.Field()
	soft_size = scrapy.Field()
	create_date = scrapy.Field()
	auth = scrapy.Field()
	version = scrapy.Field()
	pic_url = scrapy.Field()
	des = scrapy.Field()
	comm_num = scrapy.Field()


class YYBItem(scrapy.Item):
	appId = scrapy.Field()
	iconUrl = scrapy.Field()
	pkgName = scrapy.Field()
	appName = scrapy.Field()
	isOfficial = scrapy.Field()
	averageRating = scrapy.Field()
	ratingCount = scrapy.Field()
	appDownCount = scrapy.Field()
	fileSize = scrapy.Field()
	categoryId = scrapy.Field()
	categoryName = scrapy.Field()
	images = scrapy.Field()
	versionName = scrapy.Field()
	apkPublishTime = scrapy.Field()
	authorId = scrapy.Field()
	authorName = scrapy.Field()
	description = scrapy.Field()
	sameList = scrapy.Field()
