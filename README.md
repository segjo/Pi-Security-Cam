# Pi-Security-Cam
Security camera system written in python

Setup:

1. Install motion and test your camera:
sudo apt-get update && sudo apt-get install motion -y

2. Clone project to home dir:
cd ~
git clone https://github.com/segjo/Pi-Security-Cam.git

3. Set motion configuration:
sudo mv /etc/motion.conf /etc/motion/motion.conf.back
sudo mv ~/Pi-Security-Cam/motion/motion.conf /etc/motion/

When a different user than pi, change path in motion
sudo nano /etc/motion/motion.conf 
on_motion_detected /home/<username>/workspace/alarm_system/Alarming.py

