# ww

This is the "user generated religion" installation.  Once the Raspberry Pis are booted there should be an open network called "Wailing Wall".  Join this network to make modifications manage the pis.

## WiFi

The installation requires internet.  You can connect to a WiFi network as follows.

In the Terminal of your computer connect to the pi.  Passwords are "arnhemarnhem".

    $ ssh pi@10.1.1.1

Once connected to the pi. In nano Ctl+w is save, Ctl+x quits.

    $  sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Change the file, ssid is the network name, psk is the network password.

    network={
        ssid="circa...dit"
        psk="circa...dat"
        priority=1
    }

## Shutdown the pis

    $ ssh pi@10.1.1.1 "sudo poweroff"

    $ ssh pi@10.1.1.2 "sudo poweroff"

## The Chat Bot

The chatbot is based on the python version of Eliza and is in this repository in the directory `ww/pi1/ww-conf`.  You can test the chat bot by running the following.

    $ cd ww/pi1/ww-conf

    $ python main.py

Edit the file `bot.py` to make changes to the chatbot.  Once you are happy with it, copy it to the pi as follows.

    $ scp boy.py pi@10.1.1.1:ww-conf



