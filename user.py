# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-13 14:11:22
@LastEditors: HollisYu
@LastEditTime: 2019-11-20 16:54:13
'''
import stock

class User:
    def __init__(self, money:float):
        self.money = money  # cash
        self.buy_in_stocks = {} # dict of stocks have
        self.total_value = money    # all money and stock values


    def buy_stock(self, stock_id:str, buying_price:float, volume: float):
        # more than 10 stocks already have, stop buy in
        if len(self.buy_in_stocks) >= 10:
            return

        fee = self.calculate_fee(volume, "buy")
        shares = (volume - fee) / buying_price
        # add new stock to account
        self.buy_in_stocks[stock_id] = stock.Stock(stock_id, buying_price, shares)

        self.money = self.money - volume
        

    def sell_stock(self, stock_id:str):
        # if dont have, return
        if stock_id not in self.buy_in_stocks.keys():
            return

        # sell out the stock        
        volume = self.buy_in_stocks[stock_id].total_value
        self.buy_in_stocks.pop(stock_id)
        
        # cal fee
        fee = self.calculate_fee(volume, "sell")
        self.money = self.money + volume - fee


    def update_stock(self, stock_id: str, now_price: float):
        if stock_id not in self.buy_in_stocks:
            return

        pre_value = self.buy_in_stocks[stock_id].total_value
        self.buy_in_stocks[stock_id].update(now_price)
        now_value = self.buy_in_stocks[stock_id].total_value
        self.total_value += now_value - pre_value


    def calculate_fee(self, volume: float, operation_type: str) -> float:
        # total fee
        rate = 0.0005
        # sell have another stamp_tax(0.1%) to pay
        if operation_type == "sell":
            # add stamp tax(0.1%)
            rate += 0.001
        
        # all operations need transfer fee(0.002%) and trade fee(0.03%)
        # transfer_fee = volume * 0.00002
        # trade_fee = volume * 0.0003
        total_fee = volume * rate

        return total_fee


    def total_money(self) -> float:
        total = self.money
        for s in self.buy_in_stocks.values():
            total += s.shares * s.now_price
        return total
        