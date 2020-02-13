from Moe import Moe
from cover_crawler import cover_api
from Anime_NAS import convert_tuple, sql_connector, get_all_anime_in_database
import mysql.connector
import json


# connect to mysql database
database,myCursor = sql_connector()



################################################################################################################################################################

# Get all the data from the Twistmoe website
twist_moe = Moe()
website_data = twist_moe.get_all_animes_in_database()

# the mysql command
command = "INSERT INTO Animes (anime_title, main_url) VALUES ('%s','%s') "

# populate the db
for anime in website_data:

    # Format the command
    # command = command % (anime['anime_title'],anime['main_url'])

    # Send the command
    myCursor.execute(command % (anime['anime_title'].replace("'","").replace('(','').replace(')',''),anime['main_url']))


    # commit the changes made to the db
    database.commit()

################################################################################################################################################################

# Instantiate the crawler class to go through the db and getting the covers for every anime
crawler = cover_api()

# Get the list with all the animes' ids and titles
anime_data = get_all_anime_in_database()

# Go through all anime and get their covers
cover_data = []
for anime in anime_data:

    # Get the url for the cover
    cover_url = crawler.get_cover(anime_title=anime['anime_title'])

    # create a dict with the data and append it to the cover_data list
    anime_info = {'anime_id':anime['anime_id'], 'cover_path':cover_url}
    cover_data.append(anime_info)
    print(json.dumps(anime, indent=4))

    # add to the db
    myCursor.execute("INSERT INTO Covers(anime_id,cover_path) VALUES (%s,'%s')"%(anime['anime_id'],cover_url))
    database.commit()

