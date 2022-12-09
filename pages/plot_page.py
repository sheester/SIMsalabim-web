from turtle import width
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Page configuration
st.set_page_config(layout="centered", page_title="SIMsalabim device parameters")

SimSS_path = 'SIMsalabim/SimSS/'
data_var = pd.read_csv(SimSS_path+'Var.dat', delim_whitespace=True)
data_jv = pd.read_csv(SimSS_path+'JV.dat', delim_whitespace=True)
st.write(data_jv)
st.write(data_var)
with st.sidebar:
    options = st.multiselect(
        'Which parameters would you like to plot on the y-axis?',
        list(data_var.columns),
        ['V'])

    scale_y = ['linear','log']
    choice_y_scale = st.selectbox('y-scale', scale_y)

    style = ['line','scatter']
    choice_style = st.selectbox('plot style', style)

    voltages = list(set(data_var['Vext']))
    voltages.sort()
    format_func = lambda volt : f'{volt:.2}'
    choice_voltage = st.select_slider('Voltage to plot variables at', voltages, format_func=format_func)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
# fig,(ax1,ax2)=plt.subplots(1,2)

ax2.set_yscale(choice_y_scale)
plot_funcs = {'scatter':sns.scatterplot, 'line':sns.lineplot}
plot_funcs[choice_style](data=data_jv, x='Vext', y='Jext', label='Cell JV', ax=ax1)


if len(options) == 1:
    plot_funcs[choice_style](data=data_var, x='x', y=options[0], hue='Vext', ax=ax2)
elif len(options) > 1:
    data_var = data_var[data_var['Vext'] == choice_voltage]
    for y_var in options:
        plot_funcs[choice_style](data=data_var, x='x', y=y_var, ax=ax2, label=y_var)

    ax1.axvline(x=choice_voltage, label='2nd plot V', ls='--', color='grey')
    ax1.legend()

st.pyplot(fig1, format='png')
st.pyplot(fig2, format='png')