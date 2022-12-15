import streamlit as st
import os
import shutil
from subprocess import run,PIPE
from utils import parameter_functions as hf
from utils import draw_band_diagram as dbd
from utils import general_functions as gf

# Page configuration
st.set_page_config(layout="wide", page_title="SIMsalabim device parameters", page_icon='./logo/SIMsalabim_logo_HAT.jpg')

# Parameters
id = str(st.session_state['id'])
SimSS_path = 'SIMsalabim/SimSS/'
placeholder = st.empty()
plot_container_title = st.empty()
plot_container = st.empty()
dev_par_object = []

# Load custom CSS
gf.local_css('./utils/style.css')

# Functions             
def run_simss():
    """Run the SIMsalabim simulation executable. When an errocode is returned, display it on the screen. 
        When success, copy results, including zip to folder.
    """    
    with st.spinner('SIMulating...'):
        # Temp code to show console output on browser
        result = run(['./simss', 'device_parameters_' + str(id) + '.txt'], cwd=SimSS_path, stdout=PIPE)
    if result.returncode != 0:
        # st.error('SIMsalabim raised an error')
        result_decode = result.stdout.decode('utf-8')
        st.error('Errocode: ' + str(result.returncode) +'\n\n'+result_decode)
    else:
        st.success('Simulation complete')
        
        # Move files to a id specific folder
        dir_name=str(id)
        # If folder does not exist yet, create it
        if not os.path.exists(SimSS_path + dir_name):
            os.makedirs(SimSS_path + dir_name)
        
        # Verify again of folder has been created correctly to prevent write issues.
        if os.path.exists(SimSS_path + dir_name):
            for item in os.listdir(SimSS_path):
                if str(id) in item:
                    if not 'device_parameters' in item:
                        # copy to id folder and remove files from main folder
                        if os.path.isfile(SimSS_path + dir_name + '/' + item):
                            os.remove(SimSS_path + dir_name + '/' + item)
                        shutil.move(SimSS_path + item,SimSS_path + dir_name)
                    else:
                        # Only copy file to id folder but leave a copy in the main folder
                        if os.path.isfile(SimSS_path + dir_name + '/' + item):
                            os.remove(SimSS_path + dir_name + '/' + item)
                        shutil.copy(SimSS_path + item,SimSS_path + dir_name)
            # Create a ZIP file from the results and move to the id folder
            shutil.make_archive('simulation_results_' + str(id) , 'zip', SimSS_path + str(id))
            shutil.move('simulation_results_' + str(id) + '.zip', SimSS_path + str(id))

def save_parameters():
    """Update output parameter file naming with id and write to txt file.
    """    
    filename = 'device_parameters_' + str(id) + '.txt'
    
    # Add identifier to output files
    for item in dev_par_object[10]:
        if (item[0]=='par'):
            if '.dat' in item[2]:
                split_par_name = item[2].split('.dat')
                item[2]=split_par_name[0]+'_'+ str(id) + '.dat'
            if item[2]== 'log.txt':
                item[2]= 'log_' + str(id) + '.txt'

    par_file = hf.write_to_txt(dev_par_object)

    # Open the device_parameters file and write content of par_file to it. Close the file afterwards.
    # with open(SimSS_path+'device_parameters.txt', 'w') as fp:

    with open(SimSS_path+filename, 'w') as fp:
        fp.write(par_file)
        fp.close()
        # Draw the band diagram
    get_param_band_diagram(dev_par_object)
    # return timestamp_now


def close_figure():
    """CLose the band diagram manually.
    """    
    # Close the band diagram containers
    plot_container = st.empty
    plot_container_title = st.empty

def get_param_band_diagram(dev_par_object): 
    """Create and display the band diagram based on the relevant parameters from the dict object

    Parameters
    ----------
    dev_par_object : dict
        Dictionary with all data
    """    
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
            # Add version number (from device parameters file)
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
                            if item[1]== 'Pause_at_end':
                                item[2] = st.text_input(item[1] + '_val', value=item[2],disabled=True, label_visibility="collapsed")
                            else:
                                item[2] = st.text_input(item[1] + '_val', value=item[2], label_visibility="collapsed")
                        with col_desc :
                            st.text_input(item[1] +'_desc', value=item[3], disabled=True, label_visibility="collapsed")
#st.success('Done!')

#  SIMsalabim logo
with st.sidebar:
    st.markdown('<hr>',unsafe_allow_html=True)
    st.image('./logo/SIMsalabim_logo_cut_trans.png')