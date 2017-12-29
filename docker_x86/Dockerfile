# Dockerfile for Raspberry Pi web container
# Phil Hansen, 2016-11-06

FROM ubuntu:16.04
MAINTAINER Phil Hansen <phil@sg20.com>
EXPOSE 80

# Install required packages
# For Nginx, need curl installed first in order to download the repo signing key
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        gcc \
        libbz2-dev \
        libncurses-dev \
        libreadline-dev \
        libssl-dev \
        zlib1g-dev && \
    cd /tmp && \
    curl -O http://nginx.org/keys/nginx_signing.key && \
    apt-key add nginx_signing.key && \
    echo "deb http://nginx.org/packages/mainline/ubuntu/ trusty nginx" >> /etc/apt/sources.list && \
    echo "deb-src http://nginx.org/packages/mainline/ubuntu/ trusty nginx" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    cd /tmp && \
    curl -O https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz && \
    tar xfz Python-2.7.14.tgz && \
    cd Python-2.7.14 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

# Install pip and required libraries
RUN cd /tmp && \
    curl https://bootstrap.pypa.io/get-pip.py | python && \
    pip install --upgrade \
        Adafruit-GPIO \
        flask \
        mock \
        pytz \
        RPi.GPIO \
        uwsgi && \
    rm -rf /tmp/*

# Nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Add uWSGI config
COPY uwsgi.ini /uwsgi.ini

# Add run script
COPY start.sh /start.sh
RUN chmod +x /*.sh

# Add application to python path
ENV PYTHONPATH :/pi/lights

CMD ["/start.sh"]
