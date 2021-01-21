from pythonic_binance.client import Client
import datetime
import pandas as pd
from Pythonic.record_function import Record, Function

class BinanceOHLCFUnction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        interval_str, inteval_index, symbol_txt, log_state = self.config

        client = Client('', '')
        try:
            record = client.get_klines(symbol=symbol_txt, interval=interval_str)
        except Exception as e:
            log_txt = '{{BINANCE SCHEDULER}}      Exception caught: {}'.format(str(e))
            result = Record(self.getPos(), None, None, log=log_state, log_txt=log_txt)
            return result

        myList  = []
        item    = []


        try:
            for item in record:
                n_item = []
                int_ts = int(item[0]/1000)
                # nur neue timestamps anhängen

                n_item.append(int_ts)            # open time
                n_item.append(float(item[1]))    # open
                n_item.append(float(item[2]))    # high
                n_item.append(float(item[3]))    # low 
                n_item.append(float(item[4]))    # close 
                n_item.append(float(item[5]))    # volume 
                n_item.append(int(item[6]/1000)) # close_time 
                n_item.append(float(item[7]))    # quote_assetv 
                n_item.append(int(item[8]))      # trades 
                n_item.append(float(item[9]))    # taker_b_asset_v
                n_item.append(float(item[10]))   # taker_b_quote_v
                n_item.append(datetime.datetime.fromtimestamp(n_item[0]))
                myList.append(n_item)
        except:
            #logging.error('Data cant be read!')
            log_txt = '{{BINANCE SCHEDULER}}      Exception caught: {}'.format(str(e))
            result = Record(self.getPos(), None, None, log=log_state, log_txt=log_txt)
            return result

        new_ohlc = pd.DataFrame(myList, columns=['open_time', 'open', 'high', 'low',
            'close', 'volume', 'close_time', 'quote_assetv', 'trades', 'taker_b_asset_v',
            'taker_b_quote_v', 'datetime'])

        log_txt = '{{BINANCE OHLC QUERY}}     Received {} records'.format(len(record))
        result = Record(self.getPos(), (self.row +1, self.column), new_ohlc, log=log_state, log_txt=log_txt)

        return result
