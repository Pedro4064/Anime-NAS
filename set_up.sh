# CLEAR THE SCREEN 
clear 

# GET THE PATH TO THE HDD THAT WAS PASSED AS ARG IN THE COMMAND LINE
PATH_TO_HDD=${1?Error: no path to save the anime given}
echo "Anime Location: " $PATH_TO_HDD 

# DOWNLOAD AND INSTALL DOCKER
echo "Downloading docker ..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# ADD THE PI USER TO DOCKER SO IT WONT NEED TO RUN AS ROOT
sudo usermod -aG docker Pi

# PIP INSTALL DOCKER-COMPOSE
echo "Downloading docker-compose ..."
pip install docker-compose

# CURL TO DOWNLOAD THE DOCKER-COMPOSE.YML
curl https://raw.githubusercontent.com/Pedro4064/Anime-NAS/Docker_Develop/docker-compose.yml > docker-compose.yml

# SED TO FIT UPDATE THE PATH FROM THE DOCKER-COMPOSE.yml
sed -i "s+/media/pi/DISK/Animes+$PATH_TO_HDD+g" docker-compose.yml

# COMPOSE UP THE CONTAINERS
docker-compose up