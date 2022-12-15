import streamlit as st
from datetime import datetime, timezone
from utils import general_functions as gf

st.set_page_config(layout="wide", page_title="SIMsalabim online", page_icon='./logo/SIMsalabim_logo_HAT.jpg')

# Load custom CSS to reduce whitespace between rows in columns. Convert disbaled greyed text back to either white or black.

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

gf.local_css('./utils/style.css')

#  SIMsalabim logo
with st.sidebar:
    st.image('./logo/SIMsalabim_logo_cut_trans.png')

st.title("SIMsalabim online")

st.write(
    "This is a web implementation of the open source [SIMsalabim](https://github.com/kostergroup/SIMsalabim) drift-diffusion simulation package. it currently only allows steady state simulations using SimSS."
)

# Set an id for the user to identify input/output files. Currently UTC timestamp
id_user = int(datetime.now(timezone.utc).timestamp()*1e6)
st.session_state.key='id'
st.session_state['id']=id_user