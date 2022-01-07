import time, queue
import ccxt
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


        eId     = None
        pubKey  = None
        prvKey  = None


        for attrs in specificConfig:
            if attrs['Name'] == 'ExchangeId':
                eId = attrs['Data']
            if attrs['Name'] == 'PubKey':
                pubKey = attrs['Data']
            elif attrs['Name'] == 'PrvKey':
                prvKey = attrs['Data']


        exchangeClass = getattr(ccxt, eId)
        if pubKey and prvKey:

             exchange = exchangeClass( {
                                        'apiKey'            : pubKey,
                                        'secret'            : prvKey,
                                        'enableRateLimit'   : True
             })

        else:
            exchange = exchangeClass( {'enableRateLimit'   : True})

        method = getattr(exchange, self.inputData['method'])

        kwargs  = None
        params  = None
        
        if not 'kwargs' in self.inputData:

            data = method()

        elif not 'params' in self.inputData:
            
            kwargs = self.inputData['kwargs']
            data = method(**kwargs)

        else: 

            kwargs = self.inputData['kwargs']
            params = self.inputData['params']

            if params != '':
                data = method(**kwargs, params=params)
            else:
                data = method(**kwargs)

           
        recordDone = Record(data, '{}() successfull'.format(self.inputData['method']))     
        self.return_queue.put(recordDone)