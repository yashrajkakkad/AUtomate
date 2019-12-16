# AUtomate

AUtomate scrapes your attendance and marks from AURIS (Ahmedabad University Resource Information System) on your behalf and stores them in a database. 

It controls your web browser to do several things for you. As you might expect, it uses Selenium to control the browser and BeautifulSoup4 to do the required scraping work.

Features:
  - Notifies the updates in attendance in all subjects.
  - Notifies if marks of a component are added (eg. Quiz 1 marks in Linear Algebra)
  - Adds subjects automatically


# Installation
  - Clone this repository
```sh
git clone https://github.com/yashrajkakkad/AUtomate.git
```
  - Install the required Python packages in your system or a virtual environment.
```sh
pip install -r requirements.txt
```
  - Create the database tables. Executing 'database.py' will create a file called 'db.sqlite3' for you.
```sh
python database.py
```
  - Download [ChromeDriver](https://chromedriver.chromium.org/downloads) (Web Driver for Google Chrome) and place it in the main folder. Make sure that it is called "chromedriver".
  - Create a new file called '.env' and add the following (replace yourname@email.com with your e-mail address and yourpassword with your Ahmedabad University Mail password **(not AURIS password)**:
```
EMAIL=yourname@email.com
PASSWORD=yourpassword
```
  - Run the main script. If running for the first time, it'll add all the courses and attendance data. Thereafter, it will only show what has changed from the last time.
```sh
python auris.py
```

If you like my work or find it helpful please "Star" this repository. Pull requests are welcome too!
