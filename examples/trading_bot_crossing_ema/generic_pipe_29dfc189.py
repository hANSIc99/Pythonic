import time, queue
from enum import Enum
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, ListPersist
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, ListPersist


@dataclass
class OrderRecord:
    orderType:          bool  # True = Buy, False = Sell
    price:              float # close price
    profit:             float # profit in percent
    profitCumulative:   float # cumulative profit in percent


class OrderType(Enum): 
    Buy  = True
    Sell = False


class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)

    def execute(self):

        ### Load data ###

        file_path = Path.home() / 'Pythonic' / 'executables' / 'ADAUSD_5m.df'

        # only the last 21 columsn are considered
        self.ohlcv = pd.read_pickle(file_path)[-21:]

        self.bBought             = False
        self.lastPrice           = 0.0
        self.profit              = 0.0
        self.profitCumulative    = 0.0   
        self.price               = self.ohlcv['close'].iloc[-1]
        
        # switches for simulation

        self.bForceBuy  = False
        self.bForceSell = False
        

        # load trade history from file
        self.trackRecord = ListPersist('track_record')

        try:
            lastOrder = self.trackRecord[-1]

            self.bBought          = lastOrder.orderType
            self.lastPrice        = lastOrder.price
            self.profitCumulative = lastOrder.profitCumulative

        except IndexError:
            pass
        
        ### Calculate indicators ###

        self.ohlcv['ema-10'] = self.ohlcv['close'].ewm(span = 10, adjust=False).mean()
        self.ohlcv['ema-21'] = self.ohlcv['close'].ewm(span = 21, adjust=False).mean()
        self.ohlcv['condition'] = self.ohlcv['ema-10'] > self.ohlcv['ema-21']
        
        ### Check for Buy- / Sell-condition ###
        tradeCondition = self.ohlcv['condition'].iloc[-1] != self.ohlcv['condition'].iloc[-2]

        if tradeCondition or self.bForceBuy or self.bForceSell:

            orderType = self.ohlcv['condition'].iloc[-1] # True = BUY, False = SELL

            if orderType and not self.bBought or self.bForceBuy: # place a buy order
                
                msg         = 'Placing a  Buy-order'
                newOrder    = self.createOrder(True)

            elif not orderType and self.bBought or self.bForceSell: # place a sell order

                msg = 'Placing a  Sell-order'

                sellPrice   = self.price
                buyPrice    = self.lastPrice

                self.profit = (sellPrice * 100) / buyPrice - 100
                self.profitCumulative += self.profit

                newOrder = self.createOrder(False)

            else: # Something went wrong
                msg         = 'Warning: Condition for {}-order met but bBought is {}'.format(
                    OrderType(orderType).name, self.bBought)

                newOrder    = None
            

            recordDone = Record(newOrder, msg)     
            self.return_queue.put(recordDone)


    def createOrder(self, orderType: bool) -> OrderRecord:
        
        newOrder = OrderRecord(
                orderType=orderType,
                price=self.price,
                profit=self.profit,
                profitCumulative=self.profitCumulative
            )
        
        self.trackRecord.append(newOrder)

        return newOrder