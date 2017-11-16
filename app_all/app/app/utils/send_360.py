# coding:utf-8

import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)

from app.utils.info import rc, etl


# def send_key(key):
# 	cursor = etl.cursor()
# 	sql = """select soft_id from 360app ORDER BY soft_id"""
# 	cursor.execute(sql)
# 	results = cursor.fetchall()
# 	values = [str(i['soft_id']) for i in results if i['soft_id']]
# 	if values:
# 		for value in values:
# 			rc.lpush(key, value)
# 			print(1)


if __name__ == '__main__':
	for i in range(4000000):
		rc.lpush('id_360', i)
		print(i)
