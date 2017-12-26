#!/usr/bin/env python3

#/home/pi/workspace/controller/

from RPi import GPIO
import time
import datetime
import os


# ************************************************
#  ************************************************
#  **                                            **
#  **                                            **
#  **  NOCH in Arbeit....  !!!                   **
#  **                                            **
#  **                                            **
#  ************************************************
#  ************************************************





# Konstanten
RED = 64
GREEN = 32
BLUE = 16

ON = 0    
OFF = 1
BLINK = 4

LED_RED=18
LED_GREEN=25
LED_BLUE=23

def init():
    GPIO.setmode(GPIO.BCM)

def cleanup():
    GPIO.cleanup()

def setLEDs_RedGreenBlue(red, green, blue):
    # mehrere Argumente möglich
    # pro Argument Farbe und Status kombiniert (z.B. 38 = GREEN | BLINKING: grüne LED blinkt)
    #  oder fixe Anzahl Argumente und nur on/off
    
    init();
    GPIO.setwarnings(False)             #  da Channels bereits in use...
    GPIO.setup(LED_RED, GPIO.OUT)
    if red == BLINK:
        GPIO.output(LED_RED, 1)   # !! AENDERN auf Blinken...!!
    else:
        GPIO.output(LED_RED, red) 
    
    GPIO.setup(LED_GREEN, GPIO.OUT)
    if green == BLINK:
        GPIO.output(LED_GREEN, 1)   # !! AENDERN auf Blinken...!!
    else:
        GPIO.output(LED_GREEN, green)
    
    GPIO.setup(LED_BLUE, GPIO.OUT)
    if blue == BLINK:
        GPIO.output(LED_BLUE, 1)   # !! AENDERN auf Blinken...!!
    else:
        GPIO.output(LED_BLUE, blue)


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

    


    