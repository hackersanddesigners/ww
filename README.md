# ww

This is the "user generated religion" installation.  Once the Raspberry Pis are booted there should be an open network called "Wailing Wall".  Join this network to make modifications manage the pis.

## WiFi

The installation requires internet.  You can connect to a WiFi network as follows.

In the Terminal of your computer connect to the pi.  Passwords are "arnhemarnhem".

    $ ssh pi@10.1.1.1

Once connect to the pi.

    $  sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Change the file, ssid is the network name, psk is the network password.

    network={
        ssid="circa...dit"
        psk="circa...dat"
        priority=1
    }

