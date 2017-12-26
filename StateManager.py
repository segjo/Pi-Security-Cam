#!/usr/bin/env python3

#/home/pi/workspace/controller/

import dbm



# ************************************************
#  ************************************************
#  **                                            **
#  **                                            **
#  **  NOCH in Arbeit....     !!!                **
#  **                                            **
#  **                                            **
#  ************************************************
#  ************************************************



READY = b'READY' 
ACTIV = b'ACTIV'
ALARM = b'ALARM'

#!/usr/bin/python
#
def setState(state):
    print("StateManager.setState: " + state.__str__())
    db = dbm.open('state.db', 'c')
    db['state'] = state
    db.close
    
def getState():
    db = dbm.open('state.db', 'c')
    state = db['state'].__str__()
    db.close
    print("StateManager.getState returns: " + state.__str__())
    return state

if __name__ == '__main__':
    # Testcode wenn Programm nicht als Modul ausgefuehrt wird
    #
    getState()
    setState(ALARM)
    getState()
    setState(READY)
    getState()