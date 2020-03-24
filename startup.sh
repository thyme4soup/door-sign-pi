#!/bin/bash
cd /home/pi/door-sign-pi/ && /usr/bin/git pull && /usr/bin/pip3 install -r requirements.txt
/usr/bin/python3 /home/pi/door-sign-pi/fauxmo_receiver.py &
