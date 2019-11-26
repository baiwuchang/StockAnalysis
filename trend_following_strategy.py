# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-13 14:02:47
@LastEditors: HollisYu
@LastEditTime: 2019-11-26 23:00:50
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


def check(stock_id: str, day_data, op_type: str) -> bool:
    # Volume is 0, cannot do anything
    if day_data['Volume'] == 0:
        return False

    # if is selling
    if op_type == "sell":
        # if day_data['Mean10'] <= day_data['Mean30'] and day_data['Mean5'] < day_data['Mean30']:
        if day_data['DIF'] <= day_data['DEA'] and day_data['DIF'] < 0 and day_data['DEA'] < 0:
            return True
        else:
            return False

    #if is buying
    else:
        # if day_data['Mean10'] >= day_data['Mean30'] and day_data['Mean5'] > day_data['Mean30']:
        if day_data['DIF'] >= day_data['DEA'] and day_data['DIF'] > 0 and day_data['DEA'] > 0:
            return True
        else:
            return False


def strategy(account, start_date, end_date):
    #画甘特图需要的
    gantt_data = []
    gantt_data_everyday = [0] * 97 #某天是否持有某个股票
    #画甘特图需要的-结束

    date = start_date
    sh_50 = []
    file_path = "./sh1_each_stock_data/"
    money_records = pd.DataFrame(columns=['DateTime', 'TotalMoney', 'Cash', 'Stocks'])
    stock_records = pd.DataFrame(columns=['DateTime'] + stock_set)

    
    while date <= end_date:
        if date.weekday() < 5:  # if it's Saturday or Sunday, skip
            # get sh_50 stocks
            sh_50 = get_sh50_info(date.strftime("%Y%m%d"))
            dt = date.strftime("%Y-%m-%d")
            
            if sh_50:   # if no sh_50 data, maybe a holiday, skip
                # first sell stocks which are down, also update prices
                temp_sell = []  # store selling stocks temperly
                for stock_id in account.buy_in_stocks:
                    # open data file
                    file_name = file_path + "ID_" + stock_id + "_Day.csv"
                    # if data not exists, skip
                    if not os.path.exists(file_name):
                        continue
                    stock_data = pd.read_csv(file_name)
                    stock_data.set_index('DateTime', drop=False, inplace=True)
                    # get today data line
                    # if data not exists, skip
                    if dt not in stock_data.index:
                        continue
                    today_data = stock_data.loc[dt]
                    # update value
                    account.update_stock(stock_id, today_data['LastPx'])

                    # check whether to sell the stock
                    sell_flag = check(stock_id, today_data, "sell")
                    # stock down, sell all
                    if sell_flag:
                        temp_sell.append(stock_id)
                        gantt_data_everyday[stock_set.index(stock_id)] = 0 #甘特图需要
                    
                # get all selling stocks and then sell them
                for stock_id in temp_sell:
                    account.sell_stock(stock_id)
                    print("Sell stock: {} on {}".format(stock_id, dt))

                # check if there have place to buy stocks
                if len(account.buy_in_stocks) < 10:
                    for stock_id in sh_50:
                        # already have, continue to next one
                        if stock_id in account.buy_in_stocks:
                            continue

                        # open data file
                        file_name = file_path + "ID_" + stock_id + "_Day.csv"
                        # if data not exists, skip
                        if not os.path.exists(file_name):
                            continue
                        stock_data = pd.read_csv(file_name)
                        stock_data.set_index('DateTime', drop=False, inplace=True)
                        # get today data line
                        # if data not exists, skip
                        if dt not in stock_data.index:
                            continue
                        today_data = stock_data.loc[dt]

                        # check whether to buy the stock
                        buy_flag = check(stock_id, today_data, "buy")
                        if buy_flag:
                            # buy no more than threshold or money have
                            money = min(account.up_threshold, account.money)
                            account.buy_stock(stock_id, today_data['LastPx'], money)
                            print("Buy stock: {} on {}".format(stock_id, dt))

                            gantt_data_everyday[stock_set.index(stock_id)] = 1 #甘特图需要

                            # if already have 10 stocks, stop buying
                            if len(account.buy_in_stocks) >= 10:
                                break
        # record account money change and buy-sell records
        record = pd.DataFrame([[date.strftime("%Y-%m-%d"), account.total_value, account.money, account.total_value - account.money]], columns=['DateTime', 'TotalMoney', 'Cash', 'Stocks'])
        money_records = money_records.append(record, ignore_index=True)
        record_for_gantt = pd.DataFrame([[date.strftime("%Y-%m-%d")] + gantt_data_everyday], columns=['DateTime'] + stock_set)
        stock_records = stock_records.append(record_for_gantt, ignore_index = True)
        # add one day
        date += datetime.timedelta(days=1)
    
    return money_records, stock_records

if __name__ == '__main__':
    my_account = user.User(200000.0)
    start_date = datetime.datetime.strptime("20140302", '%Y%m%d')
    end_date = datetime.datetime.strptime("20141231", '%Y%m%d')
    result, stock_records = strategy(my_account, start_date, end_date)

    #画账户变化图
    fig, ax = plt.subplots()
    for label in ['TotalMoney', 'Cash', 'Stocks']: 
        ax.plot(result[label], label=label)
    ax.set_title('趋势跟随策略下的账户变化', fontsize=20)
    ax.set_xlabel('交易日期')
    ax.set_xticks(range(0, len(result['DateTime']), 10))
    ax.set_xticklabels(result['DateTime'][::10], rotation=45)
    ax.set_ylabel('金额(元)')
    ax.legend(loc='upper left')
    ax.grid(True)


    
    #先把没买过的的股票删掉
    for i in reversed(range(len(stock_set))):
        delete_flag = 1
        for j in range(len(stock_records.values)):
            if stock_records.values[j][i+1]:
                delete_flag = 0
                break
        if delete_flag == 1:
            id = stock_set[i]
            del(stock_set[i])
            stock_records.drop([id],axis=1,inplace=True)

    #画各股票持仓甘特图
    plt.figure(1) #另一幅图
    fig2, ax2 = plt.subplots()
    plt.plot(len(stock_records.values), len(stock_set)) #设置坐标轴刻度范围
    for i in range(len(stock_records.values)): #当天持有该股票的话画个点
        for j in range(len(stock_set)):
            if stock_records.values[i][j] == 1:
                ax2.scatter(i,j,s = 10, c = 'r')
    
    ax2.set_title('趋势跟随策略下的股票持仓变化', fontsize=20)
    ax2.set_xlabel('交易日期')
    ax2.set_xticks(range(0, len(result['DateTime']), 10)) #显示坐标轴日期用的
    ax2.set_xticklabels(result['DateTime'][::10], rotation=45)
    plt.yticks(range(len(stock_set)),stock_set)
    ax2.set_ylabel('股票代码')

    plt.show()

    