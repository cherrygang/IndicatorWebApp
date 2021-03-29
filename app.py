from flask import Flask, request, render_template
import yfinance as yf

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
    hist = quote.history(period=period, interval=interval)
    data = hist.to_json()
    return data

@app.route("/ticker")
def display_everything():
    symbol = request.args.get('ticker', default = "AAPL")
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")
    quote = yf.Ticker(symbol)
    hist = quote.history(period=period, interval=interval)
    data = hist.to_json()
    return render_template('tickerpage.html', data = data)

@app.route("/quote")
def display_quote():
    symbol = request.args.get('symbol', default="AAPL")

    quote = yf.Ticker(symbol)

    return quote.info

if __name__ == "__main__":
    app.run(debug=True)