import streamlit as st
import yfinance as yf
import pandas as pd
import requests

# Company descriptions (add more if needed)
company_info = {
    "Amazon": "Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions.",
    "Tesla": "Tesla, Inc. designs, develops, manufactures electric vehicles and energy storage systems.",
    "NVIDIA": "NVIDIA Corporation designs graphics processing units (GPUs) for gaming and professional markets."
}

# App title
def app():
    st.title("Visuals - Customer Stocks")
    st.write("Select one or more companies to view their individual stock price trends and brief info.")

# API key and multi-select
api_key = st.sidebar.text_input("🔐 Alpha Vantage API Key", type="password")
companies = list(company_info.keys())
selected_companies = st.sidebar.multiselect("Select Companies", companies, default=["Amazon"])

def get_ticker(company_name, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {"function": "SYMBOL_SEARCH", "keywords": company_name, "apikey": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    if "bestMatches" in data and data["bestMatches"]:
        return data["bestMatches"][0]["1. symbol"]
    return None

# Main visualization
if api_key and selected_companies:
    all_data = pd.DataFrame()

    for company in selected_companies:
        ticker = get_ticker(company, api_key)
        if ticker:
            df = yf.download(ticker, period="3y")["Close"]
            df.name = company  # Rename the series for clarity
            all_data = pd.concat([all_data, df], axis=1)

            st.subheader(f"{company} - Closing Price")
            st.line_chart(df)
            st.markdown(company_info.get(company, "No description available."))
            st.markdown("---")

        else:
            st.error(f"❌ Could not find ticker for {company}.")

    if not all_data.empty and len(selected_companies) > 1:
        st.subheader("📊 Combined Chart of All Selected Companies")
        st.line_chart(all_data)
else:
    st.info("ℹ️ Enter your API key and select one or more companies to begin.")
