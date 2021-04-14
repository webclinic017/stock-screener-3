from flask import Flask, render_template, request
from patterns import patterns
import yfinance as yf
import os, csv
import pandas as pd
import talib
app = Flask(__name__)

@app.route('/')
def index():
    pattern = request.args.get('pattern', None)
    #pattern2 = request.args.get('pattern2', None)
    stocks = {}
    with open('datasets/nasdaq2.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    if pattern:
        print('starting...........')
        #print(pattern)
        datafiles = os.listdir('datasets/nasdaq2-daily')
        for filename in datafiles:
            df = pd.read_csv('datasets/nasdaq2-daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            #print(pattern_function)
            #pattern_function2 = getattr(talib, pattern2)
            #print(pattern_function2)
            symbol = filename.split('.')[0]
            #print(df)
            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]
                print(last)
                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print('failed on filename: ', filename)

    return render_template('index.html', patterns=patterns, stocks=stocks, current_pattern=pattern)

@app.route('/snapshot')
def snapshot():
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        print(companies)
        for company in companies:
            symbol = company.split(',')[0]
            df = yf.download(symbol, start="2020-10-12", end="2021-04-12")
            df.to_csv('datasets/daily/{}.csv'.format(symbol))
    return {
        'code': 'succes'
    }

