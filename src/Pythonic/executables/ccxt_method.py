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

        
        methodName  = None
        orderType   = None
        side        = None
        symbol      = None
        timeframe   = None
        limit       = None     
        amount      = None
        price       = None
        address     = None
        params      = None

        for attrs in self.config['SpecificConfig']:
            if attrs['Name'] == 'Public Methods':
                methodName = attrs['Data']
            elif attrs['Name'] == 'Private Methods':
                methodName = attrs['Data']
            elif attrs['Name'] == 'Order Types':
                orderType = attrs['Data']
            elif attrs['Name'] == 'Side':
                side = attrs['Data']
            elif attrs['Name'] == 'SymbolPublic':
                symbol = attrs['Data']
            elif attrs['Name'] == 'SymbolPrivate':
                symbol = attrs['Data']
            elif attrs['Name'] == 'Timeframe':
                timeframe = attrs['Data']
            elif attrs['Name'] == 'LimitData':
                limit = attrs['Data']
            elif attrs['Name'] == 'Tickers':
                symbol = attrs['Data']
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

        if methodName == 'create order' and orderType == 'Market':

            methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol,
                    'type'      : orderType,
                    'side'      : side,
                    'amount'    : amount,
                    'params'    : params
                }
            }


        elif methodName == 'create order' :

            methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol,
                    'type'      : orderType,
                    'side'      : side,
                    'amount'    : amount,
                    'price'     : price,
                    'params'    : params
                }
            }

        elif methodName == 'fetch orders' or 
             methodName == 'fetch open orders' or 
             methodName == 'fetch closed orders' or
             methodName == 'fetch my trades' or 
             methodName == 'fetch trades' or 
             methodName == 'fetch order book' or 
             methodName == 'fetch ticker' or 
             methodName == 'fetch tickers':

            methodName.replace(" ", "_")

            apiCall = {
                'method' : methodName,
                'kwargs' : {
                    'symbol'    : symbol
                }
            }



        recordDone = Record(None, 'Test')     
        self.return_queue.put(recordDone)