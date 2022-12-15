#!/bin/bash
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

