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
    # GPIOs aufraeumen
    GPIO.cleanup()

def setLEDs_RedGreenBlue(red, green, blue):
    #
    # pro LED wird kann gewünschte Zustand (ON / OFF / None) mitgegeben 
    # (bei None bleibt der Zustand der entstrechenden LED wie er ist)
    
    logging.info("LedController: setLEDs_RedGreenBlue(" + red.__str__() + ", " + green.__str__() + ", " + blue.__str__() + ")")
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
    
    GPIO.setwarnings(False)             #  da Channels bereits "in use" sein kann

    if red is not None:
        GPIO.setup(led_red, GPIO.OUT)
        GPIO.output(led_red, red) 
    
    if green is not None:
        GPIO.setup(led_green, GPIO.OUT)
        GPIO.output(led_green, green)
    
    if blue is not None:
        GPIO.setup(led_blue, GPIO.OUT)
        GPIO.output(led_blue, blue)


if __name__ == '__main__':
    #
    # Nur zum Testen (LedController direkt gestartet und nicht als Modul/Funktion verwendet)
    #
    init()
    print("alle LEDs aus")
    setLEDs_RedGreenBlue(OFF, OFF, OFF)
    time.sleep(0.5)
    print("alle LEDs an")
    setLEDs_RedGreenBlue(ON, ON, ON)
    time.sleep(2)
    print("gruene LED aus")
    setLEDs_RedGreenBlue(None, OFF, None)
    time.sleep(2)
    print("aus und Ende")
    setLEDs_RedGreenBlue(OFF, OFF, OFF)
    cleanup()

    


    