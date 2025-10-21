import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import numpy as np

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

st.success("Running inside GitHub Codespaces. Port 8501 is forwarded automatically.")
