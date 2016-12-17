# templogger
Raspberry Pi temperature logger that send temps to InitialState.com. Includes a shutdown switch to shutdown your Pi and a status light to let you know your script is running

To setup your raspberry pi Install Raspbian

Configure your Pi 

$ sudo nano /boot/config.txt

$ sudo apt-get install git-core

$ git clone https://github.com/MikeBrawley/templogger.git

if the following line is not alaready in this file, add it and save the file 

$ dtoverlay=w1-gpio,gpiopin=4

restart your Pi for the changes to take affect

$ sudo reboot

Install Initial State

$ cd /home/pi/ $ \curl -sSl https://get.initialstate.com/python -o - | sudo bash

To set the TempLogger to auto run

$ sudo nano crontab -e

Add the following line to the bottom of the file 

@reboot sudo python /home/pi/templogger/templogger.py
