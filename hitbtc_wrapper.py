# import libraries, initalize some variables
from time import gmtime, strftime
from urllib import urlencode
import time, csv, os
import numpy as np
import requests

# ------------------------------ #
#       HitBtc Functions         #
# ------------------------------ #

class hitbtc(object):

    # initialize things
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    # for public methods, no need to pass (key, value) pairs or auth
    def query_public_hitbtc(self, method):
        url = 'https://api.hitbtc.com/api/2/public/'
        url += method
        req = requests.get(url)
        return req.json()

    # query methods that have (key, value) pairs, pretty much just order
    def query_hitbtc(self, method, values={}):
        url = 'https://api.hitbtc.com/api/2/'
        url += method
        req = requests.post(url, data=values, auth=(self.key, self.secret))
        return req.json()

    # get pricing data for specific currency pair
    def get_ticker_hitbtc(self, symbol):
        return self.query_public_hitbtc('ticker/%s' % symbol)

    # get all balances
    # TODO: update so this only returns currencies with non-zero balance
    def get_balances_hitbtc(self):
        url = 'https://api.hitbtc.com/api/2/trading/balance'
        req = requests.get(url, auth=(self.key, self.secret))
        return req.json()

    # place a new order, includes "fill or kill" and "immediate or cancel" options
    # fees of 0.1% as noted in hitbtc docs
    def new_order_hitbtc(self, symbol, side, quantity, price, timeInForce):
        return self.query_hitbtc('order', {'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price, 'timeInForce': timeInForce})
