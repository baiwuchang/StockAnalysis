# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-13 14:02:47
@LastEditors: HollisYu
@LastEditTime: 2019-11-20 16:55:17
'''
import pandas as pd
import numpy as np
import datetime
# local
import stock
import user

def get_sh50_info(stocks: list, asending_stocks: list, date: str):
    pass


def check(stock_id: str, stock_data, op_type: str) -> bool:
    if op_type == "sell":
        return False
    else:
        return True


def strategy(account, start_date, end_date):
    dt = start_date
    sh_50 = []
    ascending_stocks = []
    while dt <= end_date:
        date = dt.strftime("%Y%m%d")
        # TODO: cal sh_50 stocks and add 
        get_sh50_info(sh_50, ascending_stocks, date)

        # check if buy the stock in sh_50
        # TODO: open data file
        file_path = "D:/Files/Codes/Dataset/his_sh1_Day/"
        file_name = file_path + date + "_Day.csv"
        day_data = pd.read_csv(file_name)
        day_data.set_index('SecurityID', drop=False, inplace=True)

        # first sell stocks which are down, also update prices
        for stock_id in account.buy_in_stocks:
            stock_data = day_data.loc[stock_id]
            account.update_stock(stock_id, stock_data['LastPx'])
            sell_flag = check(stock_id, stock_data, "sell")
            # stock down, sell all
            if sell_flag:
                account.sell_stock(stock_id)

        # cal 1R
        stock_up_threshold = account.total_value / 11

        if len(account.buy_in_stocks) < 10:
            for stock_id in sh_50:
                # already have, continue to next one
                if stock_id in account.buy_in_stocks:
                    continue

                stock_data = day_data.loc[stock_id]
                buy_flag = check(stock_id, stock_data, "buy")
                if buy_flag:
                    volume = min(stock_up_threshold, account.money)
                    account.buy_stock(stock_id, stock_data['LastPx'], volume)

                    if len(account.buy_in_stocks) >= 10:
                        break
        
        # add one day
        dt += datetime.timedelta(days=1)

if __name__ == '__main__':
    my_account = user.User(200000.0)
    start_date = datetime.datetime.strptime("20140202", '%Y%m%d')
    end_date = datetime.datetime.strptime("20181231", '%Y%m%d')
    strategy(my_account, start_date, end_date)
