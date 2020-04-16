from flask import Flask, render_template, request
from Anime_NAS import convert_tuple, sql_connector, get_all_anime_in_database
from cover_crawler import cover_api
from Moe import Moe
import mysql.connector
import json



app = Flask(__name__)

@app.route('/update')
def update_database_season_anime():

    # Get the animes already in the database ---- returns a list of dicts with anime_id and anime_title
    anime_in_database = get_all_anime_in_database()

    # Get animes in the source website
    twist_moe = Moe()
    raw_website_data = twist_moe.get_all_animes_in_database()  # Returns a list of dicts with anime_title and main_url

    # format the scraped data 
    website_data = [{'anime_title':anime['anime_title'].replace("'","").replace('(','').replace(')',''), 'main_url': anime['main_url']} for anime in raw_website_data]

    # Create a list with just the titles for the animes on the website
    website_titles = [anime['anime_title'] for anime in website_data]

    # Create a list with just the anime_title in the db
    database_titles = [anime['anime_title'] for anime in anime_in_database]


    # Create a list with the titles for all animes that are not in the database wet 
    new_anime_title = [title for title in website_titles if title not in database_titles]

    # Create a new list with all the info for the new anime
    new_anime = [{'anime_title':anime['anime_title'], 'main_url':anime['main_url']} for anime in website_data if anime['anime_title'] in new_anime_title]


    # the mysql command
    command = "INSERT INTO Animes (anime_title, main_url) VALUES ('%s','%s') "

    # iterate through the new anime and add it to the db
    for anime in new_anime:

        # Get the tools to access the db
        data_base,my_cursor = sql_connector()
        my_cursor.execute(command % (anime['anime_title'],anime['main_url']))

        # commit the changes to the db
        data_base.commit()

        print(json.dumps(anime,indent=4))

    ############################################################################################################################################################
    # Get the anime_title and anime_id for the newly added anime
    new_anime_info = []
    for anime_title in new_anime_title:

        data_base,my_cursor = sql_connector()
        my_cursor.execute("SELECT * FROM Animes WHERE anime_title='%s'" %(anime_title))
        raw_anime_info = my_cursor.fetchall()
        anime_info = convert_tuple(data=raw_anime_info,keys=['anime_id','anime_title'],return_type='DICT')

        # append the data
        new_anime_info.append(anime_info)


    
    # Get the covers

    # Instantiate the crawler class to go through the db and getting the covers for every anime
    crawler = cover_api()

    # Go through all anime and get their covers
    cover_data = []
    for anime in new_anime_info:

        # Get the url for the cover
        cover_url = crawler.get_cover(anime_title=anime['anime_title'])

        # create a dict with the data and append it to the cover_data list
        anime_info = {'anime_id':anime['anime_id'], 'cover_path':cover_url}
        cover_data.append(anime_info)
        print(json.dumps(anime, indent=4))

        # connect to mysql database
        print('Getting mysql tools...')
        database,myCursor = sql_connector()
        
        # add to the db
        myCursor.execute("INSERT INTO Covers(anime_id,cover_path) VALUES (%s,'%s')"%(anime['anime_id'],cover_url))
        database.commit()