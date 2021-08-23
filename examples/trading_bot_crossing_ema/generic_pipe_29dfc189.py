import time, queue
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
try:
    from element_types import Record, Function, ProcCMD, GuiCMD, ListPersist
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD, ListPersist


@dataclass
class OrderRecord:

    orderType:          bool
    price:              float
    exchangeReturnCode: str
    profit:             float # profit in percent
    profitCumulative:   float # cumulative profit in percent

    
class Element(Function):

   


    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):


        #####################################
        #                                   #
        #             LOAD DATA             #
        #                                   #
        #####################################

        bBought     = False
        trackRecord = ListPersist('track_record')

        try:
            last = trackRecord[-1]

        except IndexError:
            bBought = False
        
        
        newOrder = OrderRecord(
            orderType=False,
            price=0.0,
            exchangeReturnCode='test',
            profit=0.0,
            profitCumulative=0.5)
        
        trackRecord.append(newOrder)

        file_path = Path.home() / 'Pythonic' / 'executables' / 'ADAUSD_5m.df'

        # only the last 21 columsn are considered
        ohlcv = pd.read_pickle(file_path)[-5:]

        ohlcv['ema-10'] = ohlcv['close'].ewm(span = 10, adjust=False).mean()
        ohlcv['ema-21'] = ohlcv['close'].ewm(span = 21, adjust=False).mean()
        ohlcv['condition'] = ohlcv['ema-10'] > ohlcv['ema-21']
        
        #########################################
        #                                       #
        #    The execution exits immediately    #
        #    after providing output data        #
        #                                       #
        #########################################

        #recordDone = Record(output, 'Sending value of cnt: {}'.format(output))     
        #self.return_queue.put(recordDone)