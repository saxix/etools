FROM python:3.6.4-jessie
# python:3.6.4-jessie has python 2.7 and 3.6 installed, and packages
# available to install 3.4
# /usr/local/bin/python is in fact python 3.6

# Install dependencies
RUN apt-get update \
&&  apt-get install -y --no-install-recommends \
    build-essential \
    libcurl4-openssl-dev \
    libjpeg-dev \
    vim \
    ntp \
    git-core \
    postgresql-client \
    libpq-dev \
    python-gdal \
    gdal-bin \
    libgdal-dev \
    libgdal1h \
    libgdal1-dev \
    libxml2-dev \
    libxslt-dev \
    xmlsec1 \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade \
    setuptools \
    pip \
    wheel
#
## http://gis.stackexchange.com/a/74060
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
ENV REQUIREMENTS_FILE production.txt
