# coding:utf-8

import os
import sys
import pymysql
import time
from os.path import dirname

from my_redis import QueueRedis

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)

from app_all.app.app.utils.info import rc, etl


def send_key(key):
	cursor = etl.cursor()
	sql = """select soft_name from hw_app ORDER BY soft_id"""
	cursor.execute(sql)
	results = cursor.fetchall()
	values = [i['com_name'].strip() for i in results]
	if values:
		for value in values:
			rc.lpush(key, value)
			print(1)


if __name__ == '__main__':
	send_key(key='word_yyb')
