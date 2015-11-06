#!/usr/bin/python

class Transaction:
    def __init__(self, id):
        self.id = id
        self.date = None
        self.count = 0.0
        self.price = 0.0
        self.total = 0.0
        self.fee = 0.0
        self.product = "" # Name of product/paper
        self.type = "" # BUY, SELL
        self.currency = None
        
        #print("New trans: %s" % id)
    
    def getAdjTotal(self):
        if self.type == 'BUY':
            return self.total# * -1
        return self.total
    
    def getAdjCount(self):
        if self.type == 'SELL':
            return self.count * -1
        return self.count
    
    def setTotal(self, sum):
        self.total = float(sum.replace(',', '.').replace(' ', ''))
    
    def setPrice(self, price):
        self.price = float(price.replace(',', '.').replace(' ', ''))
    
    def setCount(self, count):
        self.count = float(count.replace(',', '.').replace(' ', ''))
        
    def setFee(self, fee):
        self.fee = float(fee.replace(',', '.').replace(' ', ''))
        
    def setProduct(self, name):
        self.product = name
    def setType(self, type):
        self.type = type