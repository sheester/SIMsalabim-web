#!/bin/bash
nginx -t
service nginx start
cd SIMsalabim-web
streamlit run SIMsalabim.py
