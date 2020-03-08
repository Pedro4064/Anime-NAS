from Anime_NAS import sql_connector,convert_tuple, get_titles_from_ids
from Moe import Moe
import os

def get_watching_list():

    # Get the tools to access the db
    database,myCursor = sql_connector()
    
    # Get the raw data from the db
    myCursor.execute('SELECT anime_id FROM Watching')
    raw_data = myCursor.fetchall()

    # Parse the data
    watching_list = convert_tuple(data=raw_data,keys=['anime_id'], return_type='LIST')

    #  Return a list of dicts with the anime_id from the animes that are in the watching list
    return watching_list

def get_main_url_from_id(anime_id:int):

    #  Get the tools to access the db
    database,myCursor = sql_connector()

    # get the raw data
    myCursor.execute('SELECT main_url FROM Animes WHERE anime_id = %d' %(anime_id))
    raw_data = myCursor.fetchall()

    # format the data
    anime_url = convert_tuple(data=raw_data,keys=['main_url'],return_type='DICT')

    #  Return the main url for the anime
    return anime_url['main_url']

def get_downloaded_episodes(anime_id:int):

    # Get the tools to access the db
    database,myCursor = sql_connector()

    # get raw data 
    myCursor.execute('SELECT anime_id,episode_number FROM Downloads WHERE anime_id = %d' %(anime_id))
    raw_data = myCursor.fetchall()

    # format the data
    anime_episodes = convert_tuple(data=raw_data,keys=['anime_id','episode_number'],return_type='LIST')

    #  Return a dict with the anime_d and the episode_number
    return anime_episodes

def get_anime_links(anime_url):

    twist_moe = Moe()
    mp4_urls,referers = twist_moe.get_raw_urls(url=anime_url,nEpisodes=1000)

    # Return both the referers and the raw urls
    return mp4_urls,referers

def parse_new_episodes(downloaded_episodes:'list of all episodes downloaded for that anime', released_episodes:'list of all episodes released and available in the site'):
    
    # Check to see if there are new episodes by checking the size of list containing all episodes in the website and comparing to the number of episodes downloaded in the system
    if len(downloaded_episodes) == len(released_episodes):

        return None

    else:
        # If there are new Episodes, create a sub list containing  only the new relsed ones

        # Get the number of new episodes that are not in the system
        number_of_new_episodes = len(released_episodes)-len(downloaded_episodes)

        # Multiply by -1 to format the new list
        number_of_new_episodes *= -1

        # create a sub list containing  only the new relsed ones
        new_released = released_episodes[number_of_new_episodes:]

        # return a list with all the new episodes on the site
        return new_released

def download_new_releases(anime_id,number_of_downloaded_episodes,new_releases_referers:list, new_releases_raw_mp4:list):

    # Get the anime title so we can change to the correct directory
    anime_title = get_titles_from_ids(ids = [anime_id])[0]['anime_title']

    base_directory = '/Users/pedrocruz/Desktop/Anime/'
    anime_directory = base_directory+anime_title.replace('.','_').replace('/','_').replace(':','')

    # Change to the directory 
    os.chdir(anime_directory)

    # A variable to keep track of the episode number
    episode_number = number_of_downloaded_episodes+1
    
    for raw_url,referer in zip(new_releases_raw_mp4,new_releases_referers):
        pass        
if __name__ == '__main__':

    watching_list = get_watching_list()

    for anime in watching_list:
        potato = get_downloaded_episodes(anime_id=anime['anime_id'])
        number_of_episodes = len(get_anime_links(get_main_url_from_id(anime['anime_id'])))