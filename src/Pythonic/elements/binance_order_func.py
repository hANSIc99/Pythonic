from pythonic_binance.client import Client
from Pythonic.record_function import Record, Function

class BinanceOrderFunction(Function):

    def __init(self, config, b_debug, row, column):

        super().__init__(config, b_debug, row, column)
        #logging.debug('__init__() called BinanceOHLCFUnction')

    def execute(self, record):

        
        pub_key, prv_key, side_index, side_txt, symbol_txt, quantity, \
                order_index, order_string, order_config, log_state = self.config

        timeInForce = None
        stopPrice   = None
        price       = None

        client = Client(pub_key, prv_key)

        if order_string == 'MARKET':

            if isinstance(record, dict):
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    )

        elif order_string == 'LIMIT':

            timeInForce = order_config[0]
            price       = '{:.8f}'.format(order_config[2])

            if isinstance(record, dict):
                if 'price' in record: 
                    price = '{:.8f}'.format(record['price'])
                if 'quantity' in record: 
                    quantity = record['quantity']
                if 'type' in record: 
                    timeInForce = record['type']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    timeInForce = timeInForce,
                    price       = price,
                    )

        elif order_string == 'STOP_LOSS':

            stopPrice   = '{:.8f}'.format(order_config[0])

            if isinstance(record, dict):
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    stopPrice   = stopPrice
                    )

        elif order_string == 'STOP_LOSS_LIMIT':

            timeInForce = order_config[0]
            price       = '{:.8f}'.format(order_config[2])
            stopPrice   = '{:.8f}'.format(order_config[3])

            if isinstance(record, dict):
                if 'price' in record: 
                    price = '{:.8f}'.format(record['price'])
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']
                if 'type' in record: 
                    timeInForce = record['type']


            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    timeInForce = timeInForce,
                    price       = price,
                    stopPrice   = stopPrice
                    )

        elif order_string == 'TAKE_PROFIT':

            stopPrice   = '{:.8f}'.format(order_config[0])

            if isinstance(record, dict):
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']



            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    stopPrice   = stopPrice
                    )

        elif order_string == 'TAKE_PROFIT_LIMIT':

            timeInForce = order_config[0]
            price       = '{:.8f}'.format(order_config[2])
            stopPrice   = '{:.8f}'.format(order_config[3])

            if isinstance(record, dict):
                if 'price' in record: 
                    price = '{:.8f}'.format(record['price'])
                if 'stopPrice' in record: 
                    stopPrice = '{:.8f}'.format(record['stopPrice'])
                if 'quantity' in record: 
                    quantity = record['quantity']
                if 'type' in record: 
                    timeInForce = record['type']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity),
                    timeInForce = timeInForce,
                    price       = price,
                    stopPrice   = stopPrice
                    )

        elif order_string == 'LIMIT_MAKER':

            if isinstance(record, dict):
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity)
                    )

        elif order_string == 'MARKET':

            if isinstance(record, dict):
                if 'quantity' in record: 
                    quantity = record['quantity']

            order = client.create_order(
                    symbol      = symbol_txt,
                    side        = side_txt,
                    type        = order_string,
                    quantity    = '{:.8f}'.format(quantity)
                    )


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

        log_txt = '{{BINANCE ORDER}}          {} ORDER EXECUTED'.format(order_string)
        result = Record(self.getPos(), (self.row +1, self.column), order,
                 log=log_state, log_txt=log_txt)

        return result
