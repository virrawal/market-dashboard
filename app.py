import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

LITE = os.getenv("LITE_MODE") == "1"

st.set_page_config(page_title="Market Dashboard", layout="wide")
st.title("Market Dashboard (Codespaces)")

# Example: lightweight mode trims history / refresh
HISTORY_DAYS = 90 if LITE else 365*3

st.sidebar.header("Settings")
st.sidebar.write(f"Lite mode: **{LITE}**")
symbol = st.sidebar.text_input("Symbol", value="SPY")

@st.cache_data(ttl=60 if LITE else 15)
def get_prices(sym: str):
    # Replace with your real data pull (Polygon/yfinance/etc)
    idx = pd.date_range(end=pd.Timestamp.utcnow(), periods=HISTORY_DAYS, freq="D")
    df = pd.DataFrame({"close": np.linspace(400, 500, len(idx)) + np.random.randn(len(idx))*3}, index=idx)
    return df

# Fetch prices
df = get_prices(symbol)

# 50/200 DMA demo
df["ma50"] = df["close"].rolling(50).mean()
df["ma200"] = df["close"].rolling(200).mean()

# Display chart
st.line_chart(df[["close", "ma50", "ma200"]])

# Magnificent Seven 50/200-Day Moving Average Status
st.header("Magnificent Seven 50/200-Day Moving Average Status")

MAG7 = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA"]

@st.cache_data(ttl=3600)
def get_ma_indicator(ticker: str):
    data = yf.download(ticker, period="1y")
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA200"] = data["Close"].rolling(window=200).mean()
    data = data.dropna()
    last = data.iloc[-1]
    signal = "Bullish" if last["MA50"] > last["MA200"] else "Bearish"
    return {
        "Ticker": ticker,
        "Close": round(last["Close"], 2),
        "MA50": round(last["MA50"], 2),
        "MA200": round(last["MA200"], 2),
        "Signal": signal,
    }

ma_rows = [get_ma_indicator(t) for t in MAG7]
ma_df = pd.DataFrame(ma_rows)
st.dataframe(ma_df)

st.success("Running inside GitHub Codespaces. Port 8501 is forwarded automatically.")
