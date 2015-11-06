#!/usr/bin/python
import pickle
import datetime
from lib.Transaction import Transaction

class Account:
    def __init__(self, id):
        self.id = id
        self.readRow = 0
        self.tList = []
        self.fHeadList = []

    def load(self, dbName):
        input = open(dbName, 'rb')
        acc = pickle.load(input)
        input.close()
        print("Bruker lokal database")
        return acc
    
    def save(self, dbName):
        output = open(dbName, 'wb')
        pickle.dump(self, output)
        output.close()

    def getTr(self, num):
        return self.tList[num]
        
    def size(self):
        return len(self.tList)
        
    def addRow(self, row, style):
        if style == 'NORDNET':
            if self.readRow == 0:
                # Header
                # Id;Bokføringsdag;Handelsdag;Oppgjørsdag;Transaksjonstype;Verdipapir;Instrumenttyp;ISIN;Antall;Kurs;Rente;
                # Avgifter;Beløp;Valuta;Kjøpsverdi;Resultat;Totalt antall;Saldo;Vekslingskurs;Transaksjonstekst;Makuleringsdato;Sluttseddelnummer
                self.fHeadList = row
            else:
                # 
                t = Transaction(id=self.getField(row, 'Id'))
                
                t.setCount(self.getField(row, 'Antall'))
                t.setPrice(self.getField(row, 'Kurs'))
                t.setTotal(self.getField(row, 'Beløp'))
                t.setFee(self.getField(row, 'Avgifter'))
                
                t.setProduct(self.getField(row, 'Verdipapir'))
                t.setType(self.getField(row, 'Transaksjonstype').replace('SALG', 'SELL').replace('KJØPT', 'BUY'))
                t.setCategory(self.getField(row, 'Instrumenttyp'))
                t.setDate(datetime.datetime.strptime(self.getField(row, 'Handelsdag'), "%Y-%m-%d").date())
                
                print(t.__dict__)
                
                self.tList.append(t)
            self.readRow += 1
            
    def getField(self, row, name):
        for i in range(0, len(self.fHeadList)):
            if self.fHeadList[i].lower() == name.lower():
                return row[i]
        return None
    
    def getStat(self):
        stat = {'tr': 0, 'prod': {}, 'cat': {}}
        
        for i in range(0, len(self.tList)):
            tr = self.getTr(i)
            
            if(tr.product in stat['prod']):
                stat['prod'][tr.product]['total'] += (tr.getAdjTotal())
                stat['prod'][tr.product]['holding'] += (tr.getAdjCount())
                stat['prod'][tr.product]['fees'] += tr.fee
                stat['prod'][tr.product]['trades'] += 1
            else:
                stat['prod'][tr.product] = {'total': tr.getAdjTotal(), 'holding': tr.getAdjCount(), 'fees': tr.fee, 'trades': 1}
        return stat
        