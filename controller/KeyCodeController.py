#!/usr/bin/env python3

from RPi import GPIO
import time, signal
from threading import Timer
import os
import datetime
import logging
import configparser



def waitOnCode(keycode, timeout):
    # Lese Konfiguration
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read('../alarming.conf')
        config.sections()
        key_1 = config['GPIO'].getint('button_1')
        key_2 = config['GPIO'].getint('button_2')
        key_3 = config['GPIO'].getint('button_3')
    except:
        logging.error("Can't read config")
        quit()
    
    key_list = [key_1, key_2, key_3]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(key_1, GPIO.IN)
    GPIO.setup(key_2, GPIO.IN)
    GPIO.setup(key_3, GPIO.IN)

    
    logging.info("KeyCodeController: wait on key-code (polling) at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    start = time.time()
    
    CodeString = "";
    keyCodeLen = len(keycode.__str__())
    
        
    #
    # Solange warten, bis die zuletzt eingegebnen Tasten dem Key-Code entsprechen oder
    # bis der (optionale) Timeout abläuft
    # (bisher eingegebener Code-String wird fortlaufend auf die maximale Key-Laenge gekuerzt)
    #
    #
    
    while (timeout is None) or (time.time() - start < timeout):

        for ix in range(len(key_list)):
            if not GPIO.input(key_list[ix]): # and btnReleased_list[ix]:
                if __name__ == '__main__':
                    # im TEST-Modus eingegebene Tasten/Tastencode fortlaufend anzeigen
                    print("Taster " + (ix + 1).__str__() + " gedrueckt")
            
                # warten bis taste xy wider losgelassen wird
                while(1):
                    if GPIO.input(key_list[ix]):
                        if __name__ == '__main__':
                            # im TEST-Modus eingegebene Tasten/Tastencode fortlaufend anzeigen
                            print("Taster " + (ix +1).__str__() + " losgelassen")
                
                        CodeString = CodeString + (ix + 1).__str__()
                        if len(CodeString) > keyCodeLen:
                            CodeString = CodeString[-keyCodeLen:]
                        
                        if len(CodeString) == keyCodeLen:
                            if CodeString == keycode.__str__():
                                logging.info("KeyCodeLController: correct key-code entered at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                GPIO.cleanup() 
                                return True
                        
                        if __name__ == '__main__':
                            # im TEST-Modus eingegebene Tasten/Tastencode fortlaufend anzeigen
                            print("CodeString: " + CodeString)
                                                
                        break
            
        time.sleep(0.01)
    
    logging.info("KeyCodeController: Timeout occured at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    GPIO.cleanup() 
    return False;        



if __name__ == '__main__':
    #
    # Nur zum Testen (KeyCodeCotroller direkt gestartet und nicht als Modul/Funktion verwendet)
    #
    print("Warte 20 Sekunden bzw. bis Code 123321 eingegeben wurde")
    if waitOnCode(123321, 20):
        print("richtiger Code wurde eingegeben")
    else:
        print("Timeout abgelaufen bevor richtiger Code eingegeben wurde")    
    
