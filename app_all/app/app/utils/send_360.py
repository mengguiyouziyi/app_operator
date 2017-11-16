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

from app_all.app.app.utils.info import rc

if __name__ == '__main__':
	for i in range(4000000):
		rc.lpush('id_360', i)
