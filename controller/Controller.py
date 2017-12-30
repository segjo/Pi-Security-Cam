#!/usr/bin/env python3

#/home/pi/workspace/controller/

#from RPi import GPIO
import time
import datetime
import os
import configparser
import logging
import dbm
import StateManager
import KeyCodeController
import LedController


#
# Wartet auf in einem Enlosloop auf einen gueltigen Tatencode.
# Je nach Status wird entsprechend reagiert:
#    
# READY: Ueberwachung (mit Verzoegerung) starten; Status -> ACTIV 
# ACTIV: Ueberwachung deaktivieren; Status -> READY
# ALARM: Ueberwachung dekativierung; (Alarming-Prozess wird abgebrochen); Status -> READY
#        
#    (Alarmierings-Prozzess laeuft in unbhaengigem Prozess: Effektiv alarmiert wird, wenn
#     der Status (ALARM) nicht innerhalb von einer gewissen Zeit auf READY geaendert wird)


logging.basicConfig(filename='../logs/controller.log', level=logging.DEBUG)
logging.info("-------Controller starts--------") 

def getState(state):
    with dbm.open('../state', 'r') as db:
        if state == 'controller':
            return db.get('controller_state')
        if state == 'quit':
            return db.get('quit_state')
    
def setState(state, value):
    with dbm.open('../state', 'c') as db:
        if state == 'controller':
            db['controller_state'] = value 
        if state == 'quit':
            db['quit_state'] = value
           
#  
#  Konfiguration einlesen
#
config = configparser.ConfigParser()
config.sections()
try:
    config.read('../alarming.conf')
    config.sections()
    key_code = config['Controller'].getint('key_code')  # TastenCode 
    activation_delay = config['Controller'].getint('activation_delay')  # Verzoegerung bis Ueberwachung (nach Aktivierung) beginnt
except Exception as e:
    logging.error("Controller: Can't read config" + e.__str__())
    quit()

#
# 
#
setState("controller", "READY")
LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.OFF)
while True:
    logging.info("Controller: wait on correct Key-Code")
    KeyCodeController.waitOnCode(key_code, None);     # auf (richtigen) TastenCode  warten  (ohne Timeout)
    
    if getState('controller') == b'READY':
        logging.info("controller: start surveillance in " + activation_delay + " seconds")
        for i in range (0, 2 * activation_delay): 
            LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.ON)
            time.sleep(0.25)
            LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.OFF)
            time.sleep(0.25)
        
        os.system("sudo motion &")
        logging.info("controller: motion started")
        setState("quit", "null")
        
        LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.ON)
        setState("controller", "ACTIV")
    else:   # ACTIV or ALARM
        logging.info("controller: deactivate surveillance/alarming")
        os.system("sudo kill `pgrep motion`")
        logging.info("controller motion stopped")
        setState("quit", "true")
        
        LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.OFF)
        setState("controller", "READY")

