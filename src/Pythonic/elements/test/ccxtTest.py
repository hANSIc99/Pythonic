import ccxt

exchanges = ccxt.exchanges[0]



print('CCXT Version:', ccxt.__version__)

for exchange_id in ccxt.exchanges:
    try:
        exchange = getattr(ccxt, exchange_id)()
        print(exchange_id)
        # do what you want with this exchange
        name = exchange.name
    except Exception as e:
        print(e)

print('done')
# Inspect call signature
# https://docs.python.org/3.3/library/inspect.html

#binance = ccxt.binance()

#print(binance.status)

# list all exchanges
#print(ccxt.exchanges)