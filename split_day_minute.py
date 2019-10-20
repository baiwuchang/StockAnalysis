'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-10-20 09:41:19
@LastEditors: HollisYu
@LastEditTime: 2019-10-20 10:21:22
'''
# -*- coding:utf-8 -*-
import os
import shutil

# file settings
root_path = "F:/Programming/Dataset/StockInformation/"
file_path = root_path + "his_sh1/"
day_file_name = "Day.csv"
minute_file_name = "Minute.csv"
result_day_path = root_path + "his_sh1_Day/"
if not os.path.exists(result_day_path):
    os.makedirs(result_day_path)
result_minute_path = root_path + "his_sh1_Minute/"
if not os.path.exists(result_minute_path):
    os.makedirs(result_minute_path)

# iterate the dir and copy data file to different result dir
for f in os.listdir(file_path):
    print("file dir: ", f)
    # split the day and minute data
    if os.path.exists(file_path + f + "/" + day_file_name):
        shutil.copy(file_path + f + "/" + day_file_name, result_day_path)
        os.rename(result_day_path + day_file_name, result_day_path + f + "_" + day_file_name)
    if os.path.exists(file_path + f + "/" + minute_file_name):
        shutil.copy(file_path + f + "/" + minute_file_name, result_minute_path)
        os.rename(result_minute_path + minute_file_name, result_minute_path + f + "_" + minute_file_name)