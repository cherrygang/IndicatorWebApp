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
        #download data from yf
        data = yf.download(tickers=self.ticker, period=self.period, interval=self.interval)

        #add additional data for screening
        data['50MA'] = data.Close.rolling(50).mean()
        data['200MA'] = data.Close.rolling(200).mean()
        data['RSI'] = self.getRSI(data['Close'], 14)
        data['MACD'] = self.getMACD(data['Close'])
        data['9dEMA'] = self.getEMA(data['Close'], 9)
        data['20dEMA'] = self.getEMA(data['Close'], 20)
        
        #based off of whatever indicators we need to set signal to -1, 0, 1 [sell, hold, buy] e.g.
        data['Signal'] = self.testingRSI(data['Close'])

        return data

    def getRSI(self, data, time_window):
        diff = data.diff(1).dropna()
        gain_chg = 0 * diff
        loss_chg = 0 * diff
        gain_chg[diff > 0] = diff[diff > 0]
        loss_chg[diff < 0] = diff[diff < 0]
        gain_chg_avg = gain_chg.ewm(com=time_window-1, min_periods=time_window).mean()
        loss_chg_avg = loss_chg.ewm(com=time_window-1, min_periods=time_window).mean()

        rs = abs(gain_chg_avg/loss_chg_avg)
        rsi = 100-100/(1+rs)
        return rsi

    def getMACD(self, data):
        return self.getEMA(data,12)-self.getEMA(data,26)

    def getEMA(self,data,time_frame):
        return data.ewm(span=time_frame,adjust=False).mean()

    def testingRSI(self, data):
        if isinstance(data, float):
            if data > 30:
                return 1
        return 0

    def lineCross(self, line1, line2, lookback):
        #if line1 is initially lower than line 2 & cross then return True
        try:
            if (line1.iloc[-lookback]-line2.iloc[-lookback]<0):
                if (line1.iloc[-1]-line2.iloc[-1]>0):
                    return True
                return False
        except IndexError:
            return False