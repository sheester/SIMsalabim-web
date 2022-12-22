"""Device Parameters"""
import os
import shutil
import re
from subprocess import run,PIPE
from werkzeug.utils import secure_filename
import streamlit as st
from utils import parameter_functions as hf
from utils import draw_band_diagram as dbd
from utils import general_functions as gf

######### Page configuration ######################################################################

st.set_page_config(layout="wide", page_title="SIMsalabim device parameters",
                    page_icon='./logo/SIMsalabim_logo_HAT.jpg')

# Load custom CSS
gf.local_css('./utils/style.css')

######### Parameter Initialisation ################################################################

if 'id' not in st.session_state:
    st.error('SIMsalabim simulation has not been initialized yet, return to SIMsalabim page to start a session.')
else:
    # Session ID
    id_session = str(st.session_state['id'])

    # Folder paths
    simss_path = 'SIMsalabim/SimSS/'
    output_path = 'Simulations/'

    # Containers
    placeholder = st.empty()
    bd_container_title = st.empty()
    bd_container_plot = st.empty()

    # Parameters
    dev_par = []
    sc_par={'Simulated':{'Jsc':0, 'Vmpp':0, 'MPP':0, 'Voc':0, 'FF':0}, 'Experimental':{}, 'Deviation':{}}
    st.session_state.key='sc_par'

    ######### Function Definitions ####################################################################

    def run_simss():
        """Run the SIMsalabim simulation executable. When an errocode is returned, display it on the screen.
            When success, copy results, including zip to folder.
        """
        with st.spinner('SIMulating...'):
            # Temp code to show console output on browser
            result = run(['./simss', '../../' + output_path + id_session + '/' + 'device_parameters_' + id_session + '.txt'], cwd=simss_path, stdout=PIPE, check=True)

            # console_decoded = result.stdout.decode('utf-8')
        if result.returncode != 0:
            # SIMsalabim raised an error, print the console output to the screen and exit.
            result_decode = result.stdout.decode('utf-8')
            st.error('Errocode: ' + str(result.returncode) +'\n\n'+result_decode)
        else:
            # SIMsalabim simulation succeeded
            st.success('Simulation complete')

            # Read the console output.
            console_output_decoded = result.stdout.decode('utf-8')

            # Initialize the solar cell parameter object.
            # Set <NA> values for the simulation dict to setup all the avaialble rows
            sc_par={'Simulated':{'Jsc [Am\u207b\u00b2]':'<NA>', 'Vmpp [V]':'<NA>', 'MPP [Wm\u207b\u00b2]':'<NA>', 'Voc [V]':'<NA>', 'FF ':'<NA>'},
                    'Experimental':{},
                    'Deviation':{}}

            #Parameters to indicate whether a solar cell has been simulated. If True, try to read and use the solar cell parameters from the console.
            solar_cell = False
            for line_console in console_output_decoded.split('\n'):
                sc_par,solar_cell = hf.write_scpars(line_console,sc_par,solar_cell)
            for item_numerical_par in dev_par[10]:
                if (item_numerical_par[1]=='ExpJV'):
                    st.session_state['exp_jv_filename'] = item_numerical_par[2]
            if solar_cell is False:
                # Simulation was not for a solar cell. Epty the experimental JV object.
                st.session_state['exp_jv_filename']=''
                sc_par = {}
            # Store the solar cell parameters in memory
            st.session_state['sc_par']=sc_par

            # Move files to an id specific folder
            dir_path=output_path + id_session
            # If folder does not exist yet, create it
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # Verify again of folder has been created correctly to prevent write issues.
            if os.path.exists(dir_path):
                for item_dir_list in os.listdir(simss_path):
                    # Read all files in the standard SimSS output folder. Identify simulation result files by their session_id. Move these files to the id folder.
                    file_path = dir_path + '/' + item_dir_list
                    if id_session in item_dir_list:
                            # Only copy file to id folder but leave a copy in the main folder
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        shutil.move(simss_path + item_dir_list,dir_path)
                
                # Create a ZIP file from the results folder and move to the Simulations folder
                shutil.make_archive('simulation_results_' + id_session , 'zip', dir_path)
                zip_file_name = 'simulation_results_' + id_session + '.zip'
                # If the ZIP archive already exists for this id in the Simulations folder, remove it first.
                if os.path.isfile(output_path + zip_file_name):
                    os.remove(output_path + zip_file_name)
                shutil.move(zip_file_name, output_path)

    def save_parameters():
        """Update output parameter file naming with id and write to txt file.
        """
        # Define the session_id specific filename.
        filename = 'device_parameters_' + id_session + '.txt'

        # Add identifier to output files (as defined in device parameters)
        for item_output_par in dev_par[10]:
            if item_output_par[0]=='par':
                if '.dat' in item_output_par[2] and not id_session in item_output_par[2]:
                    split_par_name = item_output_par[2].split('.dat')
                    item_output_par[2]=split_par_name[0]+'_'+ id_session + '.dat'
                if item_output_par[2]== 'log.txt':
                    item_output_par[2]= 'log_' + id_session + '.txt'

        # Write the device parameter List object to a txt string.
        par_file = hf.write_to_txt(dev_par)

        # Setup an id specific folder
        dir_path=output_path + id_session
        # If folder does not exist yet, create it
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Upon saving a new set of device parameters, remove output files from previous simulation
        for item_dir_list in os.listdir(output_path + id_session):
            if id_session in item_dir_list:
                os.remove(output_path + id_session + '/' + item_dir_list)

        # Open the device_parameters file (in the id folder) and write content of par_file to it. # Close the file afterwards.
        with open(dir_path +'/'+filename, 'w',encoding='utf-8') as fp_device_parameters:
            fp_device_parameters.write(par_file)
            fp_device_parameters.close()

        # Draw the band diagram
        get_param_band_diagram(dev_par)

    def close_figure():
        """Close the band diagram manually.
        """
        # Dummy function to close the band diagram containers

    def get_param_band_diagram(dev_par_bd):
        """Create and display the band diagram based on the relevant parameters from the dict object

        Parameters
        ----------
        dev_par : dict
            Dictionary with all data
        """
        # A fixed list of parameters must be supplied to create the band diagram.
        plot_param = {}
        plot_param_keys = ['L','L_LTL','L_RTL','CB','VB','W_L','W_R','CB_LTL','CB_RTL','VB_LTL','VB_RTL']

        # Find the parameter in the main object and assign it to its key in the dict.
        for section in dev_par_bd[1:]:
            for param in section:
                if param[1] in plot_param_keys:
                    plot_param[param[1]]=param[2]

        # Band diagram will fail when the width the transport layers exceeds the device width. Early exit when this is the case.
        if float(plot_param['L'])-float(plot_param['L_LTL'])-float(plot_param['L_RTL']) <= 0:
            st.error('Cannot create band diagram, Width of transport layers (L_LTL + L_RTL) is larger than the device width (L)')
        else:
            fig = dbd.create_band_energy_diagram(plot_param)

        # Initialize the plot containers again and split into (virtual) columns to position correctly.
        bd_container_title=st.empty()
        bd_container_plot = st.empty()

        # Place the title and close button in the top container
        with bd_container_title:
            col_plot_t_1, col_plot_t_2, col_plot_t_3 = st.columns([3,4,4])
            with col_plot_t_2:
                # Title
                st.markdown('''<h3><u>Energy band diagram (eV)</u></h3>''',unsafe_allow_html=True)
            with col_plot_t_3:
                # Close button
                st.button('Close figure', on_click=close_figure)

        # Place the figure in the plot container
        with bd_container_plot:
            col_plot_1, col_plot_2, col_plot_3 = st.columns([3,4,4])
            with col_plot_2:
                # Band diagram
                st.pyplot(fig)
            with col_plot_3:
                # Scale disclaimer
                st.markdown('''<em>Note: Band diagram is not to scale</em>''',unsafe_allow_html=True)

    def upload_exp_jv():
        """ Read and decode the uploaded experimental jv curve and create a file.
        """
        # Decode the uploaded file (utf-8)
        data = uploaded_file.getvalue().decode('utf-8')

        # Setup the write directory
        target_path = simss_path + uploaded_file.name

        # Write the contents of the uploaded file to a file in the SimSS folder
        destination_file = open(target_path, "w", encoding='utf-8')
        destination_file.write(data)
        destination_file.close()
        return st.success('File upload complete')

    ######### UI layout ###############################################################################

    def verify_up():
        valid,msg = hf.verify_upload_parameter_file('',simss_path)
        if valid is False:
            st.error(msg)
    st.button("tets", on_click=verify_up)

    with st.sidebar:
        # Functionality to upload an experimental JV curve
        chk_expJVcurve = st.checkbox("Upload experimental current voltage characteristic")
        if chk_expJVcurve:
            uploaded_file = st.file_uploader("Select experimental current voltage characteristic",type=['txt'], accept_multiple_files=False, label_visibility='collapsed')
            if uploaded_file is not None:
                bytes_date = uploaded_file.getvalue()
                data = uploaded_file.getvalue().decode('utf-8')
                # validation of the uploaded file: 
                # - Illegal characters
                # - File pattern
                # - Filename length
                msg = ''
                chk_chars = 0
                msg_chars = ''
                chk_pattern = 0
                msg_pattern = ''
                chk_filename = 0
                msg_filename = ''
                # Illegal characters
                if '=' in data or '+' in data or '@' in data or '0x09' in data or '0x0D' in data:
                    chk_chars = 1
                    msg_chars = "Illegal characters used. \n"
                # File pattern
                data = data.splitlines()
                pattern = re.compile("^-?\d*(\.\d*)?\s+-?\d*(\.\d*)?$")
                for line in data[1:]:
                    if not pattern.match(line):
                        chk_pattern = 1
                        msg_pattern = 'File content does not meet the required pattern. \n'
                # Filename lengthand secure the filename.       
                file_name = secure_filename(uploaded_file.name)
                if len(file_name) > 50:
                    print('filename too long. Max 50 characters')
                    chk_filename = 1
                    msg_filename = 'Filename is too long. Max 50 characters'

                if chk_chars + chk_pattern + chk_filename == 0:
                    # All checks passed, allow upload
                    st.button("Upload file to SimSS", on_click=upload_exp_jv)
                    st.markdown('<hr>', unsafe_allow_html=True)
                else:
                    # One or more checks failed. Do not allow upload and show error message
                    st.error(msg_chars + msg_pattern + msg_filename)
                    st.markdown('<hr>', unsafe_allow_html=True)

    with st.sidebar:
        # Device Parameter buttons
        st.button('Save device parameters', on_click=save_parameters)
        if os.path.isfile(output_path + id_session + '/' + 'device_parameters_' + id_session + '.txt'):
            with open(output_path + id_session + '/' +'device_parameters_' + id_session + '.txt', encoding='utf-8') as fo:
                st.download_button('Download device parameters', fo, file_name='device_parameters_' + id_session + '.txt')
                fo.close()
        else:
            with open(simss_path+'device_parameters.txt', encoding='utf-8') as fo:
                st.download_button('Download device parameters', fo, file_name="device_parameters.txt")
                fo.close()

        reset_device_parameters = st.button('Reset device parameters to default')
        st.button('Run SimSS', on_click=run_simss)

    # Load the device_parameters file and create a List object.
    # Check if a session specific file already exists. If True, use this one, else return to the default device_parameters.txt
    if os.path.isfile(output_path + id_session + '/' + 'device_parameters_' + id_session + '.txt'):
        # Session specific parameter file
        with open(output_path + id_session + '/' + 'device_parameters_' + id_session + '.txt', encoding='utf-8') as fp:
            dev_par = hf.read_from_txt(fp)
            fp.close()
    else:
        # Default parameter file
        with open(simss_path+'device_parameters.txt', encoding='utf-8') as fp:
            dev_par = hf.read_from_txt(fp)
            fp.close()

    # When the reset button is pressed, empty the container and create a List object from the default .txt file. Next, save the default parameters to the parameter file.
    if reset_device_parameters:
        placeholder.empty()
        with open(simss_path + 'device_parameters_default_1.txt', encoding='utf-8') as fd:
            dev_par = hf.read_from_txt(fd)
        save_parameters()

    with placeholder.container():
        st.title("SIMsalabim device parameters")
        for par_section in dev_par:
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
