'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-10-19 12:44:35
@LastEditors: HollisYu
@LastEditTime: 2019-10-20 12:24:35
'''
# -*- coding:utf-8 -*-
import pandas as pd
import os

# basic file settings
root_path = "F:/Programming/Dataset/StockInformation/"
file_path = root_path + "his_sh1_Day/"
result_path = root_path + "sh1_each_stock_data/"
file_name = "Day.csv"
# data settings
data_header = ["SecurityID", "DateTime", "PreClosePx", "OpenPx", "HighPx", "LowPx", "LastPx", "Volume", "Amount", "IOPV"]

csv_data = pd.read_csv(file_path + "20140102_" + file_name, header=0, names=data_header, dtype=str)
one_stock_data = pd.DataFrame(columns = data_header)
id_list = list(csv_data["SecurityID"])

# one_stock_data = one_stock_data.append(line, ignore_index=True)
# print(one_stock_data)

file_list = os.listdir(file_path)
file_list.sort()

for index in id_list:
    one_stock_data = pd.DataFrame()
    for f in file_list:
        print(f)
        csv_data = pd.read_csv(file_path + f, header=0, names=data_header, dtype=str)
