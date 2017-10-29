#!/usr/bin/env python3

#/home/pi/workspace/controller/

#from RPi import GPIO
import time
import datetime
import subprocess

import StateManager

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
# Wartet auf in einem Enlosloop auf einen gültigen Tatencode.
# Je nach Status wird entsprchend reagiert:
#    
# READY: Überwachung starten (Verzögerung); Status -> ACTIV 
# ACTIC: Uberwachung deaktivieren; Status -> READY
# ALARM: Überwachung dekativierung; (Alarming-Prozess wird abgebrochen); Status -> READY
#        
#    (Alarmierings-Prozzess läuft in unbhängigem Prozess: Effektiv alarmiert wird, wenn
#     der Status (ALARM) nicht innerhalb von einer gewissen Zeit auf READY geändert wird)

#
#    Asynchrone Prozess..... ..
#      StateManager....
# 


# readConfig()
#
#Folgende Parameter sollen zu einen spätern Zeitpunkt aus der Config Datei gelesen werden

start_delay=3      # Verzögerung bis Überwachung nach Aaktivierung eff. startet  BESSER 30 
taster_code=123321   # Tastencode
 


StateManager.setState(StateManager.READY)

while (true):
    print("WaitOnCode")
    TasterController.waitOnCode(taster_code, 0);     # auf (richtigen) TastenCode  warten

    state = StateManager.getStatus()
    print("State: " + state)
    
    if (state == StateManager.READY):
        ###LedController.setLEDs(LedController.GREEN, LedController.BLUE_BLINKING);
        LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.BLINK)
        sleep(start_delay)
        subprocess.call("motion")
        LedController.setLEDs_RedGreenBlue(LedController.OFF, LedController.ON, LedController.ON)
        StateManager.setState(StateManager.ACTIV)
        
    else:   # ACTIV or ALARM
        stopVideoMotion
        LedController.setLEDs_RedGreenBlue(off, on, off)
        StateManger.setState(StateMagager.READY)
