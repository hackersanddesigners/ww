#!/bin/bash

echo "`date` add $1 $2" >> /home/pi/usb.log
echo 1 > /home/pi/status
mount $2"1" /mnt
echo "" > /mnt/data
