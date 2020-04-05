FROM ubuntu:latest

# Install python3 , pip, and all the packages necessary
RUN apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && pip3 install flask,mysql.connector

# Create and move to the scripts directory
RUN mkdir scripts 
WORKDIR /scripts

# Copy the necessary scripts 
COPY . /scripts

