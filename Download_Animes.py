import Anime_NAS
import requests
import json
import Moe
import sys
import os



# Create an instace of the moe class
twist_moe = Moe.Moe(driverPath='/home/pedro/Documents/Python/chromedriver')

# Get the tools to access the database
database,MyCursor = Anime_NAS.sql_connector()

# Get the anime_id that was passed as a terminal _
anime_id = int(sys.argv[1])

# Get the url from the anime
MyCursor.execute('SELECT main_url,anime_title FROM Animes WHERE anime_id = %d' %(anime_id))
raw_data = MyCursor.fetchall()
anime_data = Anime_NAS.convert_tuple(data=raw_data,keys=['main_url','anime_title'],return_type='DICT')


print(json.dumps(anime_data,indent=4))

# Get two lists, one with the raw urls and another with their referers
mp4_urls,referers = twist_moe.get_raw_urls(url=anime_data['main_url'],nEpisodes=100)

# clear the webdriver
twist_moe.finish()
print(json.dumps(mp4_urls,indent = 4))
print(json.dumps(referers,indent = 4))
with open('referers.txt','w') as file:
    file.write(json.dumps(referers,indent=4))
    file.write(json.dumps(mp4_urls,indent=4))

    
# Change to the correct directory 
os.chdir('/Users/pedrocruz/Desktop/Anime/')

# Make a directory for the new anime
os.system('mkdir "%s" ' %(anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')))

# change to the new directory
os.chdir(anime_data['anime_title'].replace('.','_').replace('/','_').replace(':',''))
static_path = 'Animes/'+anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')+'/%s'

episode_number = 1
# go through each url and download it
for raw_url,referer in zip(mp4_urls,referers):

    # Set up the session config
    session = requests.Session()
    session.headers.update({'referer':referer})

    # A Bool to determine if the download was successful
    done = False
    while done == False:

        # Make a request to the url
        response = session.get(raw_url)
        
        file_name = anime_data['anime_title'].replace('.','_').replace('/','_').replace(':','')+'_'+str(episode_number)+'.mp4'
        

        # Create the .mp4 file and write binary content
        with open(file_name,'wb') as video_file:

            video_file.write(response.content)

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
    