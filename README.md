# ANIME N.A.S

• Web app writen in Python using Flask and MySQL to manage and download animes;
</br>
• Using a Raspberry Pi 3b+ and a 2.5"HDD as the "server".
</br>
• Access from any device in the network.

--- 
## Details

• The application uses python as the main programming language.

• It uses MySQL to store the path to all the anime episodes downloaded to the system as well as  "Favorites", "Watching", and "Downloaded" lists.

• If you add an anime to the "Downloaded" list it will automatically download all episodes for that anime from the website [twist.moe](https://twist.moe/) using the python modules: Requests and Selenium, as well as the chrome WebDirver that is used with the Raspberry Pi's default browser Chromium.

• It also uses the  [Kitsu.io](https://kitsu.docs.apiary.io/) api to get the thumbnails for all animes in the database.

• The front end is made using HTML5 and css, and it is served by the flask application. 

• It can be accessed from any device within the same network.

---
## Getting Started

#### Prerequisites
• Libraries and drivers you need to install to deploy the application.
##### Raspberry Pi

• Make sure your system is running the latest version of raspbian by running:
</br>
```bash
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

-Obs: If it's your first time with a Raspberry Pi, follow this [introductory article](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) by the Pi Foundation.

##### Python
• Support for python3 or greater.</br>
• To download all modules just change to the default pip directory and download from the requirements.txt:

1. Find the default location for pip3. The output of this command is the default location for pip3 in your system:
   ```bash
   which pip3
   ```
2. Change to that directory:
   ```bash
   cd path/to/default_pip3_location
    ```
3. Pip install from requirements.txt
    ```bash
   sudo python3 -m pip3 install -r path/to/requirements.txt 
   ```
##### Mysql
•Follow [this tutorial](https://pimylifeup.com/raspberry-pi-mysql/) up to step 8 to set up MySQL database on your Raspberry Pi.
</br>

##### WebDriver
 • Follow this [instructions](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/) to download chrome webdriver that is used by the selenium module to download animes from [Twist Moe](https://twist.moe/) . <br/>

#### Set Up The Database
