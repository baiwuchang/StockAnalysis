'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-10-22 10:31:57
@LastEditors: HollisYu
@LastEditTime: 2019-10-28 21:33:01
'''
# -*- coding:utf-8 -*-
import os

root_path = "F:/Programming/Dataset/StockInformation/"
output_file_path = root_path + "his_sh1_Day/"
input_file_path = root_path + "his_sh1_Day-backup/"

for csv in os.listdir(input_file_path):
    with open(input_file_path + csv, 'r') as input_file:
        index = 1
        with open(output_file_path + csv, 'w') as output_file:
            lines = input_file.readlines()
            for line in lines:
                if index == 1:
                    output_file.writelines("SecurityID,DateTime,PreClosePx,OpenPx,HighPx,LowPx,LastPx,Volume,Amount,IOPV,fp_Volume,fp_Amount\n")
                    index += 1
                else:
                    output_file.writelines(line)
    print(csv)