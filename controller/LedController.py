#!/usr/bin/env python3

#/home/pi/workspace/controller/

from RPi import GPIO
import time
import datetime
import os
import logging
import configparser



# Konstanten
ON = 0    
OFF = 1

def init():
    # GPIOs initialieren  
    GPIO.setmode(GPIO.BCM)

def cleanup():
    GPIO.cleanup()

def setLEDs_RedGreenBlue(red, green, blue):
    # mehrere Argumente möglich
    # pro Argument Farbe und Status kombiniert (z.B. 38 = GREEN | BLINKING: grüne LED blinkt)
    #  oder fixe Anzahl Argumente und nur on/off
    
    init()
    
    # Lese Konfiguration
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read('../alarming.conf')
        config.sections()
        led_red = config['GPIO'].getint('led_red')
        led_green = config['GPIO'].getint('led_green')
        led_blue = config['GPIO'].getint('led_blue')
    except:
        logging.error("Can't read config")
        quit()
    
    GPIO.setwarnings(False)             #  da Channels bereits in use...
    GPIO.setup(led_red, GPIO.OUT)
    GPIO.output(led_red, red) 
    
    GPIO.setup(led_green, GPIO.OUT)
    GPIO.output(led_green, green)
    
    GPIO.setup(led_blue, GPIO.OUT)
    GPIO.output(led_blue, blue)


if __name__ == '__main__':
    # Testcode wenn Programm nicht als Modul ausgeführt wird
    #
    init()
    print("alle LEDs aus")
    setLEDs_RedGreenBlue(OFF, OFF, OFF)
    time.sleep(2)
    print("alle LEDs an")
    setLEDs_RedGreenBlue(ON, ON, ON)
    time.sleep(2)
    print("aus und Ende")
    setLEDs_RedGreenBlue(OFF, OFF, OFF)
    cleanup()

    


    