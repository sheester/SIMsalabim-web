import streamlit as st
from subprocess import run,PIPE
from utils import helper_functions as hf
from utils import draw_band_diagram as dbd

# Page configuration
st.set_page_config(layout="wide", page_title="SIMsalabim device parameters")

# Parameters
SimSS_path = 'SIMsalabim/SimSS/'
placeholder = st.empty()
plot_container_title = st.empty()
plot_container = st.empty()
dev_par_object = []

# Load custom CSS to reduce whitespace between rows in columns. Convert disbaled greyed text back to either white or black.

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

local_css('./utils/style.css')

# Functions             
def run_simss():
    with st.spinner('SIMulating...'):
        # Temp code to show console output on browser
        result = run('./simss', cwd=SimSS_path, stdout=PIPE)
    if result.returncode != 0:
        # st.error('SIMsalabim raised an error')
        result_decode = result.stdout.decode('utf-8')
        st.error('Errocode: ' + str(result.returncode) +'\n\n'+result_decode)
    else:
        st.success('Simulation complete')

def save_parameters():
    par_file = hf.write_to_txt(dev_par_object)
    
    # Open the device_parameters file and write content of par_file to it. Close the file afterwards.
    with open(SimSS_path+'device_parameters.txt', 'w') as fp:
        fp.write(par_file)
        fp.close()
        # Draw the band diagram
    get_param_band_diagram(dev_par_object)

def close_figure():
    # Close the band diagram containers
    plot_container = st.empty
    plot_container_title = st.empty

def get_param_band_diagram(dev_par_object): 
    # A fixed list of parameters must be supplied to create the band diagram.
    plot_param = {}
    plot_param_keys = ['L','L_LTL','L_RTL','CB','VB','W_L','W_R','CB_LTL','CB_RTL','VB_LTL','VB_RTL']
    # Find the parameter in the main object and assign it to its key in the dict.
    for section in dev_par_object[1:]:
        for param in section:
            if (param[1] in plot_param_keys):      
                plot_param[param[1]]=param[2]
    # Band diagram will fail when the width the transport layers exceeds the device width. Early exit when this is the case.
    if (float(plot_param['L'])-float(plot_param['L_LTL'])-float(plot_param['L_RTL']) <= 0):
        st.error('Cannot create band diagram, Width of transport layers (L_LTL + L_RTL) is larger than the device width (L)')
    else:
        fig = dbd.create_band_energy_diagram(plot_param)

    # Initialize the plot containers again and split into (virtual) columns to position correctly.
    plot_container_title=st.empty()
    plot_container = st.empty()
    # First place the title and close button in the top container
    with plot_container_title:
        col_plot_t_1, col_plot_t_2, col_plot_t_3 = st.columns([3,4,4])
        with col_plot_t_2:
            st.markdown('''<h3><u>Energy band diagram (eV)</u></h3>''',unsafe_allow_html=True)
        with col_plot_t_3:
            st.button('Close figure', on_click=close_figure)
    # Place the figure in the plot container
    with plot_container:
        col_plot_1, col_plot_2, col_plot_3 = st.columns([3,4,4])
        with col_plot_2:
            st.pyplot(fig)
        with col_plot_3:
            st.markdown('''<em>Note: Band diagram is not to scale</em>''',unsafe_allow_html=True)

#Initialeze but do not render the plot containers
with plot_container_title.container():
        plot_container_title.empty()
with plot_container.container():
        plot_container.empty()

with st.sidebar: 
    st.button('Save device parameters', on_click=save_parameters)

    with open(SimSS_path+'device_parameters.txt') as fo:
        st.download_button('Download device parameters', fo, file_name="device_parameters.txt")
        fo.close()
    
    reset_device_parameters = st.button('Reset device parameters to default')
    st.button('Run SimSS', on_click=run_simss)

# Read the device_parameters.txt file and create a List object
with open(SimSS_path+'device_parameters.txt') as fp:
    dev_par_object = hf.read_from_txt(fp)
    fp.close()

# WHen the reset button is pressed, empty the container and create a List object from the default .txt file. Next, save the default parameters to the parameter file.
if reset_device_parameters:
    placeholder.empty()
    with open(SimSS_path + 'device_parameters_default_1.txt') as fd:
        dev_par_object = hf.read_from_txt(fd)
    save_parameters()

# Build UI layout
with placeholder.container():
    st.title("SIMsalabim device parameters")
    for par_section in dev_par_object:
        if par_section[0]=='Description':
            # Version number
            version=[i for i in par_section if i[1].startswith('version:')]
            # Add version number (from device parameters file) to sidebar
            with st.sidebar:
                st.write("SIMsalabim " + version[0][1])
            # Reference to the SIMsalabim manual
            st.write("""For more information about the device parameters or SIMsalabim itself, refer to the 
                            [Manual](https://raw.githubusercontent.com/kostergroup/SIMsalabim/master/Docs/Manual.pdf)""")
        else: 
            if (par_section[0]== 'Numerical Parameters' or par_section[0]== 'Voltage range of simulation' or par_section[0]== 'User interface'):
                expand=False
            else:
                expand = True
            with st.expander(par_section[0], expanded=expand):
                col_par, col_val, col_desc = st.columns([2,2,8],)
                for item in par_section[1:]:
                    if item[0]=='comm':
                        st.write(item[1])
                        col_par, col_val, col_desc = st.columns([2,2,8])
                    if item[0]=='par':
                        with col_par : 
                            st.text_input(item[1], value=item[1], disabled=True, label_visibility="collapsed")
                            # st.code(item[1],language='markdown')
                        with col_val :
                            item[2] = st.text_input(item[1] + '_val', value=item[2], label_visibility="collapsed")
                        with col_desc :
                            st.text_input(item[1] +'_desc', value=item[3], disabled=True, label_visibility="collapsed")
#st.success('Done!')