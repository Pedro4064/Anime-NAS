import requests
import json
import time
# Number of animes = 1584

class cover_api():

    def __init__(self, driverPath:str = '/Applications/chromedriver'):

        # Base url
        self.main_url = 'https://kitsu.io/api/edge/anime?filter[text]=%s'
       

    def get_cover(self,anime_title):


        # format the url
        url = self.main_url %(anime_title)

        # make the request to the rest api
        response = requests.get(url)

        # Check to see if the response is 200(successfull) or 400(no data)
        if response.status_code != 200:

            print('[ERROR] No data for',anime_title)
            return False

        try:
            # Parse the data and returnt the url for the cover
            json_data = json.loads(response.content.decode())
            cover_path = json_data['data'][0]['attributes']['posterImage']['large']
            
            # return the url
            return cover_path

        except:
            print('[ERROR]',anime_title)

        