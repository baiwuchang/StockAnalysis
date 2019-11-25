#找出所有可能会买到的股票（从sh_50中找出所有不重复的值，结果在all_sh50.txt中
#此文件理论上不需要再用

import pandas as pd
import numpy as np
import datetime
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
# local
import stock
import user
from numpy import loadtxt

file_path = r"./sh_50/"

stock_list = []

for f in os.listdir(file_path):
	#data = pd.read_txt(f, delimiter = ",")
	#print(data)
	file_name = f
	all_path = file_path + file_name
	data = loadtxt(all_path, delimiter = ",")
	for i in data:
		if i not in stock_list:
			stock_list.append(i)

stock_list2 = []
for i in stock_list:
	stock_list2.append(int(i))
print(stock_list2)
print(len(stock_list))