FROM linuxserver/mariadb:latest

#Create Database
ENV MYSQL_DATABASE="Anime_NAS"

#Copy the sql file to the correct directory to initialize the database
COPY ./database_setup/Database_setup.sql /config/initdb.d/

