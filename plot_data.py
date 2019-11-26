'''
@Description: This module is to plot the stock data
@Author: HollisYu
@Date: 2019-10-19 10:55:15
@LastEditors: HollisYu
@LastEditTime: 2019-11-26 23:16:19
'''
# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

pd.set_option('display.float_format',lambda x : '%.3f' % x)

data_file = "./sh1_each_stock_data/ID_1_Day.csv"
csv_data = pd.read_csv(data_file)

# Cal average means
# csv_data['Mean5'] = csv_data.LastPx.rolling(5).mean()
# csv_data['Mean10'] = csv_data.LastPx.rolling(10).mean()
# csv_data['Mean30'] = csv_data.LastPx.rolling(30).mean()

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

# plot MACD
fig3, ax3 = plt.subplots()
ax3.plot(csv_data['DIF'], label='DIF')
ax3.plot(csv_data['DEA'], label='DEA')

ax4 = ax3.twinx()
ax4.bar(csv_data.shape[0], csv_data['MACD'].values, width=0.3, color=['r' if csv_data.MACD[x] > 0 else 'g' for x in range(csv_data.shape[0])])

ax3.legend(loc='upper left')
ax3.grid(True)
ax3.set_title('股票MACD走势', fontsize=20)
ax3.set_xlabel('交易日期')
ax3.set_xticks(range(0, len(csv_data['DateTime']), 10))
ax3.set_xticklabels(csv_data['DateTime'][::10], rotation=45)
ax3.set_ylabel('MACD')

# show the result
plt.show()