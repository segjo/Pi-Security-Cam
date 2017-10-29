#!/usr/bin/env python3

from RPi import GPIO
import time
import datetime
import os
import Mail
from Mail import send_mail
import configparser
import dbm
import logging

#Check ob bereits einen Alarm verarbeitet wird
if os.path.exists("alarming.lock"):
    if os.path.exists("detection.lock")==False:
        os.mknod("detection.lock")
#Neuer Alarm, da kein alarming.lock.Folgender Bereich darf nicht mehrfach ausgeführt werden
else:
    logging.basicConfig(filename='../logs/alarming.log',level=logging.DEBUG)
    logging.info("-------Alarming process starts--------")
    os.mknod("alarming.lock") 
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setwarnings(False)
    except:
        logging.error("some troubles with GPIO's")
        quit()
    
    #Lese Konfigurationen
    config = configparser.ConfigParser()
    config.sections()
    config.read('../alarming.conf')
    config.sections()
    
    detection_time = config['detection'].getint('detection_time') #Verzögerung nach letzter Bewegung, bis Aufzeichnung beendet ist
    alarm_send_delay = config['detection'].getint('alarm_send_delay') #Verzögerung bis einen Alarm versendet wird (Zeit Muss kleiner sein als detection Time)
    capture_dir = config['detection']['capture_dir']#Ordner wo die Bilder und Videos gespeichert werden
    save_videos = config['detection'].getboolean('save_videos') #True Falls die Vidoes der Aufnahmen gespeichert werden sollen

    server = config['E-Mail']['server']
    port = config['E-Mail']['port']
    useTLS = config['E-Mail']['useTLS']
    username = config['E-Mail']['username']
    password = config['E-Mail']['password']
    send_from = config['E-Mail']['send_from']
    send_to = config['E-Mail']['send_to']
    subject = config['E-Mail']['subject']
    max_pictures = config['E-Mail'].getint('max_pictures')
    text = "Hallo \nUm "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" wurde eine Bewegung erkannt. Die Aufnahmen sind im Anhang zu finden. \nGrüsse Pi Überwachungskamera"
    
    
    
    # Schalte Rote LED ein
    GPIO.output(18, False)
    alarm_send=False
    startTime = time.time()
    last_detection = startTime
    
    #Aufnahmen von frühren Ereignissen werden ins Archiv verschoben
    for f in os.listdir(capture_dir):
                if f.endswith(".jpg"):
                    logging.info("Delete old picutres "+os.path.join(capture_dir, f))
                    os.remove(os.path.join(capture_dir, f))
    
    #Nach 20Sekunden nach der letzten Bewegung oder nach der Quittierung wird die Schlaufe verlassen
    while (time.time() - last_detection<=detection_time and os.path.exists("alarm_quit.info")==False):
        logging.info("Last Detection: "+ int(round(time.time() - last_detection)).__str__() +"<"+detection_time.__str__())
        if time.time() - startTime>=alarm_send_delay and alarm_send==False:
            #Alarm wird versendet
            logging.info("Alarm will be send")
            sended=send_mail(send_from, send_to, subject, text, capture_dir, max_pictures,server, port, username, password, useTLS)
            if not sended:
                logging.warning("E-Mail was not transmitted")
            alarm_send=True

        time.sleep(1)
  

        
        #Neue Bewegung erkannt
        if os.path.exists("detection.lock"):
            last_detection = time.time()
            os.remove('detection.lock')
            
    GPIO.output(18, True)
    
    #Bestätigung für die Quittierung des Alarms
    if os.path.exists("alarm_quit.info"):
        os.remove('alarm_quit.info')
        #GPIO.output(23, False)
        #GPIO.output(23, True)
    
    #Aufnahmen archivieren 
    for f in os.listdir(capture_dir):
            if save_videos:
                if f.endswith(".jpg"):
                    logging.info("Delete "+os.path.join(capture_dir, f))
                    os.remove(os.path.join(capture_dir, f))
            else:
                logging.info("Delete "+os.path.join(capture_dir, f))
                os.remove(os.path.join(capture_dir, f))
                    

    GPIO.cleanup() 
    if os.path.exists("detection.lock"):
        os.remove('detection.lock')
    os.remove('alarming.lock')
    logging.info("-------Alarming process ends--------")