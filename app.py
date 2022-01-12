from flask import Flask, request, render_template
import yfinance as yf
import functions
import json
import numpy as np
import chart_studio.plotly as plotly
import chart_studio.plotly.plotly as py
import plotly.graph_objects as go
import plotly.utils as putil
import datetime

# debugging stuff. Delete this later if no longer needed
from pprint import pprint
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/history")
def display_history():
    symbol = request.args.get('symbol', default="AAPL")
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")
    quote = yf.Ticker(symbol)
    #hist = quote.history(period=period, interval=interval)
    #data = hist.to_json()
    data = 'some test stuff'
    return {data:'test'}

@app.route("/ticker")
def display_everything():
    symbol = request.args.get('ticker', default = "AAPL")
    # period = request.args.get('period', default="1y")
    # interval = request.args.get('interval', default="1mo")
    # quote = yf.Ticker(symbol)
    # hist = quote.history(period=period, interval=interval)
    # data = hist.to_json()
    tick = functions.Ticker(symbol, '12mo', '1d')
    df = tick.getData()

    dftable = df.to_html()
    df.reset_index()
    # data1['newdate'] = datetime.datetime.strptime(data1['date'], '%Y-%m-%d %H:%M:%S')

    # for index, row in df.iterrows():
    #     print(row['Open'], row['Close'])

    trace = go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )



    data = [trace]
    
    graphJSON = json.dumps(data, cls=putil.PlotlyJSONEncoder)


    

    return render_template('tickerpage.html', graphJSON=graphJSON, dftable = dftable)

@app.route("/quote")
def display_quote():
    symbol = request.args.get('symbol', default="AAPL")

    quote = yf.Ticker(symbol)

    return quote.info

if __name__ == "__main__":
    app.run(debug=True)