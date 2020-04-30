import Anime_NAS

def logo():

    logo_ascii = """

    """

def get_user_input():

    anime_title = input('•Anime title- ')
    number_of_episodes = input('•Number of episodes downloaded- ')
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