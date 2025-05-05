import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

st.set_page_config(page_title="Stock Predictor", layout="centered")

st.title("🔮 Stock Prediction & 💰 Investment Estimator")

# Alpha Vantage API Key
api_key = st.sidebar.text_input("🔐 Enter Alpha Vantage API Key", type="password")

# Company name input
company_name = st.text_input("🏢 Enter Company Name (e.g., Tesla, Amazon)")

# Predict button
predict_button = st.button("🔮 Predict")

# Function to fetch ticker using Alpha Vantage
def get_ticker(company_name, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": company_name,
        "apikey": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if "bestMatches" in data and data["bestMatches"]:
        return data["bestMatches"][0]["1. symbol"]
    return None

# Process when button is clicked
if predict_button:
    if not api_key or not company_name:
        st.warning("⚠️ Please provide both API key and company name.")
        st.stop()

    ticker = get_ticker(company_name, api_key)
    if not ticker:
        st.error("❌ Could not find a ticker for the provided company.")
        st.stop()

    df = yf.download(ticker, period="3y")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    if "Close" not in df.columns:
        st.error("❌ 'Close' column not found in the downloaded data.")
        st.stop()

    df_close = df[["Close"]]
    st.subheader(f"📊 Historical Close Prices for {company_name.title()} ({ticker})")
    st.line_chart(df_close)

    # Data Preprocessing
    data = df_close.values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    seq_len = 60
    for i in range(seq_len, len(scaled_data)):
        X.append(scaled_data[i - seq_len:i])
        y.append(scaled_data[i])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # GRU Model
    model = Sequential([
        GRU(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        GRU(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=3, batch_size=32, verbose=0)

    predicted = model.predict(X)
    predicted_prices = scaler.inverse_transform(predicted)

    df_pred = df_close.iloc[seq_len:].copy()
    df_pred["Predicted"] = predicted_prices

    st.subheader("📈 Actual vs Predicted Closing Prices (GRU Model)")
    st.line_chart(df_pred[["Close", "Predicted"]])

    # Investment Estimator
    st.subheader("💵 Investment Return Estimator")
    investment_amount = st.number_input("Enter Investment Amount (USD)", min_value=10.0, value=1000.0)
    investment_days = st.slider("Investment Duration (Days)", min_value=1, max_value=len(df_pred) - 1, value=30)

    start_price = df_pred["Predicted"].iloc[0]
    end_price = df_pred["Predicted"].iloc[investment_days]
    ratio = end_price / start_price
    estimated_return = investment_amount * ratio
    profit = estimated_return - investment_amount

    st.markdown(f"""
    📅 **Period**: {investment_days} days  
    💸 **Initial Investment**: ${investment_amount:,.2f}  
    📈 **Predicted Price**: ${start_price:.2f} → ${end_price:.2f}  
    💵 **Estimated Return**: ${estimated_return:,.2f}  
    ✅ **Estimated Profit**: ${profit:,.2f}
    """)

    # Insight
    if ratio > 1.05:
        st.success("📈 The model predicts a significant upward trend. A potentially profitable opportunity.")
    elif ratio < 0.95:
        st.warning("📉 The model shows a declining trend. Caution advised before investing.")
    else:
        st.info("⏳ The trend appears neutral. Returns might be limited.")
