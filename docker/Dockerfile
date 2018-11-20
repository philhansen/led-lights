# Dockerfile for Raspberry Pi web container
# Phil Hansen, 2017-10-29

FROM resin/armv7hf-debian:stretch
MAINTAINER Phil Hansen <phil@sg20.com>
EXPOSE 80

ENV PYTHON_VERSION 3.7.1

# Install required packages
# add stretch-backports to sources.list so we can install the latest nginx
RUN echo "deb http://ftp.debian.org/debian stretch-backports main" >> /etc/apt/sources.list && \
    echo "deb-src http://ftp.debian.org/debian stretch-backports main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        gcc \
        libbz2-dev \
        libffi-dev \
        libncurses-dev \
        libreadline-dev \
        libssl-dev \
        zlib1g-dev && \
    apt-get -t stretch-backports install nginx && \
    cd /tmp && \
    curl -O https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar xfz Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*
    
# Install pip and required libraries
RUN cd /tmp && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 && \
    pip3 install --upgrade \
        Adafruit-GPIO \
        flask \
        mock \
        pytz \
        RPi.GPIO \
        uwsgi && \
    rm -rf /tmp/*
        
# Nginx config
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Add uWSGI config
COPY uwsgi.ini /uwsgi.ini

# Add run script
COPY start.sh /start.sh
RUN chmod +x /*.sh

# Add application to python path
ENV PYTHONPATH :/pi/lights

CMD ["/start.sh"]
