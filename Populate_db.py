from flask import Flask, render_template, request, redirect, send_from_directory
from Anime_NAS import convert_tuple, sql_connector, get_all_anime_in_database
from cover_crawler import cover_api
from Moe import Moe
import mysql.connector
import json

app = Flask(__name__)


@app.route('/populate_database')
def populate_database():

    # Get all the data from the Twistmoe website
    print('Instantiating Moe class and getting all the anime in the website ...')
    twist_moe = Moe()
    website_data = twist_moe.get_all_animes_in_database()

    # connect to mysql database
    print('Getting mysql tools...')
    database, myCursor = sql_connector()

    # the mysql command
    command = "INSERT INTO Animes (anime_title, main_url) VALUES ('%s','%s') "

    # populate the db
    for anime in website_data:

        # Send the command
        myCursor.execute(command % (anime['anime_title'], anime['main_url']))

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
        anime_info = {'anime_id': anime['anime_id'], 'cover_path': cover_url}
        cover_data.append(anime_info)
        print(json.dumps(anime, indent=4))

        # connect to mysql database
        print('Getting mysql tools...')
        database, myCursor = sql_connector()

        # add to the db
        myCursor.execute("INSERT INTO Covers(anime_id,cover_path) VALUES (%s,'%s')" % (
            anime['anime_id'], cover_url))
        database.commit()

    return "Database done populating"


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=80)
