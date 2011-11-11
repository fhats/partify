#!/bin/sh

# A quick and dirty force-feed script to get Partify and Mopidy up and running on Ubuntu systems

# installs Mopidy
wget -q -O - http://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list http://apt.mopidy.com/mopidy.list
sudo apt-get update
sudo apt-get install mopidy -y
sudo apt-get install python-setuptools -y

echo "Enter your Spotify Premium username: "
read spotify_username
echo "Enter your Spotify Premium password: "
stty -echo
read spotify_password ; echo
stty echo

sudo mkdir /root/.local
sudo mkdir /root/.local/share
sudo mkdir /root/.local/share/mopidy
sudo mkdir /root/.config
sudo mkdir /root/.config/mopidy
sudo rm /root/.config/mopidy/settings.py

sudo echo "SPOTIFY_USERNAME = '$spotify_username'" >> /root/.config/mopidy/settings.py
sudo echo "SPOTIFY_PASSWORD = '$spotify_password'" >> /root/.config/mopidy/settings.py

# install partify
sudo easy_install partify

cd /etc/init
sudo wget http://partify.us/static/scripts/partify.conf
sudo wget http://partify.us/static/scripts/mopidy.conf

# Run Partify!
sudo start mopidy
sudo start partify