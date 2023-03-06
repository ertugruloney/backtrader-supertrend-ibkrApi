
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from datetime import datetime
import sys

import backtrader as bt

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from pandas_datareader import data as pdr
import threading
import time
import backtrader as bt
import backtrader.plot
import matplotlib
from option2 import option as op
matplotlib.use('QT5Agg')

from atreyu_backtrader_api import IBData
class SuperTrendBand(bt.Indicator):
    """
    Helper inidcator for Supertrend indicator
    """
    params = (('period',7),('multiplier',3))
    lines = ('basic_ub','basic_lb','final_ub','final_lb')


    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(period=self.p.period)
        self.l.basic_ub = ((self.data.high + self.data.low) / 2) + (self.atr * self.p.multiplier)
        self.l.basic_lb = ((self.data.high + self.data.low) / 2) - (self.atr * self.p.multiplier)

    def next(self):
        if len(self)-1 == self.p.period:
            self.l.final_ub[0] = self.l.basic_ub[0]
            self.l.final_lb[0] = self.l.basic_lb[0]
        else:
            #=IF(OR(basic_ub<final_ub*,close*>final_ub*),basic_ub,final_ub*)
            if self.l.basic_ub[0] < self.l.final_ub[-1] or self.data.close[-1] > self.l.final_ub[-1]:
                self.l.final_ub[0] = self.l.basic_ub[0]
            else:
                self.l.final_ub[0] = self.l.final_ub[-1]

            #=IF(OR(baisc_lb > final_lb *, close * < final_lb *), basic_lb *, final_lb *)
            if self.l.basic_lb[0] > self.l.final_lb[-1] or self.data.close[-1] < self.l.final_lb[-1]:
                self.l.final_lb[0] = self.l.basic_lb[0]
            else:
                self.l.final_lb[0] = self.l.final_lb[-1]

class SuperTrend(bt.Indicator):
    """
    Super Trend indicator
    """
    params = (('period', 7), ('multiplier', 3))
    lines = ('super_trend',)
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.stb = SuperTrendBand(period = self.p.period, multiplier = self.p.multiplier)

    def next(self):
        if len(self) - 1 == self.p.period:
            self.l.super_trend[0] = self.stb.final_ub[0]
            return

        if self.l.super_trend[-1] == self.stb.final_ub[-1]:
            if self.data.close[0] <= self.stb.final_ub[0]:
                self.l.super_trend[0] = self.stb.final_ub[0]
            else:
                self.l.super_trend[0] = self.stb.final_lb[0]

        if self.l.super_trend[-1] == self.stb.final_lb[-1]:
            if self.data.close[0] >= self.stb.final_lb[0]:
                self.l.super_trend[0] = self.stb.final_lb[0]
            else:
                self.l.super_trend[0] = self.stb.final_ub[0]
class testStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        if  True:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s - %s' % (dt.isoformat(), txt))
 
    def __init__(self):
        self.Option=op('SPY',10000)
        self.x = SuperTrend(self.data)
        self.dclose = self.datas[0].close
        self.cross = bt.ind.CrossOver(self.dclose, self.x)
        self.order = None
        self.closes=[]
        self.openn=[]
        self.status=0
    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED: %s, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.data._name,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log('SELL EXECUTED: %s, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.data._name,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                
    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT: EQ %s, GROSS %.2f, NET %.2f' %
                     ('Closed'  , trade.pnl, trade.pnlcomm))
        elif trade.justopened:
            self.log('TRADE OPENED: EQ %s, SIZE %2d' % (  'Opened'  , trade.size))
                
    def next(self):
       
        
     
  
       if self.status==0:
           if not self.position: 
                   
                   self.closes.insert(0, self.data.close[0])
                   self.openn.insert(0,self.data.open[0])
                  
                   
                   status=0
                   #supertrende
                   if self.cross[0]==1 :
                       status=1
                       self.log('Buy Create, %.2f' % self.data.close[0])
                       self.order = self.buy(size=1,price=10)
                       a=str(self.datetime.date(ago=0))
                       b=a.split('-')

                       datee=b[0]+b[1]+b[2]

                       self.Option.buy(datee,self.data.close[0])
                       # close crosses 2 consecutive green bars
                   if len(self.closes)>=3:    
                    
                       if   status==0 and self.closes[2]> self.openn[2] and self.closes[1]>self.openn[1] and self.data.close[0]>self.closes[1]:
                           self.log('Buy Create, %.2f' % self.data.close[0])
                           self.order = self.buy(size=1,price=10)
                           a=str(self.datetime.date(ago=0))
                           b=a.split('-')

                           datee=b[0]+b[1]+b[2]

                           self.Option.buy(datee,self.data.close[0])
                   if len(self.closes)>=6:      
                       rangee=0
                       for i in range(1,6):
                           if abs(self.closes[i]-self.openn[i])>rangee:
                               rangee=abs(self.closes[i]-self.openn[i])
                       if status==0 and self.data.close[0]>self.data.open[0] and abs(self.data.close[0]-self.data.open[0])>rangee:
                           
                        self.log('Buy Create, %.2f' % self.data.close[0])
                        self.order = self.buy(size=1,price=10)
                        a=str(self.datetime.date(ago=0))
                        b=a.split('-')

                        datee=b[0]+b[1]+b[2]

                        self.Option.buy(datee,self.data.close[0])
           if int(self.position.price)>0:
                 status2=0
                 if abs(self.position.price-self.data.close[0])>self.position.price*0.02:
                     self.order = self.sell(size=1,price=10)
                     a=str(self.datetime.date(ago=0))
                     b=a.split('-')

                     datee=b[0]+b[1]+b[2]

                     self.Option.selll(datee,self.data.close[0])
           status2=0       
           if len(self.closes)>=3:
              if status2==0 and self.closes[1]< self.openn[1] and self.closes[0]<self.openn[0] :
                   if int(self.position.price)>0:
                       self.order = self.sell(size=1,price=10)
                       a=str(self.datetime.date(ago=0))
                       b=a.split('-')

                       datee=b[0]+b[1]+b[2]

                       self.Option.selll(datee,self.data.close[0])
                      
                
           if len(self.closes)>=6:      
                       rangee=0
                       for i in range(1,6):
                           if abs(self.closes[i]-self.openn[i])>rangee:
                               rangee=abs(self.closes[i]-self.openn[i])
                       if status2==0 and self.data.close[0]<self.data.open[0] and abs(self.data.close[0]-self.data.open[0])>rangee:    
                           if int(self.position.price)>0:
                               self.order = self.sell(size=1,price=10)
                               a=str(self.datetime.date(ago=0))
                               b=a.split('-')

                               datee=b[0]+b[1]+b[2]

                               self.Option.selll(datee,self.data.close[0])
                              
     
             
if __name__ == '__main__':


    class IBapi(EWrapper, EClient):
    	def __init__(self):
    		EClient.__init__(self, self)
    		self.data = [] #Initialize variable to store candle
    
    	def historicalData(self, reqId, bar):
    		print(f'Time: {bar.date} Close: {bar.close} Open: {bar.open}')
    		self.data.append([bar.date, bar.close,bar.open])
    		
    def run_loop():
    	app.run()
    
    app = IBapi()
    app.connect('127.0.0.1', 7496, 123)
    
    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    
    time.sleep(1) #Sleep interval to allow time for connection to server
    
    #Create contract object
    eurusd_contract = Contract()
    eurusd_contract.symbol = 'SPY'
    eurusd_contract.secType = 'STK'
    eurusd_contract.exchange = "SMART"
    eurusd_contract.currency = 'USD'
    
    #Request historical candles
    app.reqHistoricalData(1, eurusd_contract, '', '5 D', '1 min','BID', 0, 2, False, [])
    
    time.sleep(5) #sleep to allow enough time for data to be returned
    
    #Working with Pandas DataFrames
    import pandas
    
    df = pandas.DataFrame(app.data, columns=['DateTime', 'Close','Open'])
    df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s') 
    
    
    class PandasData(bt.feeds.PandasData):
        
        params = (
            ('datetime', 'DateTime'),
            ('open','Open'),
            ('high',None),
            ('low',None),
            ('close','Close'),
            ('volume',None),
            ('openinterest',None),
            ('adj_close',None),
            ('pct',None),
            ('pct2',None),
            ('pct3',None),
        )
    
    
    app.disconnect()




    df=PandasData(dataname=df)
    
    cerebro = bt.Cerebro()
    cerebro.addstrategy(testStrategy)
    cerebro.broker.setcash(10000)
    
    cerebro.adddata(df)
   
    # Print out the starting conditions
    print('Starting Portfolio Value: %.8f' % cerebro.broker.getvalue())

# Run over everything

    cerebro.run()
# Print out the final result
    print('Final Portfolio Value: %.8f' % cerebro.broker.getvalue())


# Plot the result
    cerebro.plot(style='candlestick', barup='green', bardown='red',volume=False,iplot=False)
   