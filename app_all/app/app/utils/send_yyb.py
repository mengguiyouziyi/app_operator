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


def send_key(key):
	cursor = etl.cursor()
	sql = """select soft_name from hw_app ORDER BY soft_id"""
	cursor.execute(sql)
	results = cursor.fetchall()
	values = [result['com_name'].strip() for result in results]
	if values:
		for i, value in enumerate(values):
			rc.lpush(key, value)
			print(i)


if __name__ == '__main__':
	send_key(key='word_yyb')
