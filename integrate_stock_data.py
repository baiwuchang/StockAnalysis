'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-10-19 12:44:35
@LastEditors: HollisYu
@LastEditTime: 2019-10-22 18:36:34
'''
# -*- coding:utf-8 -*-
import pandas as pd
import os

# basic file settings
root_path = "F:/Programming/Dataset/StockInformation/"
file_path = root_path + "his_sh1_Day/"
result_path = root_path + "sh1_each_stock_data/"
if not os.path.exists(result_path):
    os.mkdir(result_path)
# data settings
data_header = ["SecurityID", "DateTime", "PreClosePx", "OpenPx", "HighPx", "LowPx", "LastPx", "Volume", "Amount", "IOPV", "fp_Volume", "fp_Amount"]

csv_data = pd.read_csv(file_path + "20140102_Day.csv")
id_list = list(csv_data["SecurityID"])

file_list = os.listdir(file_path)
file_list.sort()
for stock_id in id_list:
    one_stock_data = pd.DataFrame(columns=data_header)
    for f in file_list:
        csv_data = pd.read_csv(file_path + f)
        csv_data.set_index("SecurityID", drop=False, inplace=True)
        if stock_id in csv_data.index:
            line = csv_data.loc[stock_id]
            one_stock_data = one_stock_data.append(line, ignore_index=True)
        # else:
            # print("No index {} in {}".format(stock_id, f))
    
    file_name = "ID_" + str(stock_id) + "_Day.csv"
    one_stock_data.to_csv(result_path + file_name, index=False, header=True)
    # print("Write to csv: ", file_name)
