import yfinance as yf
import pandas as pd
import datetime
import dateutil.relativedelta

class Ticker:
    def __init__(self, ticker, period, interval):
        self.ticker = ticker
        self.period = period
        self.interval = interval

    def getData(self):
        data = yf.download(tickers=self.ticker, period=self.period, interval=self.interval)
        return data