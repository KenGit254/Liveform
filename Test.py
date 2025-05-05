import streamlit as st
import pandas as pd

def app():
    st.title("💵 Investment Return Estimator")

    if "df_pred" not in st.session_state:
        st.warning("⚠️ Please run a prediction first on the 'Predict' page.")
        st.stop()

    df_pred = st.session_state["df_pred"]

    if "Predicted" not in df_pred.columns:
        st.error("❌ Prediction data missing. Please run the model first.")
        st.stop()

    st.subheader("📈 Predicted Closing Prices")
    st.line_chart(df_pred["Predicted"])

    # 💰 Investment simulation
    st.subheader("💸 Investment Simulation")
    investment_amount = st.number_input("Investment Amount (USD)", min_value=10.0, value=1000.0)
    investment_days = st.slider("Investment Duration (Days)", min_value=1, max_value=len(df_pred)-1, value=30)

    if investment_days >= len(df_pred):
        st.warning("⚠️ Investment duration exceeds available prediction range.")
    else:
        start_price = df_pred["Predicted"].iloc[0]
        end_price = df_pred["Predicted"].iloc[investment_days]

        ratio = end_price / start_price
        estimated_return = investment_amount * ratio
        profit = estimated_return - investment_amount

        st.markdown(f"""
        📅 **Period**: {investment_days} days  
        💰 **Initial Investment**: ${investment_amount:,.2f}  
        📈 **Predicted Price**: ${start_price:.2f} → ${end_price:.2f}  
        💵 **Estimated Return**: ${estimated_return:,.2f}  
        ✅ **Estimated Profit**: ${profit:,.2f}
        """)
