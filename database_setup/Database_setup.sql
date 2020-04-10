-- Create DB
CREATE DATABASE Anime_NAS;

-- Use the db
USE Anime_NAS;

-- Create the first table
CREATE TABLE Animes ( anime_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, anime_title VARCHAR(100) , main_url VARCHAR(240) );

-- Create the table that will hold the data for the downloaded anime
CREATE TABLE Downloads (anime_id INT(10) NOT NULL, episode_number SMALLINT, file_path VARCHAR(240), FOREIGN KEY (anime_id) REFERENCES Animes(anime_id) );

-- Create the table that will hold the ids for the favorited anime, and the path for its cover art
CREATE TABLE Favorites (anime_id INT(10) NOT NULL, cover_path VARCHAR(240) ,FOREIGN KEY(anime_id) REFERENCES Animes(anime_id));

-- Create the table that will hold the id for the watching list
CREATE TABLE Watching (anime_id INT(10) NOT NULL, FOREIGN KEY(anime_id) REFERENCES Animes(anime_id));

-- Create the table that will hold the id and cover path for all the anime
CREATE TABLE Covers (anime_id INT(10) NOT NULL,cover_path VARCHAR(240) , FOREIGN KEY(anime_id) REFERENCES Animes(anime_id));

-- Create a table that will hold the ids for all anime marked as downloaded
CREATE TABLE Animes_Download_List (anime_id INT(10) NOT NULL, FOREIGN KEY(anime_id) REFERENCES Animes(anime_id));
