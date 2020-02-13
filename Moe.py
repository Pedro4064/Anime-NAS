from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
import requests
import json
import time
# Number of animes = 1584

class Moe(webdriver.Chrome,webdriver.chrome.options.Options,webdriver.common.by.By,webdriver.support.ui.WebDriverWait):

    def __init__(self, driverPath:str = '/Applications/chromedriver'):

        # Added the headless option 
        self.options = webdriver.chrome.options.Options()
        self.options.add_argument('--headless')

        # Initialize the web driver
        self.driver = webdriver.Chrome(driverPath,options=self.options)

        # The wait for elements config -> 10 seconds
        self.wait = webdriver.support.ui.WebDriverWait(self.driver,10)

        # Main twist Mow url 
        self.mainURL = 'https://twist.moe'
  
    def __format_data(self,ids:list, names:list, urls:list):

        formatte_data = [{'id':Id, 'anime_title':name, 'main_url': url} for Id,name,url in zip(ids,names,urls)]

        return formatte_data

    def get_all_animes_in_database(self):

        # Go to the main URL
        self.driver.get(self.mainURL)

        # wait for the first element to appear
        ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, '//*[@id="__layout"]/div/div[1]/section/main/div[2]/nav/ul/li[1]/a')))

        names = []
        urls = []
        ids = []

        # Try to get 10.000 names
        for i in range(1,2000):
            
            try:
                ids.append(i)
                names.append(self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/main/div[2]/nav/ul/li[%d]/a/span' %(i)).text)
                urls.append(self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/main/div[2]/nav/ul/li[%d]/a' %(i)).get_attribute('href'))

                # print (str(i)+'-',self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/main/div[2]/nav/ul/li[%d]/a/span' %(i)).text)
            

            except:

                # print(e)
                continue

        # format the data
        data = self.__format_data(ids = ids, urls=urls,names=names)

        return data

    def get_raw_urls(self, url:'The anime url', nEpisodes:'The number of episodes it will try to get the url from'):

        urls = []
        rawUrls = []

        
        # Go to the url
        self.driver.get(url)

        # Check to see if it is a movie or a series, they have different xPaths
        try:

            # wait for the first element to appear, if there is an element it is a series, set the firstItem as an xPath for series
            firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[2]/a'
            ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))

        except:

            # Since it is not a series it must be a movie, set the firstItem xPath to match that of a movie
            print('Trying to get the url of a movie...')
            firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li/a'
            
            ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))
        
        
        time.sleep(3)


        # Search for urls - starting from the 1st url on page
        for i in range(1,nEpisodes+2):

            try:

                # find and append the url in a list
                url = self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[%d]/a' %(i)).get_attribute('href')
                urls.append(url)
            
                if __name__ == '__main__':
                    print(url)

            except:
                continue
        

        #  Go to each url and get the raw url 
        for url in urls:

            try:

                # go to the url
                self.driver.get(url)
                

                # wait for the first item to load
                ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))
                time.sleep(5)
             
                
                # get the raw URL
                rawUrl = self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src')
                rawUrls.append(rawUrl)

                if __name__ == '__main__':
                    print(rawUrl)

            except Exception as e:
                print(e)

        # return two lists, one with the mp4 urls and another with their respective 'referers'
        return rawUrls,urls

    def read_file(self):

        # open the json file containing all the anime's names and urls
        with open('Animes.json', 'r') as file:

            jsonData = json.loads(file.read())

        # return the json data
        return jsonData

    def finish(self):

        # close the webdriver
        self.driver.quit()


#################################################################################
def save_urls(Id:int,url:str):

    # Create an instance of the class Moe
    twistMoe = Moe()
    
    try:

        # Try to get a maximum of 100 urls
        rawAnimeUrls,AnimeUrls = twistMoe.get_raw_urls(url, 100)

        # Creats a dictionary, so we can use json.dumps to format and save it
        jsonDic = [ {'url': url, 'rawUrl': rawUrl} for url,rawUrl in zip(AnimeUrls,rawAnimeUrls)]

        # format the filename 
        path = '/Users/pedrocruz/Desktop/Programming/Python/Git/TwistMoeAPI/AnimeInfo/'

        if Id < 10:
            sId = '000'+str(Id)
        
        elif Id <100:
            sId = '00' + str(Id)

        elif Id <1000:
            sId = '0'+str(Id)
        else:
            sId = str(Id)

        path = path+sId+'.json'

        # Save the file
        with open(path, 'w') as file:

            file.write(json.dumps(jsonDic, indent=4))

    except Exception as e:
        print(e)

    # Close the driver 
    twistMoe.finish()

def save_data(path:'the path for the json file'):

    # Create an instance of the Moe class
    moe = Moe()

    # get the data
    data = moe.get_all_animes_in_database()

if __name__ == '__main__':
    
    # Creates an instance of the Moe class
    twistMoe = Moe()
    

    # clean up and close the webdriver
    twistMoe.finish()
    
    
    # /media/pi/PEDRO CRUZ/AnimeInfo