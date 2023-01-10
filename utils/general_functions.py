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

def fatal_error_message(errorcode):
    """When a 'standard' fatal error occurs, add a standard error message

    Parameters
    ----------
    errorcode : int
        the error code
    """    
    message = ''
    if errorcode == 106:
        message = 'Invalid numeric format: Reported when a non-numeric value is read from a text file'
    elif errorcode == 200:
        message = 'Division by zero: The application attempted to divide a number by zero.'
    elif errorcode == 201:
        message = 'Range check error.'
    elif errorcode == 202:
        message = 'Stack overflow error: This error is only reported when stack checking is enabled.'
    elif errorcode == 205:
        message = 'Floating point overflow.'
    elif errorcode == 206:
        message = 'Floating point underflow.'
    else:
        message = 'A fatal error occured.'
    return message