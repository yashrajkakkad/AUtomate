import requests
from bs4 import BeautifulSoup as bs
import re
import subprocess
import platform

DOWNLOAD_HOMEPAGE = "https://chromedriver.chromium.org/downloads"
DOWNLOAD_URL_PREFIX = "https://chromedriver.storage.googleapis.com/index.html"

res = requests.get(DOWNLOAD_HOMEPAGE)
res.raise_for_status()
res = res.text
soup = bs(res, 'lxml')
links = soup.find_all(href=re.compile(r"\A"+DOWNLOAD_URL_PREFIX))

chrome_version = None
os_name = ""
if platform.system() == "Linux":
    chrome_version = subprocess.check_output(
        ['google-chrome-stable', '--product-version'])
    os_name = "linux"
elif platform.system() == "Darwin":
    chrome_version = subprocess.check_output(
        ['/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome', '--version'])
    os_name = "mac"
else:
    print("This script is for Linux users only. Please check instructions for your operating system in the README")
    exit()
chrome_version = str(chrome_version)[2:]
chrome_version = chrome_version[:len(chrome_version)-3]

DOWNLOAD_PAGE = ""
for link in links:
    x = re.search(r"\bpath="+chrome_version[:2], link.get('href'))
    if x is not None:
        DOWNLOAD_PAGE = link.get("href")
        break

DOWNLOAD_URL = "https://chromedriver.storage.googleapis.com/" + \
    DOWNLOAD_PAGE.split("=")[1] + "chromedriver_" + os_name + "64.zip"
subprocess.call(['./start.sh', DOWNLOAD_URL])
