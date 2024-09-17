# -*- coding:utf-8 -*-
'''
@Description: 
@Version: 1.0
@Author: HollisYu
@Date: 2019-11-11 09:59:56
@LastEditors: HollisYu
@LastEditTime: 2019-12-18 15:47:58
'''
class Stock:
    def __init__(self, stock_id: str, buying_price: float, shares: float):
        self.stock_id = stock_id  # stock id

        self.buying_price = buying_price  # stock buying price for each shares
        self.shares = shares  # stock holding shares
        self.total_cost = self.buying_price * self.shares  # stock total buying cost, equal to buying_price * shares

        self.now_price = buying_price  # stock now price, change everyday
        self.total_value = self.total_cost  # stock now value, equal to now_price * shares
        self.profit = 0.0   # store profit percentage


    # def buy(self, buying_price: float, shares: float):
    #     self.shares += shares
    #     self.now_price = buying_price

    #     total_cost = shares * buying_price
    #     self.total_cost += total_cost
    #     self.buying_price = self.total_cost / self.shares
        
    #     self.total_value = self.shares * self.now_price


    # def sell(self, selling_price: float, shares: float):  
    #     self.shares -= shares
    #     self.now_price = selling_price
        
    #     total_value = shares * selling_price
    #     if self.shares != 0:
    #         self.total_cost -= total_value
    #         self.buying_price = self.total_cost / self.shares
    #         self.total_value = self.shares * self.now_price
    #     else:
    #         self.total_cost = 0
    #         self.buying_price = 0
    #         self.total_value = 0


    def update(self, now_price: float):
        self.now_price = now_price
        self.total_value = self.now_price * self.shares
        self.profit = (self.total_value - self.total_cost) / self.total_cost
