FROM ubuntu:latest

# update the packages
RUN apt-get -y update 

# Install python3 , pip, and all the packages necessary
RUN apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && pip3 install flask mysql-connector requests 



# Create and move to the scripts directory
RUN mkdir scripts
WORKDIR /scripts

# Copy the necessary scripts 
# COPY Anime_NAS.py /scripts
# COPY ./templates /scripts/templates

CMD [ "python3","Add_Previously_Downloaded_Anime.py" ]