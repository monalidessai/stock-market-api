import yfinance as yf

def get_current_price(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")

    if data.empty:
        return None

    return round(float(data["Close"].iloc[-1]), 2)