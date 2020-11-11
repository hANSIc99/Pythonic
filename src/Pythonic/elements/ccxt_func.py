import ccxt, inspect
from Pythonic.record_function import Record, Function

# uncomment this during development
#from record_function import Record, Function

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

        method_args     = []

        for key in params:
            if key == 'args':
                varArgs = params['args']
                for varKey in varArgs:
                   
                    # first check if argument can be converted to int
                    try:
                        method_args.append(int(varArgs[varKey]))
                        continue
                    except Exception:
                        pass
                    
                    # second check if value can be converted to float
                    try:
                        method_args.append(float(varArgs[varKey]))
                        continue
                    except Exception:
                        pass

                    method_args.append(varArgs[varKey])
                
            else:
                param_value = params[key]

                # first check if argument can be converted to int
                try:
                    method_args.append(int(param_value))
                    continue
                except Exception:
                    pass
                
                # second check if value can be converted to float
                try:
                    method_args.append(float(param_value))
                    continue
                except Exception:
                    pass
                
                # append argument as it is (string)
                method_args.append(params[key])


        res = method(*method_args)



        log_txt = '{{CCXT}}                   {}::{} CALLED'.format(current_exchange, current_method)
        result = Record(self.getPos(), (self.row +1, self.column), res,
                 log=log_state, log_txt=log_txt)

        return result
