# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-26 13:24:59
@LastEditors  : HollisYu
@LastEditTime : 2019-12-19 09:53:59
'''
import os
import pandas as pd
# import talib

# def cal_MACD(stock_id: str):
#     file_path = './sh1_each_stock_data/'
#     file_name = file_path + 'ID_' + stock_id + '_Day.csv'
#     if not os.path.exists(file_name):
#         return None
#     stock_data = pd.read_csv(file_name)
#     # cal MACD
#     stock_data['EMA12'] = stock_data['LastPx'].ewm(span=12).mean()
#     stock_data['EMA26'] = stock_data['LastPx'].ewm(span=26).mean()
#     stock_data['DIF'] = stock_data['EMA12'] - stock_data['EMA26']
#     stock_data['DEA'] = stock_data['DIF'].ewm(span=9).mean()
#     stock_data['MACD'] = (stock_data['DIF'] - stock_data['DEA']) * 2
    
#     # using talib # not very good
#     # stock_data['SEMA'] = talib.EMA(stock_data['LastPx'].values, timeperiod=12)
#     # stock_data['LEMA'] = talib.EMA(stock_data['LastPx'].values, timeperiod=26)
#     # stock_data['DIF'], stock_data['DEA'], stock_data['MACD/2'] = talib.MACD(stock_data['LastPx'].values, fastperiod=12, slowperiod=26, signalperiod=9)

#     return stock_data

file_path = "./sh1_each_stock_data-bak/"
result_path = "./sh1_each_stock_data2/"
if not os.path.exists(result_path):
    os.mkdir(result_path)

files = os.listdir(file_path)
for f in files:
    stock_data = pd.read_csv(file_path + f)
    # cal MACD
    stock_data['EMA12'] = stock_data['LastPx'].ewm(span=12).mean()
    stock_data['EMA26'] = stock_data['LastPx'].ewm(span=26).mean()
    stock_data['DIF'] = stock_data['EMA12'] - stock_data['EMA26']
    stock_data['DEA'] = stock_data['DIF'].ewm(span=9).mean()
    stock_data['MACD'] = (stock_data['DIF'] - stock_data['DEA']) * 2

    # cal KDJ
    low = stock_data['LowPx'].rolling(9).min()
    high = stock_data['HighPx'].rolling(9).max()

    rsv = (stock_data['LastPx'] - low) / (high - low) * 100
    stock_data['K'] = rsv.ewm(com=2).mean()
    stock_data['D'] = stock_data['K'].ewm(com=2).mean()
    stock_data['J'] = 3 * stock_data['K'] - 2 * stock_data['D']
    

    stock_data.to_csv(result_path + f, index=False, header=True)

