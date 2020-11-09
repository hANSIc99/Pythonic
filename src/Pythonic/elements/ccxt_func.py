import ccxt

from record_function import Record, Function
#from Pythonic.record_function import Record, Function

class CCXTFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        
        # exchange, api_key, sec_key, method, params, log_state
        current_exchange, api_key, sec_key, \
            current_method, params, log_state = self.config


        exchange        = getattr(ccxt, current_exchange)()
        exchange.apiKey = api_key
        exchange.secret = sec_key

        method          = getattr(exchange, current_method)


        for param in params:
            #BAUSTELLE: Checken ob ein dict vorkommt [args]
            if  (isinstance(param, VarPositionalParser) and
                'args' in self.current_params ):


                for argName, argVal in self.current_params['args'].items():
                    param.addArgument(argName, argVal)
            else:
                key =  param.objectName()
                if key in self.current_params:
                    param.setText(self.current_params[key])

        res = method(**params)
        order = 'hey'
        """
        logging.error('Order: {}'.format(order)) 
        logging.error('symbol = {}'.format(symbol_txt))
        logging.error('side = {}'.format(side_txt))
        logging.error('type = {}'.format(order_string))
        logging.error('quantity = {}'.format(quantity))
        logging.error('timeInForce = {}'.format(timeInForce))
        logging.error('price = {}'.format(price))
        logging.error('stopPrice = {}'.format(stopPrice))
        """

        log_txt = '{{CCXT}}                   {} {} EXECUTED'.format('test1', 'test2')
        result = Record(self.getPos(), (self.row +1, self.column), order,
                 log=log_state, log_txt=log_txt)

        return result
