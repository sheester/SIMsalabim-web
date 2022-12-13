import streamlit as st
from datetime import datetime, timezone

st.set_page_config(layout="wide", page_title="SIMsalabim online")
st.title("SIMsalabim online")

st.write(
    "This is a web implementation of the open source [SIMsalabim](https://github.com/kostergroup/SIMsalabim) drift-diffusion simulation package. it currently only allows steady state simulations using SimSS."
)

# Set an id for the user to identify input/output files. Currently UTC timestamp
id_user = int(datetime.now(timezone.utc).timestamp()*1e6)
st.session_state.key='id'
st.session_state['id']=id_user
