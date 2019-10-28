'''
@Description: This module is to plot the stock data
@Author: HollisYu
@Date: 2019-10-19 10:55:15
@LastEditors: HollisYu
@LastEditTime: 2019-10-29 00:45:33
'''
# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_finance as mpf

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'SimHei'
pd.set_option('display.float_format',lambda x : '%.3f' % x)

data_file = "F:/Programming/Dataset/StockInformation/sh1_each_stock_data/ID_1_Day.csv"
csv_data = pd.read_csv(data_file)

# Cal average means
csv_data['Mean5'] = csv_data.LastPx.rolling(5).mean()
csv_data['Mean10'] = csv_data.LastPx.rolling(10).mean()
csv_data['Mean30'] = csv_data.LastPx.rolling(30).mean()

# Control the subplots
figure = plt.figure(figsize=(16, 9))
ax1 = figure.add_axes([0.1, 0.3, 0.8, 0.6])
ax2 = figure.add_axes([0.1, 0.1, 0.8, 0.2], sharex=ax1)

# plot Candlestick chart
mpf.candlestick2_ohlc(ax1, csv_data['OpenPx'], csv_data['HighPx'], csv_data['LowPx'], csv_data['LastPx'], width=0.7, colorup='r', colordown='g', alpha=0.7)
# plot average mean
for ma in ['Mean5', 'Mean10', 'Mean30']:
    ax1.plot(csv_data[ma], label=ma)
# set ax1 settings
ax1.legend(loc='upper left')
ax1.grid(True)
ax1.set_title('上证综指K线图(2014.1.2-2019.10.8)', fontsize=20)
ax1.set_ylabel('指数')

# plot Volume chart
mpf.volume_overlay(ax2, csv_data['OpenPx'], csv_data['LastPx'], csv_data['Volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
# set ax1 settings
ax2.set_xticks(range(0, len(csv_data['DateTime']), 10))
ax2.set_xticklabels(csv_data['DateTime'][::10], rotation=45)
ax2.grid(True)
ax2.set_ylabel('成交量')
ax2.set_ylim(ymin=0)

# show the result
plt.show()