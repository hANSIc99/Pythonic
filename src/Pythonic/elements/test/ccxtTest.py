import ccxt, inspect

exchanges = ccxt.exchanges[0]



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

current_exchange = getattr(ccxt, 'bitmex')()

method_list = []

for method in inspect.getmembers(current_exchange, predicate=inspect.ismethod):
    if method[0][:2] != '__' :
        # mit getattr lässt sich die methode dann wieder aufrufen
        method_list.append(method)


current_method = getattr(current_exchange, method_list[33][0])
# symbol, type, side, amount, price, params)
signature = inspect.signature(current_method)

for param in signature.parameters.values() :
    print(param.name)
#https://docs.python.org/3/library/inspect.html
print(type(current_method))
# Inspect call signature
# https://docs.python.org/3.3/library/inspect.html

#binance = ccxt.binance()

#print(binance.status)

# list all exchanges
#print(ccxt.exchanges)