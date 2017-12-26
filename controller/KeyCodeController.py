#!/usr/bin/env python3

from RPi import GPIO
import time, signal
from threading import Timer
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
KEY_1 = 19
KEY_2 = 20
KEY_3 = 21



def handler(signum, frame):
    print('Signal handler called with signal' +  signum.__str__())
    print ("Timeout fuer TastenCode eingabe abgelaufen")
    raise Exception('NO_KEYCODE')


def waitOnCode(keycode, timeout):
    return waitOnCodePolling(keycode, timeout)
    
    #print("waitOnCode: " + keycode.__str__())
    #print("codeLength: " + len(keycode.__str_()))
          
    #if timeout > 0: 
    #    # Set the signal handler and a 5-second alarm
    #    signal.signal(signal.SIGALRM, handler)
    #    signal.alarm(timeout)        # (maximal solage auf Timeout warten....)

    ## jetzt auf gültigen Code oder Timeoutwarten
    #try:
    #    retCode = waitOnCodePolling(keycode, timeout)
    #    print("alles OK: " + ex)
    #    print("Code OK: " + retVal.__str__())
    #except Excepiton(ex):
    #    print("Exception: " + ex)
    #    print("Timeout")
    #finally:
    #    if timeout > 0:
    #       signal.alarm(0)    # Disable the alarm
          


def waitOnCodePolling(keycode, timeout):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(KEY_1, GPIO.IN)
    GPIO.setup(KEY_2, GPIO.IN)
    GPIO.setup(KEY_3, GPIO.IN)

    
    key_list = [KEY_1, KEY_2, KEY_3]
    
    print("Wait on Code Polling....")
    
    start = time.time()
    print("start" + start.__str__())
    print("diff" + (time.time() - start).__str__() )
    
    CodeString = "";

    keyCodeLen = len(keycode.__str__())
    
        
    #
    # Maximal n (=Code-Laenge) Tasten abfragen
    #    bei falscher Taste wir wieder neu begonnen
    #    (Falsch-Eingaben werden ignoriert)
    #
    #
    
    print("CodeString: " + CodeString)
    while (timeout == 0) or (time.time() - start < timeout):

        for ix in range(len(key_list)):
            if not GPIO.input(key_list[ix]): # and btnReleased_list[ix]:
                print("Taster " + (ix + 1).__str__() + " gedrueckt")
            
                # warten bis taste xy wider losgelassen wird
                while(1):
                    if GPIO.input(key_list[ix]):
                        print("Taster " + (ix +1).__str__() + " losgelassen")
                
                        CodeString = CodeString + (ix + 1).__str__()
                        if len(CodeString) > keyCodeLen:
                            CodeString = CodeString[-keyCodeLen:]
                        
                        if len(CodeString) == keyCodeLen:
                            if CodeString == keycode.__str__():
                                print("KeyCode korrekt! (keyCode: " + keycode.__str__() + ")")
                                GPIO.cleanup() 
                                return True
                        
                        print("CodeString: " + CodeString)
                        
                        
                        break
            
        time.sleep(0.01)

        #print("CodeString ------: " + CodeString)    
    
    print("Timeout abgelaufen")
    GPIO.cleanup() 
    return False;        



if __name__ == '__main__':
    # zum Testen
    #
    #try:
    #    signal.signal(signal.SIGALRM, handler)
    #    signal.alarm(120)
    #    waitOnCodePolling(123123, 300)
    #except Exception(exc):
    #         print("Exception: " + exc.__str__())
    #         signal.alarm(0)          # Disable the alarm

    if waitOnCode(123321, 20):
        print("richtiger Code wurde eingegeben")
    else:
        print("Timeout abgelaufen bevor richtiger Code eingegeben wurde")    
    
