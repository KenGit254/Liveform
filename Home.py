import streamlit as st

# Import the other pages
import visual
import predict
import output

# Sidebar menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Visuals", "Predict", "Output"])

# Page logic
if menu == "Home":
    st.title("Welcome to the Streamlit App")
    st.write("Use the sidebar to navigate to different sections.")
elif menu == "Visuals":
    visual.app()
elif menu == "Predict":
    predict.app()
elif menu == "Output":
    output.app()