# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-13 14:11:22
@LastEditors: HollisYu
@LastEditTime: 2019-11-13 15:44:18
'''
import stock

class User:
    def __init__(self, money:float):
        self.money = money
        self.buy_in_stocks = {}

    def buy_stock(self, stock_id:str, buying_price:float, shares:float):
        # if already have, add shares
        if stock_id in self.buy_in_stocks.keys():
            self.buy_in_stocks[stock_id].buy(buying_price, shares)
        else:
            # more than 10 stocks already have, stop buy in
            if len(self.buy_in_stocks) >= 10:
                return

            # add new stock to account
            self.buy_in_stocks[stock_id] = stock.Stock(stock_id, buying_price, shares)
            self.money -= buying_price * shares
        
    def sell_stock(self, stock_id:str, selling_price:float, shares:float):
        # if dont have, return
        if stock_id not in self.buy_in_stocks.keys():
            return

        # sell out the stock
        if shares >= self.buy_in_stocks[stock_id].shares:
            self.buy_in_stocks[stock_id].sell(selling_price, self.buy_in_stocks[stock_id].shares)
            self.money += selling_price * self.buy_in_stocks[stock_id].shares
            self.buy_in_stocks.pop(stock_id)
        # not sell out
        else:
            self.buy_in_stocks[stock_id].sell(selling_price, shares)
            self.money += selling_price * shares

    def total_money(self) -> float:
        total = self.money
        for s in self.buy_in_stocks.values():
            total += s.shares * s.now_price
        return total
        