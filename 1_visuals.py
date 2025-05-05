import streamlit as st
import yfinance as yf
import pandas as pd
import requests

st.title("📊 Visuals - Customer Stocks")

def get_ticker(company_name, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {"function": "SYMBOL_SEARCH", "keywords": company_name, "apikey": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    if "bestMatches" in data and data["bestMatches"]:
        return data["bestMatches"][0]["1. symbol"]
    return None

api_key = st.sidebar.text_input("🔐 Alpha Vantage API Key", type="password")
companies = ["Apple", "Microsoft", "Amazon", "Tesla", "NVIDIA"]
selected = st.sidebar.selectbox("🏢 Select a Company", companies)

if api_key and selected:
    ticker = get_ticker(selected, api_key)
    if ticker:
        st.success(f"Found ticker: {ticker}")
        df = yf.download(ticker, period="3y")
        st.line_chart(df["Close"])
    else:
        st.error("Ticker not found.")
else:
    st.info("Enter API key and select a company.")
