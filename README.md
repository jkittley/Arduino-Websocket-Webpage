# Displaying live data from an arduino in a web browser

In this tutorial we show how a Raspberry Pi serving webpages can present live data streamed from a connected Arduino. Why? Well this project came about when I was designing an [outreach project](#footnotes) for Exeter University. We needed to present live data streams on a large public display.

We began with the following observations: Arduino's are excellent for quick hardware hacks and HTML5 technologies are ideal for fast visualisation development as there are so many free libraries. This project provides a kind of black-box setup, where strings (JSON encoded data) outputted from the Arduino are piped (via a web socket) to the browser and replies fed back.

## To make things simpler the tutorial is divide into the following section:

1. [Setup the Pi](#basic-raspberry-pi-setup)
2. [Flask web server setup](#flask-web-server-setup)
3. [Connect the Arduino to the web socket](#connect-the-arduino-to-the-web-socket)
4. [Let's play pong](#lets-play-pong)
5. [Turn the Pi into an Access Point Setup (Optional)](#access-point-setup)

## Things you will need
* Raspberry Pi (preferably v3) with monitor, keyboard and mouse. Older models of the Pi will work, but if you intend to use the Pi's browser to display a page, it is worth using the latest model as its much quicker. Also the settings may require some tinkering with other wifi adapters.
* An Arduino, any model should do, we used Nanos and Unos
* USB cable to connect the Pi and the Arduino
* Power supplies

## End product
The purpose of this code and the tutorial is to give you a framework / skill set on which you can build your own project. It is not a finished article and as such elements such as error checking have been omitted in order to make the code more readable and easier to understand. This is what you will build:

[![Example Use](http://img.youtube.com/vi/PEcfkao6sfE/0.jpg)](http://www.youtube.com/watch?v=PEcfkao6sfE)



# Basic Raspberry Pi Setup
First of all install the latest version Raspbian (howto: https://www.raspberrypi.org/help/videos/) and connect it to the internet.

If you choose to use a different OS the please make sure the file system is expanded to use the full capacity of the SD Card. If you have used NOOBS then skip this step, it has been done already for you.
* Open terminal and type “raspi-config”.
* Choose the “expand Filesystem” option and reboot the Pi

Next let make sure the system is up to date.
* Launch the command line / terminal and run the following
* ```sudo apt-get update```


# Flask web server setup
Check you have Python 3 and Pip installed
* ```sudo apt-get install python3-pip```

Make a new directory for the web server and move into it
* ```mkdir ~/www```
* ```cd ~/www```

Clone the project code from github and step into the directory
* ```git clone https://github.com/jkittley/gameconsole.git```
* ```cd gameconsole```

Install all the library requirements
* ```sudo pip3 install -r requirements.txt```

That's it, now we can test the web server.
* ```sudo python3 webserver.py --prod```

You should see something like this:
```
<flask_socketio.SocketIO object at 0x102f610f0>
 * Restarting with stat
<flask_socketio.SocketIO object at 0x10388b128>
 * Debugger is active!
 * Debugger pin code: 661-779-075
(10072) wsgi starting up on http://0.0.0.0:80
```

Now the server is up and running you can open the web browser, type ```localhost``` in the address bar and hit enter. You should see the webpage being served.


# Connect the Arduino to the web socket
Open the terminal and move to the 'www' directory we made earlier.
* ```cd ~/www/```

Clone the project code from github and step into the directory
* ```git clone https://github.com/jkittley/gamepad.git```
* ```cd gamepad```

Install all the library requirements
* ```sudo pip3 install -r requirements.txt```

Now to setup the Arduino. If you don't already have the IDE installed on the Pi then run:
* ```sudo apt-get install arduino```

Open the IDE by either:
1. Use the Raspberry Pi menu system > Programming > Arduino IDE
2. Type ```arduino &``` in the terminal. The & is important, it tells the terminal to open in the background.

Connect the Arduino to the Pi via a USB cable and make sure you have the port and board type set correctly.

Open the file: ```arduino/testconnection/testconnection.ino``` in the Arduino IDE and upload it to the Arduino.

Open the serial monitor to make sure it is outputting information periodically e.g. { test: 39 }.

Close the serial monitor and run the web server
* ```sudo ~/www/gameconsole/webserver.py```

Open a new terminal window and run the serialmonitor.py script
* ```sudo ~/www/gamepad/serialmonitor.py```
* Select the Arduino's port from the list (usually /dev/ttyACM0) and hit enter.

You should now see that the serial monitor script connects to the web socket server by the webserver.py script and that it monitors the serial port and reads the Arduino.

Now switch to the web server terminal window and you should see the same data streaming in e.g. from_serial_monitor: { test: 39 }.

Finally open the web browser and open the test data page. You should see the test data stream by. Also there is a button which should send a message back to the Arduino which will toggle the LED status.


# Let's play pong
Now we have a working system, let's do something fun. Tennis anyone?

You will need:
* HC-SR04 Ultrasound Range Finder
* SG90 5v Servo
* Some wire

First connect the components as follows:

![Pong Arduino setup](https://raw.githubusercontent.com/jkittley/gameconsole/master/readme/pong_arduino_setup.png)

Note: SG90 wire colours may be different to those shown in the diagram. Commonly: Orange=signal, Red=Vcc and Brown=Gnd. See http://www.fatlion.com/sailplanes/servos.html for more color schemes.

Next make sure serialmonitor.py is not running, Ctrl-C to terminate.

Open the file: ```~/www/gamepad/arduino/pong/pong.ino``` in the Arduino IDE and upload it.

Now restart the serialmonitor.py
* ```sudo ~/www/gamepad/serialmonitor.py```

Make sure the webserver is still running and open the browser.

Select 'pong' from the main menu and see what happens. You should be able to control the left paddle by moving your hand up and down front of the range sensor (approx 5 to 10cm). When the ball goes out of play the servo should twitch!

## Next

You may have noticed that there is another game, Snake. This game expects  to control the direction of the snake. Why not try making your own Arduino script which outputs

* { "keystroke": 37 } for 'left'
* { "keystroke": 38 } for 'up'
* { "keystroke": 39 } for 'right'
* { "keystroke": 40 } for 'down'


# Access Point Setup
In this section we will cover how to turn you Pi into an access point (adapted from: https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/). This will enable you to connect external machines to view the web page. This can be very helpful if your webpage is processor intensive. When using a Pi as a web server it is important to remember the limited resources available, as such push the processing to the browser i.e. using javascript to do the heavy lifting, is a good idea.

First, get your Pi connected to the internet using Ethernet. It will make your life much easier later. We need to use the Wifi for the access point.

Install the two key packages required
* ```sudo apt-get install dnsmasq hostapd```

Now we need to set a static IP address for wlan0
* ```sudo nano /etc/dhcpcd.conf```
* Add the following to the bottom of the file:

```
interface wlan0  
    static ip_address=172.24.1.1/24
```

Next we need to prevent wpa_supplicant from running and interfering with setting up wlan0 in access point mode.
* ```sudo nano /etc/network/interfaces```
* Comment out the line that looks like:

```
allow-hotplug wlan0  
iface wlan0 inet manual  
   wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

So it looks like this

```
allow-hotplug wlan0  
iface wlan0 inet manual  
#   wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

Restart dhcpcd
* ```sudo service dhcpcd restart```

Configure HostAPD by creating a new config file.
* ```sudo nano /etc/hostapd/hostapd.conf```

Add the following to the new file. Don't forget you can open this page in the Pi's browser and copy-paste :)

```
# This is the name of the WiFi interface we configured above.
interface=wlan0

# Use the nl80211 driver with the brcmfmac driver.
driver=nl80211

# This is the name of the network.
ssid=GameConsole

# Use the 2.4GHz band.
hw_mode=g

# Use channel 6.
channel=6

# Enable 802.11n.
ieee80211n=1

# Enable WMM.
wmm_enabled=1

# Enable 40MHz channels with 20ns guard interval.
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

# Accept all MAC addresses.
macaddr_acl=0

# Use WPA authentication.
auth_algs=1

# Require clients to know the network name.
ignore_broadcast_ssid=0

# Use WPA2.
wpa=2

# Use a pre-shared key.
wpa_key_mgmt=WPA-PSK

# The network passphrase.
wpa_passphrase=raspberry

# Use AES, instead of TKIP.
rsn_pairwise=CCMP
```

Before you save, you can edit the following
* ssid - The name of your wireless network
* wpa_passphrase - The password


We can check if it's working by running
# ```sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf```

If it's all gone well thus far, you should be able to see to the network with SSID you chose in the list of available networks on any device nearby. However if you try connecting to it, you will see some output from the Pi, but it wont work as you might expect.
* Use Ctrl+C to stop it.

We also need to tell hostapd where to look for the config file when it starts up on boot
* sudo nano /etc/default/hostapd
* find the line ```#DAEMON_CONF=""```
* replace it with ```DAEMON_CONF="/etc/hostapd/hostapd.conf"```
* Exit and save

Next we will setup dnsmasq. Move the config file out of the way
* ```sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig```

Now make a new config file
* ```sudo nano /etc/dnsmasq.conf```
* paste the following into the file

```
# Use interface wlan0  
interface=wlan0      

# Bind to the interface to make sure we aren't sending things elsewhere  
bind-interfaces

# Forward al domains to local webserver
address=/#/172.24.1.1

# Assign IP addresses between 172.24.1.50 and 172.24.1.150 with a 12 hour lease time
dhcp-range=172.24.1.50,172.24.1.150,12h  
```

One of the last things that we need to do before we send traffic anywhere is to enable packet forwarding.
* ```sudo nano /etc/sysctl.conf```
* remove the # from the beginning of the line containing net.ipv4.ip_forward=1
* save and reboot it:
* ```sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"```

Start the services
* ```sudo service hostapd start```
* ```sudo service dnsmasq start```

Finally reboot the Pi
* ```sudo reboot```

Start the web server running
* Open terminal and type:
* ```sudo python3 ~/www/gameconsole/webserver.py —prod```

Now you should be able to connect to the Pi via WiFi. Navigate to http://game.console in the browser and you should see the website.


# Footnotes

This tutorials origin. Dr Anne Le Brocq, a glaciologist at Exeter University, wanted a way to explain the seabed scanning technologies used in Antarctica to school children. Together we conceived and built the Ocean Scan project. Click to watch the video on Youtube.

[![Ocean-Scan Project](http://img.youtube.com/vi/Y7ZZm3ZpZCg/0.jpg)](http://www.youtube.com/watch?v=Y7ZZm3ZpZCg)
