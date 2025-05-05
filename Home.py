import streamlit as st

# Import the other pages
import predict
import visual
import output

# Sidebar menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Predict", "Visuals", "Output"])

# Page logic
if menu == "Home":
    st.title("Welcome to the Streamlit App")
    st.write("Use the sidebar to navigate to different sections.")
elif menu == "Predict":
    predict.app()
elif menu == "Visuals":
    visual.app()
elif menu == "Output":
    output.app()