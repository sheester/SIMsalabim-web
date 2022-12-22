"""SIMsalabim Web Application"""
from datetime import datetime, timezone
import streamlit as st
from utils import general_functions as gf

######### Page configuration ######################################################################

st.set_page_config(layout="wide", page_title="SIMsalabim online", page_icon='./logo/SIMsalabim_logo_HAT.jpg')

# Load custom CSS.
gf.local_css('./utils/style.css')

######### Parameter Initialisation ################################################################

# Set an id for the user to identify input/output files. Currently UTC timestamp
if 'id' not in st.session_state:
    id_user = int(datetime.now(timezone.utc).timestamp()*1e6)
    st.session_state.key='id'
    st.session_state['id']=id_user

#  SIMsalabim logo
with st.sidebar:
    st.image('./logo/SIMsalabim_logo_cut_trans.png')

# Introduction
st.title("SIMsalabim online")

st.write(
    "This is a web implementation of the open source [SIMsalabim](https://github.com/kostergroup/SIMsalabim) drift-diffusion simulation package. it currently only allows steady state simulations using SimSS."
)