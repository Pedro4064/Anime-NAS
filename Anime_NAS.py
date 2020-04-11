from flask import Flask, render_template, request, redirect, send_from_directory
import mysql.connector
import subprocess
import requests
import json
import sys 
import os

# Create a flask instance
app = Flask(__name__,static_folder='/static')
# app = Flask(__name__)

def sql_connector():

    # Instantiate a sql connector
    data_base = mysql.connector.connect(
    host = 'anime_database',
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
    myCursor.execute('SELECT anime_id FROM Favorites')
    raw_favorites = myCursor.fetchall()

    # format the data
    favorites = convert_tuple(data = raw_favorites, keys = ['anime_id'], return_type = 'LIST')

    # Get a new list of dicts that will have: anime_id and cover path
    favorites = [get_covers_from_ids([anime_data['anime_id']])[0] for anime_data in favorites ]

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
        anime_dict = {'anime_id': anime_id, 'cover_path': cover_path['cover_path']}
        anime_data.append(anime_dict)


    # return the list with all the dicts
    return anime_data



@app.route('/setUp')
def first_setup():

    # Get the tools to access the db
    database,my_cursors = sql_connector()

    # Create the tables
    my_cursors.execute('CREATE TABLE Animes ( anime_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, anime_title VARCHAR(100) , main_url VARCHAR(240) )')
    database.commit()

    my_cursors.execute('CREATE TABLE Downloads (anime_id INT(10) NOT NULL, episode_number SMALLINT, file_path VARCHAR(240), FOREIGN KEY (anime_id) REFERENCES Animes(anime_id) )')
    database.commit()

    my_cursors.execute('CREATE TABLE Favorites (anime_id INT(10) NOT NULL, cover_path VARCHAR(240) ,FOREIGN KEY(anime_id) REFERENCES Animes(anime_id));')
    database.commit()

    my_cursors.execute('CREATE TABLE Watching (anime_id INT(10) NOT NULL, FOREIGN KEY(anime_id) REFERENCES Animes(anime_id))')
    database.commit()

    my_cursors.execute('CREATE TABLE Covers (anime_id INT(10) NOT NULL,cover_path VARCHAR(240) , FOREIGN KEY(anime_id) REFERENCES Animes(anime_id))')
    database.commit()

    my_cursors.execute('CREATE TABLE Animes_Download_List (anime_id INT(10) NOT NULL, FOREIGN KEY(anime_id) REFERENCES Animes(anime_id))')
    database.commit()

    # populate the db
    requests.get('http://populate_db:80/populate_database')
    return "SetUp Done"

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

    
    # Create a new list with all the info from the anime, including cover_path
    watching_list = [{'anime_id':anime_data['anime_id'], 'anime_title':anime_data['anime_title'],'cover_path': get_covers_from_ids([anime_data.get('anime_id')])[0]['cover_path']} for anime_data in watching_list]







    # Get all the episodes downloaded
    myCursor.execute('SELECT anime_id FROM Animes_Download_List')
    raw_downloads_id = myCursor.fetchall()

    # format the data
    anime_ids = convert_tuple(data=raw_downloads_id, keys=['anime_id'], return_type='LIST')
    

    # Get the title for the corresponding id
    downloaded_list = []
    for anime_id in anime_ids:

        anime_id = anime_id['anime_id']
        anime_data = {}

        # get the title
        myCursor.execute('SELECT anime_title FROM Animes WHERE anime_id = %d'%(anime_id))

        # format data 
        raw_download_title = myCursor.fetchall()
        download_title = convert_tuple(data=raw_download_title, keys=['anime_title'], return_type='DICT')

        # format the deict 
        anime_data = {'anime_id':anime_id, 'anime_title':download_title['anime_title']}

        # append the data to the downloaded_list
        downloaded_list.append(anime_data)

    print(json.dumps(downloaded_list, indent=4))
    
    #################### Use to call another python script (the one to download) #########################
    # commands = ["/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7", "/Users/pedrocruz/Desktop/Programming/Python/Git/Anime-NAS/potato.py", "asdasdas"]
    # subprocess.Popen(commands,  stdout=subprocess.PIPE)
    # render the html
    ######################################################################################################

    return render_template('AnimeNAS.html', favorites = favorites, watching_list = watching_list, downloaded_list = downloaded_list)
    
@app.route('/Animes/<Mode>')
def edit_favorites(Mode):

    if Mode == 'add_favorite':

        animes = get_all_anime_in_database()
        print(json.dumps(animes,indent=4))
        return render_template('AddFavorites.html', Mode = 'Add',favorites = animes)


    elif Mode == 'remove_favorite':

        # Get the info on the Favorites db
        favorites = get_favorited_anime()

        # Make a list of the ids
        anime_ids = [anime['anime_id'] for anime in favorites]

        # get the titles for those ids
        favorites = get_covers_from_ids(ids = anime_ids)

        print(json.dumps(favorites,indent=4))
        return render_template('RemoveFavorites.html', Mode = 'Remove',favorites = favorites)
    
@app.route('/Animes/add_to_favorites/anime_id=<anime_id>')
def add_to_favorites(anime_id):

    # Get the tools to access the db
    database,myCursor = sql_connector()

    # Execute the command
    myCursor.execute('INSERT INTO Favorites(anime_id) VALUES(%d)' %(int(anime_id)))

    # Send the command
    database.commit()

    # redirect to the main page
    return redirect('/Animes')

@app.route('/Animes/delete_from_favorites/anime_id=<anime_id>')
def delete_from_favorites(anime_id):

    # Get the tools to access the db
    database,myCursor = sql_connector()

    # Execute the command
    myCursor.execute('DELETE FROM Favorites WHERE anime_id = %d' %(int(anime_id)))

    # Send the command
    database.commit()

    # redirect to the main page
    return redirect('/Animes')



@app.route('/Animes/Watching/<Mode>')
def edit_watching(Mode):

    if Mode == 'add_watching':
    
        animes = get_all_anime_in_database()

        print(json.dumps(animes,indent=4))
        return render_template('AddWatching.html', Mode = 'Add',animes = animes)


    elif Mode == 'remove_watching':
        
        # Get the tools to access the db
        database,myCursor = sql_connector()

        # Get the list of all anime in the watching table
        myCursor.execute('SELECT * FROM Watching')
        watching_ids = myCursor.fetchall()

        # format the data
        watching_ids = convert_tuple(data=watching_ids, keys=['anime_id'], return_type='LIST')
        

        # Get a list with all the ids
        watching_ids = [anime_data['anime_id'] for anime_data in watching_ids]

        # Get a list with dicts that contain: 'anime_id' and 'cover_path'
        anime_data = get_covers_from_ids(ids=watching_ids)
        print(json.dumps(anime_data, indent=4))

        return render_template('RemoveWatching.html', Mode = 'Remove', animes = anime_data)

@app.route('/Animes/add_to_watching/anime_id=<anime_id>')
def add_to_watching(anime_id):

    # Get the tools to access the db
    database,myCursor = sql_connector()

    # Execute the command
    myCursor.execute('INSERT INTO Watching(anime_id) VALUES(%d)' %(int(anime_id)))

    # Send the command
    database.commit()

    # redirect to the main page
    return redirect('/Animes')

@app.route('/Animes/delete_from_watching/anime_id=<anime_id>')
def delete_from_watching(anime_id):

    # Get the tools to access the db
    database,myCursor = sql_connector()

    # Execute the command
    myCursor.execute('DELETE FROM Watching WHERE anime_id = %d' %(int(anime_id)))

    # Send the command
    database.commit()

    # redirect to the main page
    return redirect('/Animes')



@app.route('/Animes/Downloads/<Mode>')
def edit_downloads(Mode):


    if Mode == 'add_download':
    
        animes = get_all_anime_in_database()

        print(json.dumps(animes,indent=4))
        return render_template('AddDownloads.html', Mode = 'Add',animes = animes)


    elif Mode == 'remove_download':

        pass

@app.route('/Animes/add_to_download/anime_id=<anime_id>')
def add_to_download(anime_id):

    # Get the tools to access the db
    database,myCursor = sql_connector()

    # Execute the command
    myCursor.execute('INSERT INTO Animes_Download_List(anime_id) VALUES(%d)' %(int(anime_id)))

    # Send the command
    database.commit()

    #################### Use to call another python script (the one to download) #########################
    requests.get('http://anime_download:80/download_anime/anime_id=%s' %(anime_id))
    ######################################################################################################

    # redirect to the main page
    return redirect('/Animes')


@app.route('/Animes/Play/anime_id=<anime_id>/episode=<episode_number>')
def play_video(anime_id,episode_number):

    # get the tools to access the db
    database,myCursor = sql_connector()

    # Get the list of all episodes for that anime
    myCursor.execute('SELECT * FROM Downloads WHERE anime_id = %d ORDER BY episode_number' %(int(anime_id)))
    raw_response = myCursor.fetchall()

    # parse the data
    download_data = convert_tuple(data=raw_response,keys=['anime_id','episode_number','file_path'], return_type='LIST')

    # Get the info for the episode
    episode_data = [anime_info for anime_info in download_data if anime_info['episode_number'] == int(episode_number)]

    # render the html
    return render_template('AnimesVideo.html', anime_data= download_data, episode_data=episode_data[0])
    # return redirect('file:://Users/pedrocruz/Desktop/Programming/Python/Git/Anime-NAS/static/Animes/Ookami to Koushinryou_1.mp4')


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=80)
