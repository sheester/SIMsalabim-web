#!/bin/bash
nginx -t
service nginx start
cd SIMsalabim-web
streamlit run app.py
