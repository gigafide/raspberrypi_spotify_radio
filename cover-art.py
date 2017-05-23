#!/usr/bin/python
# Downloads cover-art for current song playing
# on MPD server and displays it on a 1.8" TFT LCD
#Requires a LastFM API key
#https://secure.last.fm/login?next=/api/account/create
#pip install python-mpd2
#pip install urllib2

#Add dependencies
import urllib
import xml.dom.minidom
import sys, os
from time import sleep
from mpd import MPDClient

#create an MPD Client connection variable
client = MPDClient()

#set the environment to the TFT LCD screen
os.environ["SDL_FBDEV"] = "/dev/fb1"

#create a variable to open URL's
opener = urllib.URLopener()

#create a variable for your Last FM API key
api_key = "INSERT LAST FM API KEY HERE"

#Keep attempting to connect to the MDP server until it is connected.
#While not connected, display temporary image on screen
connected = False
while not connected:
        try:
                client.connect("localhost", 6600)
                os.system("sudo fbi -T 2 -comments -d /dev/fb1 -noverbose -a startup_logo.jpg")
                connected = True

        except:
                pass

#Check to see which song is playing and grab the artist name and album name
#Search Last FM for corresponding artist and download the XML data
#Extract the album art cover from the XML data and save it to the computer
#Display the album art on the screen.
while True:
        artist = client.currentsong()['artist']
        album = client.currentsong()['album']
        #current, end = client.status()['time'].split(":")

        target = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={0}&artist={1}&album={2}".format(api_key, artist, album)

        data = opener.open(target).read()
        dom = xml.dom.minidom.parseString(data)

        imageNodes = dom.getElementsByTagName("image")
        imageUrl = ""

        for node in imageNodes:
                if node.attributes["size"].value == "large":
                        imageUrl = node.firstChild.data
                        urllib.urlretrieve(imageUrl, "cover_art.jpg")
                        os.system("sudo fbi -T 2 -comments -d /dev/fb1 -noverbose -a cover_art.jpg")
                        sleep(10)
                        break
                else:
                        pass

