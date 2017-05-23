#!/usr/bin/python
#Control MPD Client volume using a physical rotary encoder
#pip install mopidy-spotify
#pip install python-mpd2

#import dependencies
from mpd import MPDClient
from RPi import GPIO
from time import sleep

#declare variables
client = MPDClient()

clk = 17
dt = 27

#set GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#initialize counter, last click state, and starting volume.
counter = 0
clkLastState = GPIO.input(clk)
currVolume = 50

#try to connect to MPD server until connected
connected = False
while not connected:
        try:
                client.connect("localhost", 6600)
                client.setvol(currVolume)
                connected = True
        except:
                pass

#create a loop to check if knob state has been changed
#if so, adjust the volume accordingly
try:
        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                currVolume += 5
                        else:
                                currVolume -= 5
                        client.setvol(currVolume)
                        clkLastState = clkState
                        sleep(0.01)
finally:
        GPIO.cleanup
        client.close()
        client.disconnect()
