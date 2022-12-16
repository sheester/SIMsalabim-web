import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from datetime import datetime
from utils import plot_functions as pf
from utils import general_functions as gf

# Page configuration
st.set_page_config(layout="wide", page_title="SIMsalabim simulation results", page_icon='./logo/SIMsalabim_logo_HAT.jpg')

# Load custom CSS.
gf.local_css('./utils/style.css')

id = str(st.session_state['id'])
SimSS_path = 'SIMsalabim/SimSS/'
output_path = 'Simulations/' + id + '/'
data_var = pd.read_csv(output_path+'Var_' + id + '.dat', delim_whitespace=True)
data_jv = pd.read_csv(output_path+'JV_' + id + '.dat', delim_whitespace=True)

# Increase the font of pyplot graphs for readability
font = {'size' : 14}
matplotlib.rc('font', **font)

# Plot type
plot_funcs = sns.lineplot
# List with available (standard) plot colors
color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'] #standard matplotlib color cycler
# Convert all x positions in the Var.dat file to nm
data_var['x']=data_var['x']*1e9 

with st.sidebar:
    #  List of checkboxes to show/hide plots
    st.subheader('Plots')
    chk_potential=st.checkbox('Potential')
    chk_energy=st.checkbox('Energy band diagram')
    chk_density=st.checkbox('Carrier densities')
    chk_fill=st.checkbox('Filling levels')
    chk_transport = st.checkbox('Transport')
    chk_gen_recomb = st.checkbox('Generation and recombination')
    chk_current = st.checkbox('Current densities')

    # Slider for Vext to update the parameter plots and show curves for the selected Vext.
    voltages = list(set(data_var['Vext']))
    voltages.sort()
    st.markdown('<h4>Voltage (Vext) to plot variables at</h4>',unsafe_allow_html=True)
    choice_voltage = st.select_slider('Voltage to plot variables at', voltages, label_visibility='collapsed')

    # Download Output files
    with open('Simulations/simulation_results_' + str(id) + '.zip', 'rb') as ff:
        id_to_time_string = datetime.fromtimestamp(float(id) / 1e6).strftime("%Y-%d-%mT%H-%M-%SZ")
        filename = 'simulation_result_' + id_to_time_string
        btn = st.download_button(
            label="Download Simulation Results (ZIP)",
            data = ff,
            file_name=filename,
            mime="application/zip"
        )

    #  SIMsalabim logo
    st.markdown('<hr>',unsafe_allow_html=True)
    st.image('./logo/SIMsalabim_logo_cut_trans.png')

scpars_data = st.session_state['scpars']
# Resize the container layout based on the presence of Experimental parameters.

# Initialize the column widths to display the solar cell parameters correctly.
if not scpars_data == {}:
    if 'Experimental' in scpars_data: 
        if len(scpars_data['Experimental'])==0:
            ExpJV = False
            col1_head, col2_head = st.columns([4,2])
        else: 
            col1_head,col2_head= st.columns([2,3])
            ExpJV = True
            expJV_filename = st.session_state['expJV_filename']   
            df_expJV = pd.read_csv (SimSS_path + expJV_filename,sep=' ')
    else:
        col1_head, col2_head = st.columns([4,2])
        ExpJV = False

    with col1_head:
        st.title("Simulation Results")
    with col2_head:
        st.subheader('Solar cell parameters')
        # Show the solar cell parameters (simulated and experimental if available)
        # Remove Experimental and Deviation column from dict when they are not filled. (UseExpData=0)
        if 'Experimental' in scpars_data and len(scpars_data['Experimental'])==0:
            scpars_data.pop('Experimental')
            scpars_data.pop('Deviation')
        # Create a DataFrame from the dict and show in table (readonly)
        df = pd.DataFrame.from_dict(scpars_data, orient='columns')
        st.table(df)

else:
    col1_head, col2_head = st.columns([4,2])
    ExpJV = False
    with col1_head:
        st.title("Simulation Results")

st.markdown('<hr>', unsafe_allow_html=True)
# col1,col2= st.columns([2,3])
col1,col2,col3 = st.columns([2,5,2])

with col2:
    # Show the JV curve. Always visible
    fig1, ax1 = plt.subplots()
    if ExpJV == True:
        ax1 = pf.plot_jv_curve(data_jv,choice_voltage, plot_funcs,ax1, ExpJV, df_expJV)
    else:
        ax1 = pf.plot_jv_curve(data_jv,choice_voltage, plot_funcs,ax1, ExpJV )
    st.pyplot(fig1, format='png')

    # Show the output plot when sidebar box is checked
    # Potential 
    if chk_potential:
        fig2, ax2 = plt.subplots()
        ax2 = pf.plot_potential(data_var, choice_voltage, plot_funcs, ax2, color)
        st.pyplot(fig2, format='png')

    # Energy
    if chk_energy:
        fig3, ax3 = plt.subplots()
        ax3 = pf.plot_energy(data_var, choice_voltage, plot_funcs, ax3, color)
        st.pyplot(fig3, format='png')

    # Carrier Density
    if chk_density:
        fig4, ax4 = plt.subplots()
        ax4 = pf.plot_carrier_densities(data_var, choice_voltage, plot_funcs, ax4, color)
        st.pyplot(fig4, format='png')

    # Filling Factor    
    if chk_fill: 
        fig5, ax5 = plt.subplots()   
        ax5 = pf.plot_filling_levels(data_var, choice_voltage, plot_funcs, ax5, color)
        st.pyplot(fig5, format='png')

    # Transport
    if chk_transport:
        fig6, ax6 = plt.subplots()
        ax6 = pf.plot_transport(data_var, choice_voltage, plot_funcs, ax6, color)
        st.pyplot(fig6, format='png')

    # Generation and Recombination
    if chk_gen_recomb:
        fig7, ax7 = plt.subplots()
        ax7 = pf.plot_generation_recombination(data_var, choice_voltage, plot_funcs, ax7, color)
        st.pyplot(fig7, format='png')

    # Current
    if chk_current:
        fig8, ax8 = plt.subplots()
        ax8= pf.plot_currents(data_var, choice_voltage, plot_funcs, ax8, color)
        st.pyplot(fig8, format='png')