#!/usr/bin/python

#import http.client

import datetime
import sys
from lib.Account import Account
from lib.Transaction import Transaction

tFile = 'C:\\Users\\extthk\\Downloads\\transaktionsfil.csv'
if sys.argv[1]:
    tFile = sys.argv[1]

d = datetime.date.today()
accId = d.strftime("%d-%m-%y")
fName = accId + '.pkl'

acc = Account(id=accId)


delim = ";"
f = open(tFile, 'r')

for line in f:
    if line.strip() != '':
        row = line.split(delim)
        acc.addRow(row, style='NORDNET')

acc.save(fName)

    
# Lag database (pickle)

# Eget script for søk og statistikk fra basen

print("%s transaksjoner fra base: %s" % (len(acc.tList), acc.id + '.pkl'))