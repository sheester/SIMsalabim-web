#!/bin/bash
# Recompile simss for operating system support

if ! command fpc -i >& /dev/null; then
    echo 'Free Pascal Compiler is not installed. Refer to manual for installation instructions.'
    exit 1
fi

fpc SIMsalabim/SimSS/simss

# Check whether pip/pipenv is installed
if ! command pip -V >& /dev/null 
then
    sudo apt-get install python3-pip
    pip3 install pipenv
fi

# Check if a Pipfile / pipenv already exists. If not, create a new one and install packages in requirements.txt
FILE=Pipfile
if ! test -f "$FILE"; then 
    pipenv install -r requirements.txt
fi

# Run a pip env shell and start streamlit app 
pipenv run streamlit run SIMsalabim.py

