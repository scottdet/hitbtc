# import libraries, initalize some variables
from time import gmtime, strftime
from urllib import urlencode
import time, csv, os
import numpy as np
import requests

auth = ("public", "secret")

# list of portfolio assets
pairs = ['BCCBTC', 'BCCETH', 'ETHBTC']
data = []

# for public methods, no need to pass (key, value) pairs or auth
def query_public(method):
	url = 'https://api.hitbtc.com/api/2/public/'
	url += method
	req = requests.get(url)
	return req.json()

# query methods that have (key, value) pairs, pretty much just order
def query(method, values={}):
	url = 'https://api.hitbtc.com/api/2/'
	url += method
	req = requests.post(url, data=values, auth=auth)
	return req.json()

# get pricing data for specific currency pair
def get_ticker(symbol):
	return query_public('ticker/%s' % symbol)

# get all balances
# TODO: update so this only returns currencies with non-zero balance
def get_balances():
	url = 'https://api.hitbtc.com/api/2/trading/balance'
	req = requests.get(url, auth=auth)
	return req.json()

# place a new order, includes "fill or kill" and "immediate or cancel" options
# fees of 0.1% as noted in hitbtc docs
def new_order(symbol, side, quantity, price, timeInForce):
	return query('order', {'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price, 'timeInForce': timeInForce})
 
# --------------- #
#    main loop    #
# --------------- #

if __name__ == "__main__":

	while(True):
		# append the dater
		date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		data.append(date)

		# loop to get available balances as an example
		balances = get_balances()
		for i in range(len(balances)):
			if balances[i]['currency'] == 'BTC':
				x1 = balances[i]['available']
			if balances[i]['currency'] == 'ETH':
				y1 = balances[i]['available']
			if balances[i]['currency'] == 'OMG':
				z1 = balances[i]['available']

		# loop to get data for all currency pairs
		for j in range(len(pairs)):
			summaries = get_ticker(pairs[j])
			bid = float(summaries['bid'])
			ask = float(summaries['ask'])

			data.append(bid)
			data.append(ask)