from Anime_NAS import sql_connector,convert_tuple, get_titles_from_ids
from Moe import Moe
import datetime
import time
import requests
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

    # Get the tools to access the database
    database,MyCursor = sql_connector()

    # Get the anime title so we can change to the correct directory
    anime_title = get_titles_from_ids(ids = [anime_id])[0]['anime_title']

    base_directory = '/Animes'
    anime_directory = base_directory+anime_title.replace('.','_').replace('/','_').replace(':','')
    static_path = 'Animes/'+anime_title.replace('.','_').replace('/','_').replace(':','')+'/%s'

    # Change to the directory 
    os.chdir(anime_directory)

    # A variable to keep track of the episode number
    episode_number = number_of_downloaded_episodes+1
    
    for raw_url,referer in zip(new_releases_raw_mp4,new_releases_referers):
        
         # Set up the session config
        session = requests.Session()
        session.headers.update({'referer':referer})

        # A Bool to determine if the download was successful
        done = False
        while done == False:

            # Make a request to the url
            response = session.get(raw_url, stream=True)
            
            file_name = anime_title.replace('.','_').replace('/','_').replace(':','')+'_'+str(episode_number)+'.mp4'
            

            # Create the .mp4 file and write binary content
            with open(file_name,'wb') as video_file:

                # Iterate through the content, so not every thing is stored in memory at the same time
                for chunk in response.iter_content(512):
                    video_file.write(chunk)

            # Check to see the size of the file, if it is too small and error happened
            if os.path.getsize(file_name) < 10000:
                done = False
                print(os.path.getsize(file_name))

            else:
                done = True

        
        # Update the database
        MyCursor.execute("INSERT INTO Downloads(anime_id,episode_number,file_path) VALUES(%d,%d,'%s')" %(anime_id,episode_number,static_path %(file_name)))
        database.commit()

        # update the episode nuumber
        episode_number+=1

if __name__ == '__main__':

    while True:
            
        # Get the current hour
        hour = datetime.datetime.now().hour

        # If the time is one of the below, check for new episodes
        if hour == 3 or hour == 21:

            # Get the a list containing the ids for the animes you are currently watching
            watching_list = get_watching_list()

            # Itertate through each anime_id
            for anime_id in watching_list:

                # Get a list of dicts containing the anime_id and the episode_number
                downloaded_episodes = get_downloaded_episodes(anime_id=anime_id)

                # Get the main url for that anime, so we can get a list of all released animes
                main_anime_url = get_main_url_from_id(anime_id)

                # Get all animes released so far
                referers,raw_mp4_urls = get_anime_links(anime_url=main_anime_url)

                # Get only the data for the newly added episodes
                referers = parse_new_episodes(downloaded_episodes=downloaded_episodes,released_episodes=referers)
                raw_mp4_urls = parse_new_episodes(downloaded_episodes=downloaded_episodes,released_episodes=raw_mp4_urls)

                # Download the new episodes
                download_new_releases(anime_id=anime_id,number_of_downloaded_episodes=len(downloaded_episodes),new_releases_referers=referers,new_releases_raw_mp4=raw_mp4_urls)

                # sleep for an hour
                time.sleep(3600)

        else:
            time.sleep(60*30)