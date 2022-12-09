# Slim version of Python
FROM python:3.10-slim-bullseye

# Download Package Information
RUN apt-get update -y
# Install Tkinter
RUN apt-get install tk git fpc -y

RUN apt-get install -y nginx ca-certificates apache2-utils certbot python3-certbot-nginx sudo cifs-utils 
       
RUN apt-get update && apt-get -y install cron

RUN apt-get clean && apt-get autoclean && apt-get autoremove

RUN rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/nginx.conf

RUN git clone https://github.com/sheester/SIMsalabim-web.git

#install the streamlit app
WORKDIR SIMsalabim-web
RUN git clone https://github.com/kostergroup/SIMsalabim.git

# install compile SIMsalabim # and save default parameters to revert to
COPY . .
WORKDIR SIMsalabim/SimSS
RUN fpc simss.pas
# RUN cp device_parameters.txt device_parameters_backup.txt

# install requirements for the strealit app
WORKDIR ../..
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR ..
COPY run.sh .
RUN chmod a+x run.sh

# Commands to run the streamlit application
CMD ["./run.sh"]
