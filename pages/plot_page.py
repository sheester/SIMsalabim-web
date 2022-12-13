from turtle import width
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Page configuration
st.set_page_config(layout="centered", page_title="SIMsalabim device parameters")
id = str(st.session_state['id'])

SimSS_path = 'SIMsalabim/SimSS/' + id + '/'
data_var = pd.read_csv(SimSS_path+'Var_' + id + '.dat', delim_whitespace=True)
data_jv = pd.read_csv(SimSS_path+'JV_' + id + '.dat', delim_whitespace=True)
# st.write(data_jv)
st.write(data_var)
with st.sidebar:
    options = st.multiselect(
        'Which parameters would you like to plot on the y-axis?',
        list(data_var.columns),
        ['V'],max_selections=2)

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
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()
fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()
# fig,(ax1,ax2)=plt.subplots(1,2)
# ax2.set_yscale(choice_y_scale)
plot_funcs = {'scatter':sns.scatterplot, 'line':sns.lineplot}
# plot_funcs[choice_style](data=data_jv, x='Vext', y='Jext', label='Cell JV', ax=ax1)


# if len(options) == 1:
#     st.write(options)
#     plot_funcs[choice_style](data=data_var, x='x', y=options[0], hue='Vext', ax=ax2)
# elif len(options) > 1:
#     ax2_2 = ax2.twinx()
#     data_var = data_var[data_var['Vext'] == choice_voltage]
#     idx = 0
#     for y_var in options:
#         if idx==0:
#             plot_funcs[choice_style](data=data_var, x='x', y=y_var, ax=ax2, label=y_var, color='b')
#             idx+=1
#         elif idx==1:
#             plot_funcs[choice_style](data=data_var, x='x', y=y_var, ax=ax2_2, label=y_var,color='r')
#     lines, labels = ax2.get_legend_handles_labels()
#     lines2, labels2 = ax2_2.get_legend_handles_labels()
#     ax2.legend(lines+lines2,labels+labels2)
#     ax2_2.legend().remove()
#     ax1.axvline(x=choice_voltage, label='2nd plot V', ls='--', color='grey')
#     ax1.legend()

# Potential [V]
def plot_potential():
    # plot_funcs[choice_style](data=data_var, x='x', y="V", hue='Vext', ax=ax2)
    data = data_var[data_var['Vext'] == choice_voltage]
    plot_funcs[choice_style](data=data, x='x', y="V", ax=ax2)

# plot_potential()

# color = ['b','r','g','k','c','m']
color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'] #standard matplotlib color cycler

# Energy [eV]
def plot_energy():
    i=0
    par = ['Evac','Ec', 'Ev', 'phin', 'phip']
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        i+=1
        plot_funcs[choice_style](data=data, x='x', y=y_var, ax=ax1, label=y_var, color=color[i])
    ax1.set_ylabel('Energy level [eV]')
plot_energy()
 
# Carrier densities [m-3]
def plot_carrier_densities():
    i=0
    par = ['n','p','nion','pion']
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        i+=1
        plot_funcs[choice_style](data=data, x='x', y=y_var, ax=ax2, label=y_var, color=color[i])
    ax2.set_ylabel('Carrier density [ $m^{-3}$ ]')
    ax2.set_yscale('log')
plot_carrier_densities()
        
# Filling Level [a.u.]

def plot_filling_levels():
    i=0
    par = ['ftb1','fti1']
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        i+=1
        plot_funcs[choice_style](data=data, x='x', y=y_var, ax=ax3, label=y_var, color=color[i])
    ax3.set_ylabel('Filling level [ - ]')
plot_filling_levels()

# Transport [m2V-1s-1]
def plot_transport():
    i=0
    par = ['mun','mup']
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        i+=1
        plot_funcs[choice_style](data=data, x='x', y=y_var, ax=ax4, label=y_var, color=color[i])
    ax4.set_ylabel('Transport [ $m^{-2}V^{-1}s^{-1}$ ]')
plot_transport()

# Generation and Recombination [m-3s-1]
def plot_generation_recombination():
    i=0
    par=['Gehp', 'Gfree', 'Rdir','BulkSRHn', 'BulkSRHp', 'IntSRHn', 'IntSRHp']
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        i+=1
        plot_funcs[choice_style](data=data, x='x', y=y_var, ax=ax5, label=y_var, color=color[i])
        ax5.set_ylabel('Generation/Recombination Rate [ $cm^{-3}s^{-1}$ ]')
        # ax5.set_yscale('log')
plot_generation_recombination()

# Currents [Am-3]
def plot_currents():
    i=0
    par=['Jn','Jp','Jtot']
    data = data_var[data_var['Vext'] == choice_voltage]
    for y_var in par:
        i+=1
        plot_funcs[choice_style](data=data, x='x', y=y_var, ax=ax6, label=y_var, color=color[i])
        ax6.set_ylabel('[A}')
plot_currents()

st.pyplot(fig1, format='png')
st.pyplot(fig2, format='png')
st.pyplot(fig3, format='png')
st.pyplot(fig4, format='png')
st.pyplot(fig5, format='png')
st.pyplot(fig6, format='png')

