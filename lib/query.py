#!/usr/bin/python
import datetime
from lib.Account import Account
from lib.Transaction import Transaction

d = datetime.date.today()
accId = d.strftime("%d-%m-%y")

acc = Account(id=accId)

# Sjekk om database finnes
try:
    acc.load(fName)
    
except Exception: 
    print("Kunne ikke lese lokal database - lag en fra transaksjonsdata")

if acc.size() > 0:
    print("Gjør et søk")