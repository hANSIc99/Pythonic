import time, queue
try:
    from element_types import Record, Function, ProcCMD, GuiCMD
except ImportError:    
    from Pythonic.element_types import Record, Function, ProcCMD, GuiCMD
    
class Element(Function):

    def __init__(self, id, config, inputData, return_queue, cmd_queue):
        super().__init__(id, config, inputData, return_queue, cmd_queue)


    def execute(self):


        #####################################
        #                                   #
        #     REFERENCE IMPLEMENTATION      #
        #                                   #
        #####################################
        specificConfig = self.config.get('SpecificConfig')

        if not specificConfig:

            recordDone = Record(None, message='Trigger: {:04d}'.format(self.config['Identifier']))
            self.return_queue.put(recordDone)
            return

        baseAPI     = None
        pubMethod   = None
        prvMethod   = None
        orderType   = None
        side        = None
        pubSymbol   = None
        prvSymbol   = None
        symbols     = None
        timeframe   = None
        limit       = None     
        amount      = None
        price       = None
        address     = None
        params      = None

        for attrs in specificConfig:
            if attrs['Name'] == 'BaseApi':
                baseAPI = attrs['Data']
            if attrs['Name'] == 'Public Methods':
                pubMethod = attrs['Data']
            elif attrs['Name'] == 'Private Methods':
                prvMethod = attrs['Data']
            elif attrs['Name'] == 'Order Types':
                orderType = attrs['Data']
            elif attrs['Name'] == 'Side':
                side = attrs['Data']
            elif attrs['Name'] == 'SymbolPublic':
                pubSymbol = attrs['Data']
            elif attrs['Name'] == 'SymbolPrivate':
                prvSymbol = attrs['Data']
            elif attrs['Name'] == 'Timeframe':
                timeframe = attrs['Data']
            elif attrs['Name'] == 'LimitData':
                limit = attrs['Data']
            elif attrs['Name'] == 'Tickers':
                symbols = attrs['Data']
            elif attrs['Name'] == 'Amount':
                amount = attrs['Data']
            elif attrs['Name'] == 'Price':
                price = attrs['Data']
            elif attrs['Name'] == 'Address':
               address = attrs['Data']
            elif attrs['Name'] == 'Parameter':
                params = attrs['Data']
        
        #########################################
        #                                       #
        #    The execution exits immediately    #
        #    after providing output data        #
        #                                       #
        #########################################

        if baseAPI == 'Public':
            methodName  = pubMethod
            symbol      = pubSymbol
        else:
            methodName  = prvMethod
            symbol      = prvSymbol


        if methodName == 'create order' and orderType == 'Market':

            methodName = methodName.replace(" ", "_")
            
            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol,
                    'type'      : orderType,
                    'side'      : side,
                    'amount'    : amount
                }
            }

        elif methodName == 'create order' and orderType == 'Limit':

            methodName = methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol,
                    'type'      : orderType,
                    'side'      : side,
                    'amount'    : amount,
                    'price'     : price
                }
            }

        elif methodName == 'create order' :

            methodName = methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'params' : params,
                'kwargs' : {
                    'symbol'    : symbol,
                    'type'      : orderType,
                    'side'      : side,
                    'amount'    : amount,
                    'price'     : price
                }
            }

        elif methodName == 'fetch orders' or        \
             methodName == 'fetch open orders' or   \
             methodName == 'fetch closed orders' or \
             methodName == 'fetch my trades' or     \
             methodName == 'fetch trades' or        \
             methodName == 'fetch order book' or    \
             methodName == 'fetch ticker':
            

            methodName = methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol
                }
            }

        elif methodName == 'fetch tickers':

            
            methodName = methodName.replace(" ", "_")
            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbols'    : symbols
                }
            }

        elif methodName == 'withdraw':

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'code'      : symbol,
                    'amount'    : amount,
                    'address'   : address
                }
            }

        elif methodName == 'fetch OHLCV':

            methodName = methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol,
                    'timeframe' : timeframe,
                    'limit'     : limit
                }
            }

        else:

            methodName = methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName
            }

        recordDone = Record(apiCall)     
        self.return_queue.put(recordDone)