#!/usr/bin/env bash

DOWNLOAD_URL=$1

function download_chrome_driver() {
    case "$(uname -s)" in
	    Linux*) wget -O chromedriver -q $DOWNLOAD_URL && unzip -oq chromedriver;;
	    Darwin*) wget -O chromedriver -q $DOWNLOAD_URL && unzip -oq chromedriver;;
    esac
}


function python_stuff() {
    pip install -q -r requirements.txt &&
    python database.py
}

function get_credentials() {
    read -p "AU Email address: " EMAIL_ADDRESS
    read -sp "password: " PASSWORD
    echo -e "EMAIL=$EMAIL_ADDRESS\nPASSWORD=$PASSWORD" > .env
}

echo "Installing required dependencies..." &&
python_stuff &&
echo "Installing chrome driver..." &&
download_chrome_driver &&
get_credentials
python auris.py
