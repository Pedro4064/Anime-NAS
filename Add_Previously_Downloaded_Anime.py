import Anime_NAS
import os

def logo():

    logo_ascii = """

    """

def get_user_input():

    anime_title = input('•Anime title- ')
    number_of_episodes = int(input('•Number of episodes downloaded- '))
    anime_id = ''

    # Create a dict containing all the info
    anime_data = {'anime_title':anime_title, 'anime_id':anime_id, 'number_of_episodes': number_of_episodes}

    # Retunr the dict
    return anime_data

def get_anime_id(anime_title:str):

    # Get the tools to access the db
    my_database, my_cursor = Anime_NAS.sql_connector()

    # Get a list with the names and ids of all animes that have similar title 
    sql_command = r"SELECT anime_id,anime_title FROM Animes WHERE anime_title LIKE '%%" + anime_title + r"%%'"

    # Excecute the command
    my_cursor.excecute(sql_command)

    # Fetch the results 
    raw_results = my_cursor.fetchall()

    # Format the result 
    parsed_results = Anime_NAS.convert_tuple(data=raw_results,keys=['anime_id','anime_title'],return_type='LIST')

    # Show the user the options and get the input of the correct anime_id
    for anime in parsed_results:

        print(anime.get('anime_id'),"--",anime.get('anime_title'))

    # correct anime_id
    correct_anime_id = int(input('•ID for the correct anime - '))

    # return the id
    return correct_anime_id

def update_db(anime_id:int, number_of_episodes:int, anime_title:str):
    
    # Get the tools to access the db
    my_database,my_cursor = Anime_NAS.sql_connector()

    # Add the anime to the Animes_Download_List table 
    sql_command = "INSERT INTO Animes_Download_List(anime_id) VALUES(%d)" %(anime_id)
    my_cursor.excecute(sql_command)
    my_database.commit()


    # insert all episodes into the downloads table
    static_path = 'Animes/'+anime_title.replace('.','_').replace('/','_').replace(':','')+'/%s'
    file_name = anime_title.replace('.','_').replace('/','_').replace(':','')+'_'+'%d'+'.mp4'

    # Iterate through the episodes
    for episode_number in range(1,number_of_episodes+1):

        print('Adding episode',episode_number,'to the database')
        my_cursor.execute("INSERT INTO Downloads(anime_id,episode_number,file_path) VALUES(%d,%d,'%s')" %(anime_id,episode_number,static_path %(file_name %(episode_number))))
        my_database.commit()


if __name__ == '__main__':

    os.system('clear')
    
    anime_data = get_user_input()
    anime_id = get_anime_id(anime_data['anime_title'])
    update_db(anime_id,number_of_episodes=anime_data['number_of_episodes'],anime_title=anime_data['anime_title'])