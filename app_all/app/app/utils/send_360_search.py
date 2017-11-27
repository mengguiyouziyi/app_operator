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

from rediscluster import StrictRedisCluster
from app.utils.info import startup_nodes, etl


def send_key(key):
	rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
	cursor = etl.cursor()
	sql = """select comp_name from app_five"""
	cursor.execute(sql)
	results = cursor.fetchall()
	values = [i['comp_name'] for i in results if i['comp_name']]
	for value in values:
		rc.lpush(key, value)


if __name__ == '__main__':
	send_key('360_word')
	print('done')
