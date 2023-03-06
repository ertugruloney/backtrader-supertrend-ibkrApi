
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from pandas_datareader import data as pdr
from datetime import datetime
from ib_insync import *
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import threading
import time
import pandas
import datetime
import math
import backtrader as bt
util.startLoop()
class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = [] #Initialize variable to store candle

	def historicalData(self, reqId, bar):
		print(f'Time: {bar.date} Close: {bar.close} Open: {bar.open}')
		self.data.append([bar.date, bar.close,bar.open])
class option:
    def __init__(self,symbol,cash):
     
   
      self.cash=cash
      self.orderS=0
      self.symbol=symbol

    def histdata(self,date,price):
        self.datee=date
        price=int(price)
        def run_loop():
        	app.run()
        app = IBapi()
        app.connect('127.0.0.1', 7496, 123)
        
        #Start the socket in a thread
        api_thread = threading.Thread(target=run_loop, daemon=True)
        api_thread.start()
        
        ib = IB()
        ib.connect('127.0.0.1',7496,clientId=1)
                   
        underlying = Stock(self.symbol, 'SMART', 'USD')
        ib.qualifyContracts(underlying)
        chains =ib.reqSecDefOptParams(underlying.symbol, '',underlying.secType, underlying.conId)
        durum=0
        for optionschain in chains:
             if durum==0:
                 for strike in optionschain.strikes:
                         if strike>price:
                             
                            time.sleep(1) #Sleep interval to allow time for connection to server
                            
                            try:
                                queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
                                eurusd_contract = Contract()
                                eurusd_contract.symbol = self.symbol
                                eurusd_contract.secType = 'OPT'
                                eurusd_contract.exchange = 'SMART'
                                eurusd_contract.currency = 'USD'
                                eurusd_contract.lastTradeDateOrContractMonth=optionschain.expirations[1]
                                eurusd_contract.strike=strike
                                eurusd_contract.right='CALLS'
                                #Request historical candles
                                app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 min','TRADES', 1, 1, False, [])
                                durum=1
                                break
                            except:
                                
                                queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
                                eurusd_contract = Contract()
                                eurusd_contract.symbol = self.symbol
                                eurusd_contract.secType = 'OPT'
                                eurusd_contract.exchange = 'SMART'
                                eurusd_contract.currency = 'USD'
                                eurusd_contract.lastTradeDateOrContractMonth=optionschain.expirations[2]
                                eurusd_contract.strike=strike
                                eurusd_contract.right='CALLS'
                                #Request historical candles
                                app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 min','TRADES', 1, 1, False, [])
                                durum=1
                                break
            
        
        time.sleep(5) #sleep to allow enough time for data to be returnedleep to allow enough time for data to be returned
        df = pandas.DataFrame(app.data, columns=['DateTime', 'Close','Open'])
        df['DateTime'] = pandas.to_datetime(df['DateTime']) 
        self.df=df
    def buy(self,date,price):
        
        if self.orderS==0:
            self.histdata(date,price)
            self.com=self.df.iloc[1,len(self.df)-1]
            self.sizee=100
            self.cash=self.cash-self.sizee*self.com
            self.orderdate=date
            self.orderS=1
            self.orderPrice=price
    def selll(self,date,price):
          self.histdata(date,price)
          self.sizee=100
          self.cash=self.cash+self.sizee*((self.com+self.orderPrice)-self.price)
          self.orderdate=date
      
          self.orderS=0
            
            
                
  

   