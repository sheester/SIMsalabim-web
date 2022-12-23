"""Functions for page: device_parameters"""
import os
import random

def read_from_txt(fp):
    """Read the opened .txt file line by line and store all in the dev_par_object.

    Parameters
    ----------
    fp : TextIOWrapper
        filepointer to the opened .txt file.

    Returns
    -------
    List
        List with nested lists for all parameters in all sections.
    """
# Note:         List object format (basic layout) Identical strucutre for all sections
#
#               [
#                   [
#                       'Description',
#                       ['comm', {comment1}],
#                       ['comm', {comment2}],
#                           ...
#                   ],
#                   [   'General',
#                       ['par', {parameter_general_name1}, {parameter_general_value1}, {parameter_general_description1}],
#                       ['par', {parameter_general_name2}, {parameter_general_value2}, {parameter_general_description2}],
#                       ['comm', {comment_general_1}],
#                       ...
#                   ],
#                   [   'Mobilities',
#                       ...
#                   ],
#                   ...
#               ]

    index=0 # When reading the device_parameters.txt file, first reset the index counter.

    #  Definition of the parameter object with section names.
    dev_par_object = [['Description'],['General'],['Mobilities'],['Contacts'],['Transport layers'],['Ions'],
                    ['Generation and recombination'],['Trapping'],['Numerical Parameters'],
                    ['Voltage range of simulation'],['User interface']]

    for line in fp:
        if line.startswith('**'):
            # Line is a left adjusted comment, determine whether it is a new section and update index if necessary
            index,changes = read_comment_line(line,index)
            if index == 0:
                # Comment part of top description, add to Description section
                dev_par_object[index].append(['comm',line[2:].strip()])
            elif changes:
                dev_par_object[index].append(['comm',line[2:].strip()])
        elif line.strip()=='':
            # Empty line between sections, ignore and do not add to dev_par_object
            continue
        else:
            # Line represents a parameter or related comment.
            par_line = line.split('*')
            if '=' in par_line[0]:
                par_split = par_line[0].split('=')
                par = ['par',par_split[0].strip(),par_split[1].strip(),par_line[1].strip()]
                dev_par_object[index].append(par)
                # print(dev_par_object)
            else:
                # leftover (*) comment. Add to the description of the last added parameter
                dev_par_object[index][-1][3] = dev_par_object[index][-1][3] + "*" + par_line[1].strip()
    return dev_par_object

def write_to_txt(dev_par_object):
    """Convert the List object into a single string. Formatted to the device_parameter definition

    Parameters
    ----------
    dev_par_object : List
        List object with all parameters and comments.

    Returns
    -------
    string
        Formatted string for the txt file
    """
    par_file=[] # Initialize List to hold all lines
    lmax = 0 # Max width of parameter = value section, initialise with 0
    section_length_max = 84

    # Description and Version
    for item in dev_par_object[0][1:]:
        # First element of the main object contains the top description lines. Skip very first element (Title).
        desc_line = "** " + item[1] + '\n'
        par_file.append(desc_line)

    # Determine max width of the 'parameter = value' section of the txt file.
    for sect_item in dev_par_object[1:]:
        # Loop over all sections
        for par_item in sect_item[1:]:
            # Loop over all parameters
            if par_item[0]=='par':
                # Only real parameter entries need to be considered, characterised by the first list element being 'par'
                temp_string = par_item[1] + ' = ' + par_item[2]
                if len(temp_string)> lmax:
                    # Update maxlength if length of 'par = val' combination exceeds it.
                    lmax = len(temp_string)
    # Add 1 to max length to allow for a empty space between 'par=val' and description.
    lmax = lmax + 1

    # Read every entry of the Parameter List object and create a formatted line (string) for it. Append to string List par_file.
    for sect_element in dev_par_object[1:]:
        #Loop over all sections. Exclude the first (Descriptive Title) element.
        # Start with a new line before each section name. Section title must be of format **title************... Length of the section title is 84 characters.
        par_file.append('\n')
        sec_title = "**" + sect_element[0]
        sec_title_length = len(sec_title)
        sec_title = sec_title + "*"*(section_length_max-sec_title_length) + '\n'
        par_file.append(sec_title)
        for par_element in sect_element:
            #  Loop over all elements in the section list, both parameters ('par') and comments ('comm')
            if par_element[0]== 'comm':
                # Create string for a left-justified comment and append to string List.
                par_line = '** ' + par_element[1] + '\n'
                par_file.append(par_line)
            elif par_element[0] == 'par':
                # Create string for a parameter. Format is par = val
                par_line = par_element[1] + ' = ' + par_element[2]
                par_line_length = len(par_line)
                # The string is filled with blank spaces until the max length is reached
                par_line = par_line + ' '*(lmax - par_line_length)
                # The description can be a multi-line description. The multiple lines are seperated by a '*'
                if '*' in par_element[3]:
                    # MultiLine description present. Split it and first append the par=val line as normal
                    temp_desc = par_element[3].split('*')
                    par_line = par_line + '* ' + temp_desc[0] + '\n'
                    par_file.append(par_line)
                    for temp_desc_element in temp_desc[1:]:
                        #  For every extra comment line, fill left part of the line with empty characters and add coment/descrip[tion as normal.
                        par_line = ' '*25 + '* ' + temp_desc_element + '\n'
                        par_file.append(par_line)
                else:
                    # Single Line description. Add 'par=val' and comment/description together, seperated by a '*'
                    par_line = par_line + '* ' + par_element[3] + '\n'
                    par_file.append(par_line)

    # Join all individual strings/lines together
    par_file = ''.join(par_file)

    return par_file

def read_comment_line(line, index):
    """ Read the line of type (left adjusted) comment (**).
        If the commented line matches a section name, update the index to store the parameters for this section in a List.
        When a left adjusted comment is encountered that does not match a section name or is not a starting comment/description,
        set the changes parameter to True to indicate that the comment must be added to the current section (via the index)

    Parameters
    ----------
    line : string
        single line from the txt parameter file
    index : number
        current index (section)

    Returns
    -------
    number
        (updated) object/section index
    """
# Note:         List indices:
#                   0: File desription + version
#                   1: General
#                   2: Mobilities
#                   3: Contacts
#                   4: Transport layers
#                   5: Ions
#                   6: Generation and recombination
#                   7: Trapping
#                   8: Numerical parameters
#                   9: Voltage range of simulation
#                   10: User interface

    changes = False
    if line.startswith('**General*****'):
        index = 1
    elif line.startswith('**Mobilities*****'):
        index = 2
    elif line.startswith('**Contacts*****'):
        index = 3
    elif line.startswith('**Transport layers*****') :
        index = 4
    elif line.startswith('**Ions*****'):
        index = 5
    elif line.startswith('**Generation and recombination*****'):
        index = 6
    elif line.startswith('**Trapping*****'):
        index = 7
    elif line.startswith('**Numerical Parameters*****'):
        index = 8
    elif line.startswith('**Voltage range of simulation*****'):
        index = 9
    elif line.startswith('**User interface*****'):
        index = 10
    else:
        changes = True
    return index,changes

def split_line_scpars(item, solar_cell_param, par, unit):
    """Read string line and split into the different parameters (Simualted, Experimental, Deviation)

    Parameters
    ----------
    item : string
        Parameter line
    solar_cell_param : dict
        Dict to hold the solar cell parameters
    par : string
        Paramemeter name
    unit : string
        Unit of the parameter

    Returns
    -------
    solar_cell_param : dict
        Updated Dict to hold the solar cell parameters
    """
    fact = 1
    # Remove the parameter name
    item = item.replace(par + ':','')
    # If not already done, remove the unit
    if not par== 'Jsc' and not par == 'FF' and not par == 'MPP':
        item = item.replace(unit,'')
    # Place the units in square brackets
    if not par == 'FF':
        unit = '[' + unit +']'
    val_list=item.split(' ')
    val_list_compact=[]
    for val_list_split in val_list:
        if not val_list_split == '':
            val_list_compact.append(val_list_split)
    for i in val_list_compact:
        if len(val_list_compact)>0:
            solar_cell_param['Simulated'][par + ' ' + unit] = (((val_list_compact[0])))+val_list_compact[1]+(((val_list_compact[2])))
        if len (val_list_compact) > 3:
            solar_cell_param['Experimental'][par + ' ' + unit] = (((val_list_compact[3])))+val_list_compact[4]+(((val_list_compact[5])))
        if len (val_list_compact) > 5:
            solar_cell_param['Deviation'][par + ' ' + unit] = (((val_list_compact[6])))
    return solar_cell_param

def write_scpars(item, solar_cell_param, solar_cell):
    """Read the solar cell parameters from the txt line based on a RegExp pattern. Store them in a dictionary.

    Parameters
    ----------
    item : string
        String containing a solar cell parameter
    solar_cell_param : dict
        The dict object to hold the solar cell parameters

    Returns
    -------
    dict
        Updated dict object to hold the solar cell parameters
    """
    if 'Jsc' in item:
        item = item.replace('A/m2','')
        solar_cell_param = split_line_scpars(item, solar_cell_param,'Jsc', 'Am\u207b\u00b2' )
        solar_cell = True
    if 'Vmpp' in item:
        solar_cell_param = split_line_scpars(item, solar_cell_param,'Vmpp', 'V' )
        solar_cell = True
    if 'MPP' in item:
        item = item.replace('W/m2','')
        solar_cell_param = split_line_scpars(item, solar_cell_param,'MPP', 'Wm\u207b\u00b2' )
        solar_cell = True
    if 'Voc' in item:
        solar_cell_param = split_line_scpars(item, solar_cell_param,'Voc', 'V' )
        solar_cell = True
    if 'FF' in item:
        solar_cell_param = split_line_scpars(item, solar_cell_param,'FF', '' )
        solar_cell = True
    return solar_cell_param,solar_cell

def verify_upload_parameter_file(data_devpar):
    tmp_id = random.randint(0,1e10)
    destination_file_devpar = open('Simulations/tmp/devpar_' + str(tmp_id) + '.txt', "w", encoding='utf-8')
    destination_file_devpar.write(data_devpar)
    destination_file_devpar.close()

    simss_path = 'SIMsalabim/SimSS/'
    line_min = []
    line_min_default = []
    valid_upload = False
    msg = ''

    # Read the uploaded file
    with open('Simulations/tmp/devpar_' + str(tmp_id) + '.txt', encoding='utf-8') as fpp:
        count = 1
        for line in fpp:
    # for line in file_str.splitlines():   
            line = line.strip()
            if not line.startswith('*') and not line.startswith('\n') and not line == '':
                line_min.append([line,count])
            count+=1

    for item_dir_list in os.listdir('Simulations/tmp'):
        if str(tmp_id) in item_dir_list:
            os.remove('Simulations/tmp/devpar_' + str(tmp_id) + '.txt')

    # Open the standard device parameters file
    with open(simss_path+'device_parameters.txt', encoding='utf-8') as fp:
        count = 1
        for line in fp:
            line = line.strip()
            if not line.startswith('*') and not line.startswith('\n') and not line == '':
                line_min_default.append([line,count])
            count+=1

    # Loop simultaneously over both Lists and check whether each entry matches. If not, return an error message 
    for a,b in zip(line_min,line_min_default):
        a_par = a[0].split('=')
        b_par = b[0].split('=')
        if len(a[0])<2:
            valid_upload = False
            msg = ('Upload failed, file not formatted correctly.\n\n Line ' + str(a[1]) + ': " ' + a + '" is not according to the format.' )
            return valid_upload,msg
        elif a_par[0] != b_par[0]:
            valid_upload = False
            msg = ('Upload failed, expected parameter: "' + b_par[0] + '" (line ' + str(b[1]) + ') and received parameter "' + a_par[0] + '" (line ' + str(a[1]) + ')' )
            return valid_upload,msg
        else:
            valid_upload = True
    return valid_upload,msg

