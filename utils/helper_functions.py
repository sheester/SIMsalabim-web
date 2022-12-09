# helper_functions.py>

# functions
def read_from_txt(fp):
# Description:  Read the opened .txt file line by line and store all in the dev_par_object. 
# Arguments:    fp (TextIOWrapper) - filepointer to the opened .txt file.
# Returns:      dev_par_object (List) - List with nested lists for all parameters in all sections.
# 
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
# Description:  Convert the List object into a single string. Formatted to the device_parameter definition
# Arguments:    dev_par_object (List) - List object with all parameters and comments.
# Returns:      par_file (string) - Formatted string for the txt file

    par_file=[] # Initialize List to hold all lines
    lmax = 0 # Max width of parameter = value section, initialise with 0

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
        sec_title = sec_title + "*"*(84-sec_title_length) + '\n'
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
# Description:  Read the line of type (left adjusted) comment (**). 
#               If the commented line matches a section name, update the index to store the parameters for this section in a List. 
#               When a left adjusted comment is encountered that does not match a section name or is not a starting comment/description, 
#               set the changes parameter to True to indicate that the comment must be added to the current section (via the index)
# Arguments:    line (string) - single line from the txt parameter file
#               index (number) - current index (section)
# Returns:      index (number) - (updated) object/section index
#
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