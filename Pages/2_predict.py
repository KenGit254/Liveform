import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
import yfinance as yf

st.title("🔮 Predict Stock Prices (GRU)")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)")
if ticker:
    df = yf.download(ticker, period="3y")
    df_close = df[["Close"]]
    st.line_chart(df_close)

    data = df_close.values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i - 60:i])
        y.append(scaled_data[i])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = Sequential([
        GRU(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        GRU(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=3, batch_size=32, verbose=0)

    predicted = model.predict(X)
    predicted_prices = scaler.inverse_transform(predicted)

    df_pred = df_close.iloc[60:].copy()
    df_pred["Predicted"] = predicted_prices
    st.line_chart(df_pred)
