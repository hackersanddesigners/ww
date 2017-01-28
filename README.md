# ww

This is the "user generated religion" installation.  Once the Raspberry Pis are booted there should be an open network called "Wailing Wall".  Join this network to make modifications and manage the pis.

## WiFi

The installation requires internet.  You can connect to a WiFi network as follows.

In the Terminal of your computer connect to the pi.  Passwords are "arnhemarnhem".

    $ ssh pi@10.1.1.1

Once connected to the pi. In nano Ctl+o is save, Ctl+x quits.

    $  sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Change the file, ssid is the network name, psk is the network password.

    network={
        ssid="circa...dit"
        psk="circa...dat"
        priority=1
    }

Reboot the pi.

    $ sudo reboot

## Shutdown the pis

    $ ssh pi@10.1.1.2 "sudo poweroff"

    $ ssh pi@10.1.1.1 "sudo poweroff"

## The Chat Bot

The chatbot is based on the python version of Eliza and is in this repository in the directory `ww/pi1/ww-conf`.  You can test the chat bot by running the following.

    $ cd ww/pi1/ww-conf

    $ python main.py

Edit the file `bot.py` to make changes to the chatbot.  Once you are happy with it, copy it to the pi as follows.

    $ scp bot.py pi@10.1.1.1:ww-conf

Restart the pi1.

    $ ssh pi@10.1.1.1 "sudo reboot"

## Visuals - editing HTML

All projections are simple HTML and CSS.  You can edit the following files.

### Pi 1

    ww/pi1/ww-conf/index.html
    ww/pi1/ww-conf/mz.css

### Pi 2

    ww/pi2/ww-heav/index.html
    ww/pi2/ww-heav/ww.css

### Test

You can test by running the following.  You must be in the correct directory or folder for which ever pi you want to test (they both have their own `server.sh`).

    $ sudo ./server.sh

You will need some data so run the following (only once).

    $ mkdir /data

Create a file called "data" in that directory with text, can be any text.

In the browser: `https://localhost/index.html` for pi 1, or `http://localhost/index.html` for pi 2. 

Copy changes to the pis.

    $ scp ww/pi1/ww-conf/index.html pi@10.1.1.1:ww-conf

    $ scp ww/pi1/ww-conf/mz.css pi@10.1.1.1:ww-conf

    $ scp ww/pi2/ww-heav/index.html pi@10.1.1.2:ww-heav

    $ scp ww/pi2/ww-heav/ww.css pi@10.1.1.2:ww-heav

## Scripture

The scripture is saved and generated in a text file located at `/data/scripture`.  Download it, print it, design it...whatever.

    $ scp pi@10.1.1.2:/data/scripture .

## Testing/Debugging USB

    $ ssh pi@10.1.1.2

You can see add and remove events by running the following.

    $ tail -f /var/log/usb.log

