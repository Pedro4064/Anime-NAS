FROM ubuntu:latest

# Update the packages list and install chromium-browser
RUN apt-get -y update && apt-get install -y chromium-browser

# Get the wget package (it will be used to download the deb webdriver file from the web)
RUN apt-get install -y wget 

# Make sure  dpkg is installed  (it will be used to install the chromedriver package)
RUN apt-get install -y dpkg

# Download the chrome driver deb file, install it and remove the deb file
RUN wget http://launchpadlibrarian.net/361669488/chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb \
    && dpkg -i chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb \ 
    && rm chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb


# Install python3 , pip, and all the packages necessary
RUN apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && pip3 install flask mysql-connector requests selenium



# Create and move to the scripts directory
RUN mkdir scripts
WORKDIR /scripts

# Copy the necessary scripts
COPY Populate_db.py /scripts
COPY Moe.py /scripts
COPY cover_crawler.py /scripts
COPY Anime_NAS.py /scripts

CMD [ "python3","Populate_db.py" ]
