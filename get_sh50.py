# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-20 14:31:27
@LastEditors: HollisYu
@LastEditTime: 2019-11-21 19:39:05
'''
import pandas as pd
import os

res = {}
date_data = os.listdir("F:/Programming/Dataset/StockInformation/his_sh1_Day/")
for ind, d in enumerate(date_data):
    date_data[ind] = d[:-8]
    res[date_data[ind]] = []

with open("F:/Programming/Dataset/StockInformation/index_cons.txt") as f:
    # drop header
    line = f.readline()
    while line:
        line = f.readline()
        info = line.split("|")
        # only get sh_50(000016) info
        if info[0] != "000016":
            continue

        if info[3] == " ":
            info[3] = "20191008"
        for d in date_data:
            if d >= info[2] and d <= info[3]:
                res[d].append(info[1])

for key, value in res.items():
    with open("./sh_50/" + key + ".txt", 'w') as f:
        # print(key + " length: " + str(len(value)))
        write_down = str(value)[1:-1]
        write_down = write_down.replace('\'', '')
        write_down = write_down.replace(' ', '')
        f.write(write_down)