#!/bin/bash
nginx -t
service nginx start
cd src
streamlit run app.py
