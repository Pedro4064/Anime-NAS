from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from typing import Tuple
import requests
import json
import time


class Moe(webdriver.Chrome, webdriver.chrome.options.Options, webdriver.common.by.By, webdriver.support.ui.WebDriverWait):

    def __init__(self, driverPath: str = '/usr/lib/chromium-browser/chromedriver'):

        # Added the headless option
        self.options = webdriver.chrome.options.Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')

        # Initialize the web driver
        self.driver = webdriver.Chrome(driverPath, options=self.options)

        # The wait for elements config -> 10 seconds
        self.wait = webdriver.support.ui.WebDriverWait(self.driver, 50)

        # Main twist Mow url
        self.mainURL = 'https://twist.moe'

    def get_all_animes_in_database(self) -> list:
        """Method that goes to the twist.moe website and gets all the anime titles and the urls for the first
        episodes for every one of them. 

        Returns:
            list: A list of dictionaries that contain the 'anime_title' and 'main_url' for each anime on twist
            moe 
        """

        # Go to the main URL
        self.driver.get(self.mainURL)

        # wait for the first element to appear
        _ = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located(
            (webdriver.common.by.By.XPATH, '//*[@id="__layout"]/div/div[1]/section/main/div[2]/nav/ul/li[1]/a')))

        # Get all the animes html element on the page and save the title and url in a list of dictionaries
        animes_data = self.driver.find_elements_by_class_name('series-title')
        animes_data = [{'anime_title': anime.get_attribute('innerHTML').split(
            '\n')[1].replace('            ', ''), 'main_url': anime.get_attribute('href')} for anime in animes_data[:5]]

        return animes_data

    def get_raw_urls(self, url: str, nEpisodes: int) -> Tuple[list, list]:
        """Method that gets the raw mp4 urls for all the episodes of an anime

        Args:
            url (str): The link of the first episode of the anime
            nEpisodes (int): The number of episodes to get the raw mp4 url

        Returns:
            Tuple(list, list): mp4_raw_urls, episodes' urls
        """

        urls = []
        rawUrls = []

        # Go to the url
        self.driver.get(url)

        # Check to see if it is a movie or a series, they have different xPaths
        try:

            # wait for the first element to appear, if there is an element it is a series, set the firstItem as an xPath for series
            firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[2]/a'
            _ = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located(
                (webdriver.common.by.By.XPATH, firstItem)))

        except:

            try:
                # Since it is not a series it must be a movie, set the firstItem xPath to match that of a movie
                print('Trying to get the url of a movie...')
                firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li/a'

                _ = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located(
                    (webdriver.common.by.By.XPATH, firstItem)))

            except:
                # It can be a yota case, so set the correct xpath
                print('Trying to get the url for yota...')
                firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[1]/a'

                _ = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located(
                    (webdriver.common.by.By.XPATH, firstItem)))

        time.sleep(3)

        # Search for urls - starting from the 1st url on page
        for i in range(1, nEpisodes+2):

            try:

                # find and append the url in a list
                url = self.driver.find_element_by_xpath(
                    '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[%d]/a' % (i)).get_attribute('href')
                urls.append(url)

                if __name__ == '__main__':
                    print(url)

            except:

                if i != 1:
                    break
                else:
                    continue

        #  Go to each url and get the raw url
        for url in urls:

            try:

                # go to the url
                self.driver.get(url)

                # wait for the first item to load
                _ = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located(
                    (webdriver.common.by.By.XPATH, firstItem)))
                time.sleep(5)

                # get the raw URL
                rawUrl = self.driver.find_element_by_xpath(
                    '//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src')
                rawUrls.append(rawUrl)

                if __name__ == '__main__':
                    print(rawUrl)

            except Exception as e:
                print(e)

        # return two lists, one with the mp4 urls and another with their respective 'referers'
        return rawUrls, urls

    def finish(self) -> None:
        """Method to close and correctly quit the chrome driver
        """

        # close the webdriver
        self.driver.quit()


if __name__ == '__main__':

    # Creates an instance of the Moe class
    twistMoe = Moe(driverPath='/Applications/chromedriver')
    # animes = twistMoe.get_all_animes_in_database()
    print(twistMoe.get_raw_urls('https://twist.moe/a/high-school-fleet/1', 3))

    # clean up and close the webdriver
    twistMoe.finish()

    # /media/pi/PEDRO CRUZ/AnimeInfo
