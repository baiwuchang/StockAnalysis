# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-20 14:31:27
@LastEditors: HollisYu
@LastEditTime: 2019-11-20 18:51:52
'''
import pandas as pd
import os

res = {}
# date_data = os.listdir("F:/Programming/Dataset/his_sh1_Day/")
date_data = os.listdir("D:/Files/Codes/Dataset/his_sh1_Day")
for ind, d in enumerate(date_data):
    date_data[ind] = d[:-8]
    res[date_data[ind]] = []
print(date_data)

with open("F:/Programming/Dataset/cons.txt") as f:
    line = f.readline()
    while line:
        info = line.split("|")

        for d in date_data:
            if d >= info[2] and d <= info[3]:
                res[d].append(info[1])

with open("F:/Programming/Dataset/sh_50.txt", 'w') as f:
    f.write(str(res))