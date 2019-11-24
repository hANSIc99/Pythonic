import pandas as pd
from Pythonic.record_function import Record, Function

class TAFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('__init__() called TAFunction')

    def execute(self, record):

        ta_str, ta_index, ta_config, log_state = self.config
        #logging.error('b_debug = {}'.format(self.b_debug))

        function = ''

        if ta_str == 'MA':

            #logging.warning('execute() - Moving Average selected - {}'.format(ta_config))
            function = 'Moving Averages'
            column_name = 'ma-{}'.format(ta_config[0])
            record[column_name] = record['close'].rolling(window = ta_config[0], center=False).mean()

        elif ta_str == 'EMA':

            #logging.warning('execute() - Exponential Moving Average selected - {}'.format(ta_config))
            function = 'Exponential Moving Averages'
            column_name = 'ema-{}'.format(ta_config[0])
            record[column_name] = record['close'].ewm(span = ta_config[0], adjust=False).mean()

        elif ta_str == 'STOK':

            #logging.warning('execute() -  Stochastic Oscillator %K selected - {}'.format(ta_config))
            function = 'Stochastic Oscillator %K'
            record['stok'] = pd.Series((record['close'] - record['low']) / (record['high'] - record['low']), name = 'stok')

        elif ta_str == 'STO':

            #logging.warning('execute() -  Stochastic Oscillator %D selected - {}'.format(ta_config))
            function = 'Stochastic Oscillator %D'
            column_name = 'sto-{}'.format(ta_config[0])
            SOk = pd.Series((record['close'] - record['low']) / (record['high'] - record['low']), name = 'stok')
            record[column_name] = SOk.ewm(span = ta_config[0], min_periods = ta_config[0] - 1).mean()

        elif ta_str == 'RSI':

            #logging.warning('execute() - Relative Strenght Index selected - {}'.format(ta_config))
            function = 'Relative Strenght Index'

            i = 0
            UpI = [0]
            DoI = [0]

            while i + 1 <= record.index[-1]:
                UpMove = record.get_value(i + 1, 'high') - record.get_value(i, 'high')
                DoMove = record.get_value(i, 'low') - record.get_value(i + 1, 'low')

                if UpMove > DoMove and UpMove > 0:
                    UpD = UpMove
                else:
                    UpD = 0

                UpI.append(UpD)

                if DoMove > UpMove and DoMove > 0:
                    DoD = DoMove
                else:
                    DoD = 0

                DoI.append(DoD)

                i = i +1

            UpI = pd.Series(UpI)
            DoI = pd.Series(DoI)

            PosDI = UpI.ewm(span = ta_config[0], min_periods = ta_config[0] - 1).mean()
            NegDI = DoI.ewm(span = ta_config[0], min_periods = ta_config[0] - 1).mean()

            column_name = 'rsi-{}'.format(ta_config[0])
            record[column_name] = pd.Series(PosDI / (PosDI + NegDI))

        """
        else:
            logging.warning('execute() - No config found')
        """

        log_txt = '{{TECHNICAL ANALYSIS}}     {}'.format(function)

        result = Record(self.getPos(), (self.row +1, self.column), record, log=log_state, log_txt=log_txt)

        return result

