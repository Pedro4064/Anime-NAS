from flask import Flask
import threading
import Anime_NAS
import requests
import json
import Moe
import os

app = Flask(__name__)

# Global variables so they are accessible from any function
mp4_urls = []
referers = []
anime_data = {}

def download_episode():
    
    global mp4_urls
    global referers
    global anime_data
    global episodes_numbers

    # Check to see if there are more episodes to download, if not, exit the function 
    if len(mp4_urls) == 0:
        return "[DONE]"

    # Get the mp4_url and its referer + update the global list so no other thread downloads the same episode again
    mp4_url = mp4_urls[0]
    mp4_urls = mp4_urls[1:]

    referer = referers[0]
    referers = referers[1:]

    episode_number = episodes_numbers[0]
    episodes_numbers = episodes_numbers[1:]

    # Change to the correct directory 
    os.chdir('/animes/%s' %(anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')))

    # Set up the session config
    session = requests.Session()
    session.headers.update({'referer':referer})

    # A Bool to determine if the download was successful
    done = False
    while done == False:

        # Make a request to the url
        response = session.get(mp4_url,stream=True)
        
        # format the file name
        file_name = anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')+'_'+str(episode_number)+'.mp4'
        

        # Create the .mp4 file and write binary content
        with open(file_name,'wb') as video_file:

            # Iterate through the contect so not everything is stored in memory at once
            for chunk in response.iter_content(512):
                video_file.write(chunk)


        # Check to see the size of the file, if it is too small and error happened
        if os.path.getsize(file_name) < 10000:
            done = False
            print(os.path.getsize(file_name))

        else:
            done = True

        
        # Get the tools to access the database
        database,MyCursor = Anime_NAS.sql_connector()

        # Update the database
        MyCursor.execute("INSERT INTO Downloads(anime_id,episode_number,file_path) VALUES(%d,%d,'%s')" %(anime_id,episode_number,static_path %(file_name)))
        database.commit()

    # Use recursion to make the thread call itself and download any other episodes
    download_episode()

@app.route('/download_anime/anime_id=<anime_id>')
def download_all_episodes_from_id(anime_id):
        
    global mp4_urls
    global referers
    global anime_data
    global episodes_numbers

    # Create an instace of the moe class
    twist_moe = Moe.Moe()

    # Get the tools to access the database
    database,MyCursor = Anime_NAS.sql_connector()


    # Get the url from the anime
    MyCursor.execute('SELECT main_url,anime_title FROM Animes WHERE anime_id = %s' %(anime_id))
    raw_data = MyCursor.fetchall()
    anime_data = Anime_NAS.convert_tuple(data=raw_data,keys=['main_url','anime_title'],return_type='DICT')


    print(json.dumps(anime_data,indent=4))

    # Get two lists, one with the raw urls and another with their referers
    mp4_urls,referers = twist_moe.get_raw_urls(url=anime_data['main_url'],nEpisodes=1000)
    episodes_numbers = range(1,len(referers)+1)

    # clear the webdriver
    twist_moe.finish()
    print(json.dumps(mp4_urls,indent = 4))
    print(json.dumps(referers,indent = 4))
       
    # Change to the correct directory 
    os.chdir('/animes')

    # Make a directory for the new anime
    os.system('mkdir "%s" ' %(anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')))

    # change to the new directory
    os.chdir(anime_data['anime_title'].replace('.','_').replace('/','_').replace(':',''))
    static_path = 'Animes/'+anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')+'/%s'

    
    # Create 5 threads to download 5 episodes Cconcurrently
    # threads = []
    # for i in range(5):

    #     threads.append(threading.Thread(target=download_episode))
    #     threads[i].start()

    # for thread in threads:
    #     thread.join()
    download_episode()
        
    return 'DOWNLOADING %s' %(anime_data['anime_title'])

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=80)