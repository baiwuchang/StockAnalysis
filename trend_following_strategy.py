# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-13 14:02:47
@LastEditors: HollisYu
@LastEditTime: 2019-11-22 00:22:07
'''
import pandas as pd
import numpy as np
import datetime
import os
# local
import stock
import user

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
        if day_data['Mean10'] <= day_data['Mean30'] and day_data['Mean5'] < day_data['Mean30']:
            return True
        else:
            return False

    #if is buying
    else:
        if day_data['Mean10'] >= day_data['Mean30'] and day_data['Mean5'] > day_data['Mean30']:
            return True
        else:
            return False


def strategy(account, start_date, end_date):
    date = start_date
    sh_50 = []
    file_path = "./sh1_each_stock_data/"
    money_records = pd.DataFrame(columns=['DateTime', 'TotalMoney', 'Cash', 'Stocks'])
    
    while date <= end_date:
        if date.weekday() < 5:  # if it's Saturday or Sunday, skip
            # get sh_50 stocks
            sh_50 = get_sh50_info(date.strftime("%Y%m%d"))
            
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
                    dt = date.strftime("%Y-%m-%d")
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
                    
                # get all selling stocks and then sell them
                for stock_id in temp_sell:
                    account.sell_stock(stock_id)

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
                        dt = date.strftime("%Y-%m-%d")
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

                            # if already have 10 stocks, stop buying
                            if len(account.buy_in_stocks) >= 10:
                                break
        print("DateTime: {}, TotalMoney: {}, Cash: {}".format(date.strftime("%Y-%m-%d"), account.total_value, account.money))
        # record = pd.DataFrame([[date.strftime("%Y-%m-%d"), account.total_value, account.money, account.total_value - account.money]], columns=['DateTime', 'TotalMoney', 'Cash', 'Stocks'])
        # record = pd.Series({'DateTime': date.strftime("%Y-%m-%d"), 'TotalMoney': account.total_value, 'Cash':account.money, 'Stocks': account.total_value - account.money})
        # record account money change and buy-sell records
        # money_records.append(record, ignore_index=True)
        # add one day
        date += datetime.timedelta(days=1)
    
    print(money_records)
    return money_records

if __name__ == '__main__':
    my_account = user.User(200000.0)
    start_date = datetime.datetime.strptime("20140302", '%Y%m%d')
    end_date = datetime.datetime.strptime("20151231", '%Y%m%d')
    result = strategy(my_account, start_date, end_date)

