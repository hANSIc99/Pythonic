import ccxt, inspect, types

exchanges = ccxt.exchanges



print('CCXT Version:', ccxt.__version__)
"""
for exchange_id in ccxt.exchanges:
    try:
        exchange = getattr(ccxt, exchange_id)()
        print(exchange_id)
        # do what you want with this exchange
        name = exchange.name
    except Exception as e:
        print(e)
"""

current_exchange = getattr(ccxt, 'kraken')()

kraken = ccxt.kraken()
kraken.secret = 'secret'
kraken.apiKey = 'api_kay'
def list_methods(t):
    for name, item in type(t).__dict__.items():
        if isinstance(item, types.FunctionType):
            print(name)

#list_methods(current_exchange)
method_list = []

for method in inspect.getmembers(current_exchange, predicate=inspect.ismethod):
    if method[0][:2] != '__' :
        # mit getattr lässt sich die methode dann wieder aufrufen
        method_list.append(method)


current_method = getattr(current_exchange, method_list[29][0])

print('Order name: {}'.format(method_list[29][0]))

#current_exchange.create_limit_order()
# symbol, type, side, amount, price, params)
signature = inspect.signature(current_method)

for param in signature.parameters.values() :
    
    if param.kind == param.POSITIONAL_OR_KEYWORD:
        print(param.name)
    if param.kind == param.VAR_POSITIONAL:
        print('arg* found: {}'.format(param.name))

# input datentyp richtig setzen
#https://stackoverflow.com/questions/22199741/identifying-the-data-type-of-an-input
#https://docs.python.org/3/library/inspect.html
print(type(current_method))
# Inspect call signature
# https://docs.python.org/3.3/library/inspect.html

#binance = ccxt.binance()

#print(binance.status)

# list all exchanges
#print(ccxt.exchanges)