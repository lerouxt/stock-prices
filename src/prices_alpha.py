#!/usr/bin/env python

import argparse
import requests
import datetime
import jinja2
import sys

def get_latest_price(symbol, apikey):
    symtype, symbol = symbol.split(':')
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=compact&symbol={}&apikey={}'\
        .format(symbol, apikey))
    latest_date = None
    print('Getting getting price for {}'.format(symbol), file=sys.stderr)
    try:
        r.raise_for_status()
        j = r.json()
        latest_date = j['Meta Data']['3. Last Refreshed']
    except:
        print('Error getting price for {}'.format(symbol), file=sys.stderr)
        raise
    latest_date_dt = datetime.datetime.strptime(latest_date, '%Y-%m-%d')
    latest_value = j['Time Series (Daily)'][latest_date]
    return { 'type': symtype.upper(), 'symbol': symbol, 'date': latest_date_dt, 'close_price': float(latest_value['4. close']) }

def get_stocks(stockfile):
    with open(stockfile) as stocks:
        return [ line.strip() for line in stocks ]

def get_stocks_with_prices(apikey, stock_names):
    stocks = []
    for stock in stock_names:
        try:
            stocks.append(get_latest_price(stock, apikey))
        except:
            pass

    return stocks

def get_api_key(apikeyfile):
    with open(apikeyfile) as kf:
        return kf.readline().strip()
    
def template_ofx(stocks_with_prices):
    t = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template('ofx.template')
    r = t.render(stocks=stocks_with_prices, now=datetime.datetime.now())
    print(r)

def main():
    parser = argparse.ArgumentParser(description='Creates OFX with stock prices')
    parser.add_argument('--stockfile', help='File containing stocks', default='stocks.sample')
    parser.add_argument('--apikeyfile', help='File containing API key for alphavantage.co', default='apikey.sample')
    args = parser.parse_args()

    stocks = get_stocks(args.stockfile)
    stocks_with_prices = get_stocks_with_prices(get_api_key(args.apikeyfile), stocks)
    template_ofx(stocks_with_prices)

main()

