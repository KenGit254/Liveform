import streamlit as st
import pandas as pd

st.title("💰 Investment Estimator")
if "df_pred" not in st.session_state:
    st.warning("⚠️ Please run a prediction first on the 'Predict' page.")
    st.stop()

# Simulate loading prediction (in real use, share data using session_state)
try:
    df_pred = st.session_state["df_pred"]
except KeyError:
    st.warning("Please generate predictions first (go to 'Predict' tab).")
    st.stop()

investment = st.number_input("Investment Amount", min_value=10.0, value=1000.0)
days = st.slider("Investment Duration (days)", 1, len(df_pred)-1, value=30)

start = df_pred["Predicted"].iloc[0]
end = df_pred["Predicted"].iloc[days]

return_ratio = end / start
estimated = investment * return_ratio
profit = estimated - investment

st.markdown(f"""
📅 Period: {days} days  
💸 Initial: ${investment:,.2f}  
📈 Predicted Change: ${start:.2f} → ${end:.2f}  
💵 Estimated Return: ${estimated:,.2f}  
✅ Profit: ${profit:,.2f}
""")
