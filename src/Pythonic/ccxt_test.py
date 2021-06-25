import ccxt

sId = 'binance'

exchangeClass = getattr(ccxt, sId)

# https://github.com/ccxt/ccxt/wiki/Manual#overview
# Ein Element mit Schalter für Public/Private
"""
exchange = exchangeClass({
    'apiKey'            : 'YPUR_API_KEY', # text
    'secret'            : 'SECRET_KEY', #text
    'timeout'           : 30000, # milliseconds unsigned int
    'enableRateLimit'   : True,  # checkbox
})
"""
exchange = exchangeClass({'enableRateLimit'   : True})
exchange = ccxt.binance()

#tickers = exchange.fetch_tickers() # keine argumente
#if exchange.has['fetchOHLCV']: #https://github.com/ccxt/ccxt/wiki/Manual#ohlcv-candlestick-charts
#def myfunc2(*args, **kwargs): hier mit arbeiten


# Public API 

lmarkets = exchange.load_markets()
fmarkets = exchange.fetch_markets()
currencies = exchange.fetch_currencies()
ticker = exchange.fetch_ticker('ETH/BTC')
tickers = exchange.fetch_tickers('ETH/BTC XMR/BTC ADA/BNB')
orderbook = exchange.fetch_order_book('ADA/BNB')

ohlcv = exchange.fetch_ohlcv('ADA/BNB', timeframe='1m', limit=500)
exchange.fetch_ohlcv()
#since = UTC timestamp in milliseconds

#status = exchange.fetch_status()

#trades = exchange.fetch_trades('ADA/BNB')


# Private API

balance = = exchange.fetch_balance()

order = exchange.create_order('ETH/BTC', 'Market/limit/stoploss/stoplosslimit/', 'buy/sell', 123.455, price)

fetch_orders = exchange.fetch_orders('ETH/BTC')

fetch_open_orders = exchange.fetch_open_orders('ETH/BTC')

fetch_closed_orders = exchange.fetch_closed_orders('ETH/BTC')

my_trades = exchange.fetch_my_trades('ETH/BTC')

withdraw = exchange.withdraw('BTC', amount, adress)
exchange.withdraw()

print('end')