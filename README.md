# Pi-Security-Cam
Security camera system written in python


Installation
-----------

1. Install motion and test your camera:
```
sudo apt-get update && sudo apt-get install motion -y
```

2. Clone project to home dir:
```
cd ~
git clone https://github.com/segjo/Pi-Security-Cam.git
```

3. Set motion configuration:
```
sudo mv /etc/motion.conf /etc/motion/motion.conf.back
sudo mv ~/Pi-Security-Cam/motion/motion.conf /etc/motion/
```
When a different user than pi, change path in motion config
```
sudo nano /etc/motion/motion.conf 

line on_motion_detected /home/<username>/workspace/alarm_system/Alarming.py
```
4. Set alarming configuration:
```
cp alarming-default.conf alarming.conf
nano alarming.conf 
```

5. Autostart
```
sudo nano /etc/rc.local 
```
add this two lines above ```exit 0```

```cd /home/pi/Pi-Security-Cam/controller/```

```./Controller.py```
