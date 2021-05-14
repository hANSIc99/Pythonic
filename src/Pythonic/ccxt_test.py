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

tickers = exchange.fetch_tickers()



print('end')