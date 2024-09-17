# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-13 14:02:47
@LastEditors  : HollisYu
@LastEditTime : 2019-12-24 19:08:22
'''
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
# local
import stock
import user
from numpy import loadtxt
import copy

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus']=False

stock_set = loadtxt('all_sh50.txt', delimiter = ",")
stock_set = list(stock_set)
for i in range(len(stock_set)):
	stock_set[i] = str((int(stock_set[i])))

def get_sh50_info(date: str) -> list:
	file_path = "./sh_50/"
	file_name = file_path + date + '.txt'
	sh_50 = []
	# no data, skip
	if not os.path.exists(file_name):
		return sh_50

	with open(file_name) as f:
		line = f.readline()
		sh_50 = line.split(',')
	
	return sh_50

def float_to_color(a:float):
	#把float转化为一个红绿渐变间的数字，a从0到1,1最红,0最绿
	r = int(a * 255)
	g = int((1 - a) * 175)
	rgb = [r,g,25]
	strs = '#'
	for i in rgb:
		strs += str(hex(i))[-2:].replace('x','0').upper()#将R、G、B分别转化为16进制拼接转换并大写	
	return strs

def check(stock_id: str, csv_data, date, op_type: str) -> bool:

	if date.strftime("%Y-%m-%d") not in csv_data.index:
		return False
	day_data = csv_data.loc[date.strftime("%Y-%m-%d")]
	# Volume is 0, cannot do anything
	if day_data['Volume'] == 0:
		return False
	pre_date = date - datetime.timedelta(days=1)
	while pre_date.weekday() >= 5 or pre_date.strftime("%Y-%m-%d") not in csv_data.index:
		pre_date -= datetime.timedelta(days=1)
	pre_data = csv_data.loc[pre_date.strftime("%Y-%m-%d")]

	# if is selling
	if op_type == "sell":
		# if day_data['Mean10'] <= day_data['Mean30'] and day_data['Mean5'] < day_data['Mean30']:
		if day_data['MACD'] <= 0 and day_data['DIF'] < 0 and day_data['DEA'] < 0 and pre_data['MACD'] > 0:
			return True
		else:
			return False

	#if is buying
	else:
		# if day_data['Mean10'] >= day_data['Mean30'] and day_data['Mean5'] > day_data['Mean30']:
		if day_data['MACD'] >= 0 and day_data['DIF'] > 0 and day_data['DEA'] > 0 and pre_data['MACD'] < 0:
			return True
		else:
			return False


def strategy(account, start_date, end_date):
	#画甘特图需要的
	gantt_data = []
	gantt_data_everyday = [0] * 97 #某天是否持有某个股票
	#画甘特图需要的-结束

	# use data cols
	use_headers = ['DateTime', 'LastPx', 'Volume', 'DIF', 'DEA', 'MACD', 'K', 'D', 'J']

	date = start_date
	sh_50 = []
	with open('./today_sh50.txt') as f:
		line = f.readline()
		sh_50 = line.split(',')

	file_path = "./sh1_each_stock_data2/"
	money_records = pd.DataFrame(columns=['DateTime', 'TotalMoney', 'Cash', 'Stocks', 'Compare'])
	stock_records = pd.DataFrame(columns=['DateTime'] + stock_set)

	# compare account
	compare_account = user.User(account.total_value)
	compare_buy = False
	compare_id = '1'

	# up signal valid
	up_signal_valid = 3
	up_signal_stocks = {}
	
	while date <= end_date:
		if date.weekday() < 5:  # if it's Saturday or Sunday, skip
			# get sh_50 stocks
			# sh_50 = get_sh50_info(date.strftime("%Y%m%d"))
			dt = date.strftime("%Y-%m-%d")
			# compare accounts buy or update
			compare_data = pd.read_csv(file_path + 'ID_' + compare_id + '_Day.csv', usecols=use_headers)
			compare_data.set_index('DateTime', drop=False, inplace=True)
			if dt in compare_data.index:
				compare_today_data = compare_data.loc[dt]
				if not compare_buy:
					compare_account.buy_stock(compare_id, compare_today_data['LastPx'], compare_account.total_value)
					compare_buy = True
				else:
					compare_account.update_stock(compare_id, compare_today_data['LastPx'])
			
			if sh_50:   # if no sh_50 data, maybe a holiday, skip
				# first sell stocks which are down, also update prices
				temp_sell = []  # store selling stocks temperly
				for stock_id in account.buy_in_stocks:
					# open data file
					file_name = file_path + "ID_" + stock_id + "_Day.csv"
					# if data not exists, skip
					if not os.path.exists(file_name):
						continue
					stock_data = pd.read_csv(file_name, usecols=use_headers)
					stock_data.set_index('DateTime', drop=False, inplace=True)
					# get today data line
					# if data not exists, skip
					if dt not in stock_data.index:
						continue
					today_data = stock_data.loc[dt]
					# update value
					account.update_stock(stock_id, today_data['LastPx'])

					# check whether to sell the stock
					sell_flag = check(stock_id, stock_data, date, "sell")
					# check if benefit is enough or down
					profit = account.buy_in_stocks[stock_id].profit
					# stock down, sell all
					if sell_flag or profit >= 0.2:	#  or profit <= -0.1
						temp_sell.append(stock_id)
						gantt_data_everyday[stock_set.index(stock_id)] = 0 #甘特图需要
					
				# get all selling stocks and then sell them
				for stock_id in temp_sell:
					account.sell_stock(stock_id)
					print("Sell stock: {} on {}".format(stock_id, dt))

				# temp_expired = []
				# for stock_id in up_signal_stocks:
				# 	up_signal_stocks[stock_id] -= 1
				# 	if up_signal_stocks[stock_id] == 0:
				# 		temp_expired.append(stock_id)

				# for stock_id in temp_expired:
				# 	del up_signal_stocks[stock_id]
				# 	print("Up signal for {} expired.".format(stock_id))

				# check if there have place to buy stocks
				if len(account.buy_in_stocks) < account.max_number:
					for stock_id in sh_50:
						# already have, continue to next one
						if stock_id in account.buy_in_stocks:
							continue

						# open data file
						file_name = file_path + "ID_" + stock_id + "_Day.csv"
						# if data not exists, skip
						if not os.path.exists(file_name):
							continue
						stock_data = pd.read_csv(file_name, usecols=use_headers)
						stock_data.set_index('DateTime', drop=False, inplace=True)
						# get today data line
						# if data not exists, skip
						if dt not in stock_data.index:
							continue
						today_data = stock_data.loc[dt]

						# check whether to buy the stock
						buy_flag = check(stock_id, stock_data, date, "buy")
						if buy_flag:
							# buy no more than threshold or money have
							money = min(account.up_threshold, account.money)
							account.buy_stock(stock_id, today_data['LastPx'], money)
							print("Buy stock: {} on {}, price {}".format(stock_id, dt, today_data['LastPx']))

							gantt_data_everyday[stock_set.index(stock_id)] = float(today_data['LastPx']) #甘特图需要

							# if already have 10 stocks, stop buying
							if len(account.buy_in_stocks) >= account.max_number:
								break
							# up_signal_stocks[stock_id] = 3
			for stock_id in sh_50:
				# open data file
				file_name = file_path + "ID_" + stock_id + "_Day.csv"
				# if data not exists, skip
				if not os.path.exists(file_name):
					continue
				stock_data = pd.read_csv(file_name, usecols=use_headers)
				stock_data.set_index('DateTime', drop=False, inplace=True)
				# get today data line
				# if data not exists, skip
				if dt not in stock_data.index:
					continue
				today_data = stock_data.loc[dt]

				if not gantt_data_everyday[stock_set.index(stock_id)] == 0:
					gantt_data_everyday[stock_set.index(stock_id)] = float(today_data['LastPx']) #甘特图需要


					# for stock_id in up_signal_stocks:
					# 	# open data file
					# 	file_name = file_path + "ID_" + stock_id + "_Day.csv"
					# 	# if data not exists, skip
					# 	if not os.path.exists(file_name):
					# 		continue
					# 	stock_data = pd.read_csv(file_name, usecols=use_headers)
					# 	stock_data.set_index('DateTime', drop=False, inplace=True)
					# 	# get today data line
					# 	# if data not exists, skip
					# 	if dt not in stock_data.index:
					# 		continue
					# 	today_data = stock_data.loc[dt]
					# 	# buy no more than threshold or money have
					# 	money = min(account.up_threshold, account.money)
					# 	account.buy_stock(stock_id, today_data['LastPx'], money)
					# 	print("Buy stock: {} on {}".format(stock_id, dt))

					# 	gantt_data_everyday[stock_set.index(stock_id)] = 1 #甘特图需要

					# 	# if already have 10 stocks, stop buying
					# 	if len(account.buy_in_stocks) >= account.max_number:
					# 		break

		# record account money change and buy-sell records
		record = pd.DataFrame([[date.strftime("%Y-%m-%d"), account.total_value, account.money, account.total_value - account.money, compare_account.total_value]], columns=['DateTime', 'TotalMoney', 'Cash', 'Stocks', 'Compare'])
		money_records = money_records.append(record, ignore_index=True)
		record_for_gantt = pd.DataFrame([[date.strftime("%Y-%m-%d")] + gantt_data_everyday], columns=['DateTime'] + stock_set)
		stock_records = stock_records.append(record_for_gantt, ignore_index = True)
		# add one day
		date += datetime.timedelta(days=1)
	
	return money_records, stock_records

def run_strategy(start_date: str, end_date: str):
	start_money = 2000000.0
	#封装main里面的函数，给前端调用
	my_account = user.User(start_money)
	start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
	end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
	result, stock_records = strategy(my_account, start_date, end_date)

	# cal alpha rate
	last_record = result.iloc[-1]
	alpha = (last_record['TotalMoney'] - last_record['Compare']) / start_money
	print("Alpha rate is: {}".format(alpha))

	#画账户变化图
	fig, ax = plt.subplots()
	# for label in ['TotalMoney', 'Cash', 'Stocks', 'Compare']: 
	for label in ['TotalMoney', 'Compare']:
		ax.plot(result[label], label=label)
	ax.set_title('趋势跟随策略下的账户变化', fontsize=20)
	ax.set_xlabel('交易日期')
	ax.set_xticks(range(0, len(result['DateTime']), 10))
	ax.set_xticklabels(result['DateTime'][::10], rotation=45)
	ax.set_ylabel('金额(元)')
	ax.legend(loc='upper left')
	ax.grid(True)

	#先把没买过的的股票删掉
	tmp_stock_set = copy.deepcopy(stock_set)

	for i in reversed(range(len(tmp_stock_set))):
		delete_flag = 1
		for j in range(len(stock_records.values)):
			if stock_records.values[j][i+1]:
				delete_flag = 0
				break
		if delete_flag == 1:
			id = tmp_stock_set[i]
			del(tmp_stock_set[i])
			stock_records.drop([id],axis=1,inplace=True)



	#画各股票持仓甘特图
	plt.figure(1) #另一幅图
	fig2, ax2 = plt.subplots()
	plt.plot(len(stock_records.values), len(tmp_stock_set)) #设置坐标轴刻度范围
	for j in range(len(tmp_stock_set)):
		buy_price = -1
		for i in range(len(stock_records.values)): #当天持有该股票的话画个点
			if not stock_records.values[i][j + 1] == 0:
				if buy_price == -1:
					buy_price = stock_records.values[i][j + 1]
				if stock_records.values[i][j + 1] >= buy_price:
					ax2.scatter(i,j,s = 10, c = 'r')
				else:
					ax2.scatter(i,j,s = 10, c = 'g')
			else:
				buy_price = -1
	
	ax2.set_title('趋势跟随策略下的股票持仓变化', fontsize=20)
	ax2.set_xlabel('交易日期')
	ax2.set_xticks(range(0, len(result['DateTime']), 10)) #显示坐标轴日期用的
	ax2.set_xticklabels(result['DateTime'][::10], rotation=45)
	plt.yticks(range(len(tmp_stock_set)),tmp_stock_set)
	ax2.set_ylabel('股票代码')

	# plt.show()
	return fig, ax, fig2, ax2, alpha

if __name__ == '__main__':
	run_strategy("20141010","20141015")

	