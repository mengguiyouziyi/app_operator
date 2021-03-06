# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import CloseSpider
from app.utils.info import etl


class MysqlPipeline(object):
	def __init__(self):
		self.conn = etl
		self.cursor = self.conn.cursor()
		self.col_list = self._get_column('app_360_five')[1:-1]
		self.col_str = ','.join(self.col_list)
		self.val_str = self._handle_str(len(self.col_list))

	def process_item(self, item, spider):
		sql = """insert into app_360_five ({col}) VALUES ({val})""".format(col=self.col_str, val=self.val_str)
		args = [item[i] for i in self.col_list]
		try:
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['app_id'])
		except Exception as e:
			print(e)
			raise CloseSpider('mysql insert error.....')

	def _get_column(self, tab):
		sql = """select group_concat(column_name) from information_schema.columns WHERE table_name = '{tab}' and table_schema = 'spider'""".format(
			tab=tab)
		try:
			self.cursor.execute(sql)
		except Exception as e:
			print(e)
			raise CloseSpider('获取数据表字段错误....')
		results = self.cursor.fetchall()
		col_str = results[0]['group_concat(column_name)']
		col_list = col_str.split(',')
		return col_list

	def _handle_str(self, num):
		x = "%s"
		y = ", %s"
		for i in range(num - 1):
			x += y
		return x

	# id = ''
	# if isinstance(item, AppItem):
	# 	sql = """insert into app_360_update(pic, soft_name, is_official, score, down_num, apk_size, remark, pac_name, app_id, app_cat, des, overview, auth, update_time, version, sys, lang, tag, likes, comm_num, best_num, good_num, bad_num) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	# 	args = (
	# 		item['pic'], item['soft_name'], item['is_official'], item['score'], item['down_num'], item['apk_size'],
	# 		item['remark'], item['pac_name'], item['app_id'], item['app_cat'], item['des'], item['overview'],
	# 		item['auth'], item['update_time'], item['version'], item['sys'], item['lang'], item['tag'],
	# 		item['likes'], item['comm_num'], item['best_num'], item['good_num'], item['bad_num']
	# 	)
	# 	id = item['app_id']
	# # elif isinstance(item, LikeItem):
	# # 	sql = """replace into 360app_like(app_id, soft_id, pname, soft_name, download_urls, download_times, apk_sizes, logo_url, vote_scores, rate, apk_md5, cnxhtype, app_cat, diadian, soft_sub_name, origin) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	# # 	args = (item["app_id"], item["soft_id"], item["pname"], item["soft_name"], item["download_urls"],
	# # 	        item["download_times"], item["apk_sizes"], item["logo_url"], item["vote_scores"], item["rate"],
	# # 	        item["apk_md5"], item["cnxhtype"], item["app_cat"], item["diadian"], item["soft_sub_name"],
	# # 	        item["origin"])
	# elif isinstance(item, HwItem):
	# 	sql = """insert into app_hw_update(soft_id, logo_url, soft_name, pname, down_num, soft_score, soft_size, create_date, auth, version, pic_url, des, comm_num) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	# 	args = (
	# 		item['soft_id'], item['logo_url'], item['soft_name'], item['pname'], item['down_num'],
	# 		item['soft_score'], item['soft_size'], item['create_date'], item['auth'], item['version'],
	# 		item['pic_url'], item['des'], item['comm_num']
	# 	)
	# 	id = item['soft_id']
	# elif isinstance(item, YYBItem):
	# 	sql = """insert into app_yyb_update(appId, iconUrl, pkgName, appName, isOfficial, averageRating, ratingCount, appDownCount, fileSize, categoryId, categoryName, images, versionName, apkPublishTime, authorId, authorName, description, sameList) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	# 	args = (
	# 		item['appId'], item['iconUrl'], item['pkgName'], item['appName'], item['isOfficial'],
	# 		item['averageRating'], item['ratingCount'], item['appDownCount'], item['fileSize'], item['categoryId'],
	# 		item['categoryName'], item['images'], item['versionName'], item['apkPublishTime'], item['authorId'],
	# 		item['authorName'], item['description'], item['sameList']
	# 	)
	# 	id = item['appId']
	# self.cursor.execute(sql, args=args)
	# self.conn.commit()
	# print(id)
	#
