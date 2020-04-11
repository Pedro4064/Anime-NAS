FROM ubuntu:latest

# update the packages
RUN apt-get -y update 

# Install python3 , pip, and all the packages necessary
RUN apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && pip3 install flask mysql-connector requests 

# Create a static directory and inside it create another one called Animes
RUN mkdir static && mkdir static/Animes

# Create and move to the scripts directory
RUN mkdir scripts
RUN mkdir scripts/templates 
WORKDIR /scripts

# Copy the necessary scripts 
COPY Anime_NAS.py /scripts
COPY ./templates /scripts/templates

CMD [ "python3","Anime_NAS.py" ]
