from pythonic_binance.client import Client
from time import sleep
import datetime
from Pythonic.record_function import Record, Function


ohlc_steps = { '1m' : 1, '3m' : 3, '5m' : 5, '15m' : 15, '30m' : 30, '1h' : 60, '2h' : 120, '4h' : 240, '6h' : 360,
        '8h' : 480, '12h' : 720, '1d' : 1440, '3d' : 4320, '1w' : 10080, '1M' : 40320 }

class BinanceScheduler(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('__init__() called BinanceScheduler')

    def execute(self, record):

        interval_str, interval_index, offset, log_state = self.config

        if isinstance(record, tuple) and isinstance(record[0], datetime.datetime):
            
            while record[0] > datetime.datetime.now():
                sleep(1)

            record = record[1]
            target = (self.row + 1, self.column)
            log_txt = '{BINANCE SCHEDULER}      >>>EXECUTE<<<'

            result = Record(self.getPos(), target, record, log=log_state, log_txt=log_txt)

        else:

            client = Client('', '')

            try:
                binance_time = client.get_server_time()
            except Exception as e:
                log_txt = '{{BINANCE SCHEDULER}}      Exception caught: {}'.format(str(e))
                result = Record(self.getPos(), None, None, log=True, log_txt=log_txt)

            binance_time = binance_time['serverTime']
            binance_time /= 1000
            binance_timestamp = datetime.datetime.fromtimestamp(binance_time)

            offset = datetime.timedelta(seconds=offset)

            ohlc_step = datetime.timedelta(minutes=ohlc_steps[interval_str])

            date = datetime.datetime.now().date()
            # 00:00 o'clock for the actual date
            sync_time = datetime.datetime(date.year, date.month, date.day)

            # while loop leaves when the next ohlc_step target time is found 
            while sync_time < binance_timestamp:
                sync_time += ohlc_step


            sync_time += offset
            countdown = sync_time - datetime.datetime.now()

            target  = self.getPos()
            record  = (sync_time, record)
            hours   = countdown.seconds // 3600
            minutes = (countdown.seconds // 60) % 60
            seconds = countdown.seconds % 60
            log_txt = '{{BINANCE SCHEDULER}}      Synchronization successful, '\
                    'execution starts in {:02}:{:02}:{:02}'.format(hours, minutes, seconds)

            result = Record(self.getPos(), target, record, log=log_state, log_txt=log_txt)

        return result
