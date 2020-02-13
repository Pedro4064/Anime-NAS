from flask import Flask, render_template, request
import mysql.connector
import json


# Create a flask instance
app = Flask(__name__)

def sql_connector():

    # Instantiate a sql connector
    data_base = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'P3dr0mysql',
    database = 'Anime_NAS'
    )

    # create a cursur to controll the db
    myCursor = data_base.cursor(buffered=True)

    # return the data base and cursor
    return data_base,myCursor

def convert_tuple(data:tuple, keys:list, return_type:'The type of return expected - list or dict'):
    # convert a tuple to a json dict

    json_data = []

    # Goes through each anime 
    for anime in data:
        
        anime_dict = {}

        # For every key in the keys list, add it to the anime_dict with its corresponding data on the anime tuple
        for index,key in enumerate(keys):

            anime_dict[key] = anime[index]

        # append the dictionary to the json_data list
        json_data.append(anime_dict)
            
    # return the json list if the return_type is  'LIST'
    if return_type == 'LIST':
        return json_data
    
    # if the return type is 'DICT', the data should only have one element --- data[0][0], otherwise it will only return the last tupple in the list
    elif return_type == 'DICT':
        return anime_dict

def get_all_anime_in_database():

    # Get the necessary tools to acess the db
    data_base,myCursor = sql_connector()

    # Get the names and ids for all anime
    myCursor.execute('SELECT anime_id, anime_title FROM Animes ORDER BY anime_title')
    raw_anime_data = myCursor.fetchall()

    # format the data
    anime_data = convert_tuple(data=raw_anime_data, keys=['anime_id','anime_title'], return_type='LIST')

    return anime_data

def get_favorited_anime():

    # Get the database connector
    data_base,myCursor = sql_connector()

    # Get the list of favorited anime
    myCursor.execute('SELECT * FROM Favorites')
    raw_favorites = myCursor.fetchall()

    # format the data
    favorites = convert_tuple(data = raw_favorites, keys = ['anime_id','cover_path'], return_type = 'LIST')

    return favorites

def get_titles_from_ids(ids:list):

    # necessary tools for accessing the db
    data_base,myCursor = sql_connector()

    animes = []
    for anime_id in ids:

        # Get the first title
        myCursor.execute('SELECT anime_id, anime_title FROM Animes WHERE anime_id = %d' %(anime_id))
        raw_response = myCursor.fetchall()

        # convert the data into a dict and append it to the list
        animes.append(convert_tuple(data=raw_response, keys=['anime_id','anime_title'], return_type='DICT'))

    return animes

def get_covers_from_ids(ids:list):

    # Get the connector to access the db
    data_base,myCursor = sql_connector()
    
    # list that will hold all the dicts
    anime_data = []

    for anime_id in ids:

        myCursor.execute('SELECT cover_path FROM Covers WHERE anime_id=%d' %(anime_id))
        cover_path = myCursor.fetchall()

        # format the data
        cover_path = convert_tuple(data=cover_path, keys=['cover_path'],return_type='DICT')

        # format the dict and append it to the list
        anime_dict = {'anime_id': anime_id, 'cover_path': cover_path}
        anime_data.append(anime_dict)


    # return the list with all the dicts
    return anime_data


@app.route('/Animes')
def animes_main_page():

    # Get a list with the favorited anim
    favorites = get_favorited_anime()


    # Get the database connector
    data_base,myCursor = sql_connector()




    # Get the watching list
    myCursor.execute('SELECT * FROM Watching')
    raw_watching = myCursor.fetchall()

    # format the data
    watching = convert_tuple(data=raw_watching, keys=['anime_id'], return_type='LIST')
    watching_list = []

    # get the title for the corresponding IDs
    for anime in watching:

        anime_id = anime['anime_id']

        # get the name from the Animes table
        myCursor.execute('SELECT anime_title FROM Animes WHERE anime_id = %d' %(anime_id))

        #  get and parse the data
        raw_name = myCursor.fetchall()
        name = convert_tuple(data=raw_name, keys=['anime_title'], return_type='DICT')['anime_title']

        # Make a dict and add to the watching list
        watching_dict = {'anime_id':anime_id, 'anime_title': name}
        watching_list.append(watching_dict)

    



    # Get all the episodes downloaded
    myCursor.execute('SELECT anime_id FROM Downloads')
    raw_downloads_id = myCursor.fetchall()

    # format the data
    raw_downloads_id = convert_tuple(data=raw_downloads_id, keys=['anime_id'], return_type='LIST')

    # Remove duplicated data
    anime_ids = []
    for anime_data in raw_downloads_id:

        # Get the id in the dict
        anime_id = anime_data['anime_id']

        # if the id was not already in the list, add it
        if anime_id not in anime_ids:
            anime_ids.append(anime_id)

    
    # Get the title for the corresponding id
    downloaded_list = []
    for anime_id in anime_ids:

        anime_data = {}

        # get the title
        myCursor.execute('SELECT anime_title FROM Animes WHERE anime_id = %d'%(anime_id))

        # format data 
        raw_download_title = myCursor.fetchall()
        download_title = convert_tuple(data=raw_download_title, keys='anime_title', return_type='DICT')

        # format the deict 
        anime_data = {'anime_id':anime_id, 'anime_title':download_title}

        # append the data to the downloaded_list
        downloaded_list.append(anime_data)


    # render the html
    return render_template('AnimeNAS.html', favorites = favorites)


@app.route('/Animes/<Mode>')
def favorites(Mode):

    if Mode == 'add_favorite':

        animes = get_all_anime_in_database()
        print(json.dumps(animes,indent=4))
        return render_template('Favorites.html', Mode = 'Add',favorites = animes)


    elif Mode == 'remove_favorite':

        # Get the info on the Favorites db
        favorites = get_favorited_anime()

        # Make a list of the ids
        anime_ids = [anime['anime_id'] for anime in favorites]

        # get the titles for those ids
        favorites = get_titles_from_ids(ids = anime_ids)

        print(json.dumps(favorites,indent=4))
        return render_template('Favorites.html', Mode = 'Remove',favorites = favorites)
    



if __name__ == '__main__':

    app.run(debug=True, host='172.20.10.7')