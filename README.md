# ANIME N.A.S

• Web app writen in Python using Flask and MySQL to manage and download animes;
</br>


</br>




## Details

• The application uses python as the main programming language.

• In My set up I'm using a  Raspberry Pi 3b+ and a 2.5" 500 GB HDD as the "server".

• It uses MySQL to store the path to all the anime episodes downloaded to the system as well as  "Favorites", "Watching", and "Downloaded" lists.

• If you add an anime to the "Downloaded" list it will automatically download all episodes for that anime from the website [twist.moe](https://twist.moe/) using the python modules: Requests and Selenium, as well as the chrome WebDirver that is used with the Raspberry Pi's default browser Chromium.

• It also uses the  [Kitsu.io](https://kitsu.docs.apiary.io/) api to get the thumbnails for all animes in the database.

• The front end is made using HTML5 and css, and it is served by the flask application. 

• It can be accessed from any device within the same network.

## Getting Started

### Prerequisites
• Libraries and drivers you need to install to deploy the application.
#### Raspberry Pi

• Make sure your system is running the latest version of raspbian by running:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

• Install the driver that lets you read an exFAT file system Hard Drive (Most Hard Drives) by typing:

```bash
sudo apt install exfat-fuse
sudo apt-get install exfat-utils
 ```
-Obs: If it's your first time with a Raspberry Pi, follow this [introductory article](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) by the Pi Foundation.

---

#### Hard Drive

• Inside the Hard Drive create a directory called `static` and inside that create another directory called `Animes`.

|

|_ This will be the directory where the program will store the directories and episodes for all animes.

• The path to the `Animes` directory should be the following:

`/media/pi/Hard_Drive_Name/static/Animes`

---

#### Python
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

---

#### Mysql
•Follow [this tutorial](https://pimylifeup.com/raspberry-pi-mysql/) up to step 8 to set up MySQL database on your Raspberry Pi.
</br>

---

#### WebDriver
 • Follow this [instructions](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/) to download chrome webdriver that is used by the selenium module to download animes from [Twist Moe](https://twist.moe/) . <br/><br/><br/><br/>

### Set Up The Database

#### Mysql

1. Open the MySQL Shell by typing `sudo mysql -u root -p` and typing your MySQL password when requested;

2. Once inside the MySQL Shell type the following command to set up the database: `source /path/to/Databse_setup.sql`
</br>

*obs: Where `/path/to/Databse_setup.sql` is the path to [Database_setup.sql](Database_setup.sql) in your system.

---

#### Populate the Database

• To populate the database we will be using the [Populate_db.py](Populate_db.py) script, but before that you'll need to change the mysql details in the [Anime_NAS.py](Anime_NAS.py) script to match the ones in your system, and change the webdriver path to the one in your sytem in the [Populate_db.py](Populate_db.py) script.

1. In [Anime_NAS.py](Anime_NAS.py), go to the `sql_connector` function (line 12) and change the `password` variable to your MySQL password.

2. In the [Populate_db.py](Populate_db.py) script (line 16), set the correct webdriver to match the one in your system:

   ```python
   twist_moe = Moe(driverPath="path/to/WebDriver")
   ```

3. After saving the changes, run the [Populate_db.py](Populate_db.py) script by typing : `python3 Populate_db.py`.

<br/>
<br/>
<br/>

### Set Up The Anime Downloader Script

1. In the [Download_Animes.py](Download_Animes.py) script, set the webdriver path to the one in your system (on line 11):

   ```python
   twist_moe = Moe.Moe(driverPath="path/to/WebDriver")
   ```
2. Also in the [Download_Animes.py](Download_Animes.py) script, set the  path to the `Animes` directory on your Hardrive (on line 40):

   ```python
   os.chdir('/media/pi/Hard_Drive_Name/static/Animes')
   ```