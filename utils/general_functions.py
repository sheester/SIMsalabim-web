"""Functions for general use"""
import streamlit as st

def local_css(file_name):
    """Load a custom CSS file and add it to the application

    Parameters
    ----------
    file_name : string
        path to the CSS file
    """

    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
