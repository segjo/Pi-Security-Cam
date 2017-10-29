#!/usr/bin/env python3

#/home/pi/workspace/controller/

#from RPi import GPIO
import time
import datetime
import os
import configparser
import logging

import StateManager
import KeyCodeController
import LedController


# ************************************************
#  ************************************************
#  **                                            **
#  **                                            **
#  **  NOCH in Arbeit....     !!!                **
#  **                                            **
#  **                                            **
#  ************************************************
#  ************************************************






#
# Wartet auf in einem Enlosloop auf einen gueltigen Tatencode.
# Je nach Status wird entsprchend reagiert:
#    
# READY: Ueberwachung starten (Verzoegerung); Status -> ACTIV 
# ACTIC: Ueberwachung deaktivieren; Status -> READY
# ALARM: Ueberwachung dekativierung; (Alarming-Prozess wird abgebrochen); Status -> READY
#        
#    (Alarmierings-Prozzess laeuft in unbhaengigem Prozess: Effektiv alarmiert wird, wenn
#     der Status (ALARM) nicht innerhalb von einer gewissen Zeit auf READY geaendert wird)

#
#    Asynchrone Prozess..... ..
#      StateManager....
# 

logging.basicConfig(filename='../logs/controller.log', level=logging.DEBUG)
logging.info("-------Controller starts--------") 


#  
#  Konfiguration einlesen
#
config = configparser.ConfigParser()
config.sections()
try:
    config.read('../controller.conf')
    config.sections()
    key_code = config['Controller'].getint('key_code')  # TastenCode 
    activation_delay = config['Controller'].getint('activation_delay')  # Verzoegerung bis Ueberwachung (nach Aktivierung) beginnt
except Exception as e:
    logging.error("Can't read config" + e.__str__())
    quit()





StateManager.setState(StateManager.READY)

while True:
    print("WaitOnCode")
    KeyCodeController.waitOnCode(key_code, 0);     # auf (richtigen) TastenCode  warten

    state = StateManager.getState()
    print("State: " + state)
    
    if (state == b'READY'):
        print ("im READY")
        ###LedController.setLEDs(LedController.GREEN, LedController.BLUE_BLINKING);
        LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.BLINK)
        sleep(activation_delay)
        
        
        os.system("sudo motion start")
        logging.info("motion started")
        
        LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.ON)
        StateManager.setState(StateManager.ACTIV)
        
    else:   # ACTIV or ALARM
        print ("ELSE")
        os.system("sudo kill `pgrep motion`")
        logging.info("motion stoped")
        
        LedController.setLEDs_RedGreenBlue(off, on, off)
        StateManger.setState(StateMagager.READY)
