#!/usr/bin/python
import datetime
import sys
from lib.Account import Account
from lib.Transaction import Transaction

class QueryResult:
    def __init__(self):
        self.rList = []
        self.total = 0.0
        self.tBuy = 0.0
        self.tSell = 0.0
        self.fees = 0.0
        self.holding = 0.0
    
    def add(self, tr):
        self.rList.append(tr)

    def calculate(self):
        self.total = 0.0
        for i in range(0, len(self.rList)):
            self.total += self.rList[i].total
            self.holding += self.rList[i].getAdjCount()
            self.fees += self.rList[i].fee
            
            if(self.rList[i].type == 'BUY'):
                self.tBuy += self.rList[i].total
            if(self.rList[i].type == 'SELL'):
                self.tSell += self.rList[i].total
    
        
class Query:
    def __init__(self, acc):
        self.acc = acc
    
    def searchProduct(self, productName):
        res = QueryResult()
        for i in range(0, self.acc.size()):
            tr = self.acc.getTr(i)
            if tr.product.lower() == productName.lower():
                res.add(tr)
        
        return res

d = datetime.date.today()
accId = d.strftime("%d-%m-%y")
fName = accId + '.pkl'
acc = Account(id=accId)

# Sjekk om database finnes
try:
    acc = acc.load(fName)
    
except Exception: 
    print("Kunne ikke lese lokal database - lag en fra transaksjonsdata")

if acc.size() > 0:
    print("Søker i %s rader" % (acc.size()))
    
    try:
        q = None
        
        if len(sys.argv) > 1:
            prod = sys.argv[1]
            q = Query(acc)
        
        res = q.searchProduct(prod)
        res.calculate()
        fTr = res.rList[0]
        lTr = res.rList[len(res.rList) - 1]
        
        print("SEARCH %s" % prod)
        
        print("PROD: ".ljust(30) + fTr.product)
        print("RESULT: ".ljust(30) + str(round(res.total, 2)))
        print("FEES: ".ljust(30) + str(round(res.fees, 2)) + " (" + str(round((res.fees / res.total) * 100, 2)) + "%)")
        print("DAYS: ".ljust(30) + str(fTr.date - lTr.date))
        
        print("")
        
        for i in range(0, len(res.rList)):
            tr = res.rList[i]
            print(tr.date.strftime("%d-%m-%Y").ljust(30) + str(round(tr.total, 2)))
        
        print("")
    except Exception as e:
        print("Except" + e)
        
    print("PR PRODUKT:")
    stat = acc.getStat()
    
    print(" ".ljust(30) + "TOTAL".rjust(12) + "FEES".rjust(8) + "TRADES".rjust(8) + "HOLDING".rjust(8))
    
    for key in stat['prod'].keys():
        print(key.ljust(30) + str(round(stat['prod'][key]['total'])).rjust(12) + str(stat['prod'][key]['fees']).rjust(8)+ str(stat['prod'][key]['trades']).rjust(8) + str(stat['prod'][key]['holding']).rjust(8))
    
    


else:
    print("Database har %s rader" % (acc.size()))
    
