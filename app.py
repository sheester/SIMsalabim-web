import streamlit as st


st.set_page_config(layout="wide", page_title="SIMsalabim online")
st.title("SIMsalabim online")

st.write(
    "This is a web implementation of the open source [SIMsalabim](https://github.com/kostergroup/SIMsalabim) drift-diffusion simulation package. it currently only allows steady state simulations using SimSS."
)