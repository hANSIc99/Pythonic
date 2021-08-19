import time, queue
import pandas as pd
from pathlib import Path
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):

        df_in = pd.DataFrame(self.inputData, columns=['close_time', 'open', 'high', 'low', 'close', 'volume'])

        df_in['close_time'] = df_in['close_time'].floordiv(1000)


        file_path = Path.home() / 'Pythonic' / 'executables' / 'ADAUSD_5m.df'

        
        try:
            df = pd.read_pickle(file_path)

            n_row_cnt = df.shape[0]
            df = pd.concat([df,df_in], ignore_index=True).drop_duplicates(['close_time'])
            df.reset_index(drop=True, inplace=True)
            n_new_rows = df.shape[0] - n_row_cnt
            log_txt = '{}: {} new rows written'.format(file_path, n_new_rows)
        except Exception as e:
            log_txt = 'File error - writing new one'
            df = df_in

        df.to_pickle(file_path)
        


        logInfo = Record(None, log_txt)   
        self.return_queue.put(logInfo)
        