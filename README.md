# Pioneer RGB Amp Monitor
This project allows you to display key information, in realtime, from your Pioneer AV Receiver on a RGB LED display. Using an Adafruit RGB display and Raspberry Pi this python code allows you to connect your Pioneer receiver and integrate and read the status of your device.

Information such as the current volume, input source, front line display, video and audio settings are displayed on the RGB display. The RGB display is updated as you use your reciever, for example changing the input source as you select different devices on your reciever. 

The code has been tested using a Raspberry Pi 2 and 3 and Pioneer VSX-925. It is likely that it will work on other 900/1000 range models, although see the notes below. 

You'll need to make sure your Pioneer reciever is connected to your local network and the Pi can see it.   

The display will look like this:![alt-text](https://github.com/danamini/PioneerRgbAmpMonitor/blob/master/images/RGB%20Display.JPG)
r
 ## Hardware
You'll need a Raspberry Pi (2 or 3), an Adafruit RGB matrix, a 64x32 RGB LED display, and a network connected Pioneer VSX Receiver. 

These links will help you understand what you need. If you're doing this from scratch you'll need to do a bit of soldering (not too difficult for a novice): 
* https://www.adafruit.com/product/2276
* https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

## Getting Started

### Dependencies
You'll need to get this github project https://github.com/adafruit/rpi-rgb-led-matrix. It contains `rgbmatrix.so` which you'll need to copy to the directory you've download this Pioneer python code to. The LED-matrix library is (c) Henner Zeller h.zeller@acm.org with GNU General Public License Version 2.0 http://www.gnu.org/licenses/gpl-2.0.txt

The monitor is also dependent on the Python Image Library (PIL). 

1. If you don't have PIP then run `sudo apt-get install python-pip`
2. run `sudo apt-get install python-imaging`

### Clone and run the Monitor
1. Clone the git repo to your Raspberry Pi.
2. Execute the command: `chmod +x ./run.sh`
3. Get the IP Address of your Pioneer Receiver and modify the `./run.sh` file.
4. Start the Monitor by either `./run.sh` or `sudo python AmpApp.py [address of your reciever]`
 
## AmpApp Usage
```
usage: AmpApp.py [-h] [-r RETRY] [-i RETRYINTERVAL] [-p PORT] host

positional arguments:
  host                  ip address/host name of reciever

optional arguments:
  -h, --help                show this help message and exit
  -r RETRY, --retry RETRY   retry connecting if reciever not found
  -i RETRYINTERVAL, --retryInterval RETRYINTERVAL
                            length, in seconds, to wait before retrying
  -p PORT, --port PORT      reciever port to connect to
```
Notes:
* You'll need to run python using sudo, as this is required to allow the Pi to access the GPIO.
* The default port to connect to the reciever is 8102, this is different on some other models. 

## Pioneer Connectivity
See https://www.pioneerelectronics.com/StaticFiles/PUSA/Files/Home%20Custom%20Install/SC-37-RS232.pdf for more details of the telnet (originally RS-232) based protocol that is used by the monitor to communicate with the reciever. If you look at that file you'll notice it is for a different model, however it looks like most Pioneer recievers use the same basic protocol. 

## Limitations
The code has been written for a 32x64 pixel display. If you want to use a different size display and fonts then you'll need to change the constants in the `AmpView.py` file:
```
    FONT1 = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    FONT2 = '/home/pi/rpi-rgb-led-matrix-master/fonts/5x7.pil'
    FONT3 = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

    PANEL_HEIGHT = 32
    PANELS = 2
    PANEL_WIDTH = 64
```
The default configuration assumes you've `git clone`'d `rpi-rgb-led-matrix` to `/home/pi`. 

## Known Bugs/Issues
* Retry interval not yet coded
* The reciever needs around 0.1 seconds between sending requested, need a better way to sync data

## Next Steps
This is a work in progress. Next steps are:
* Add Unit Tests
* Move font and panel values to AmpConstants
* Add multiple callbacks in to the AmpView to remove dependency on AmpModel
* Replace ImageText usage with new custom TextRegion class to allow decoupling of text from the display and to support animations (_work started_)
* _IoT_ the project by providing a RESTful interface to allow remote starting/stopping over HTTP (_work started_)
* Add a port scanner to locate a reciever on your local network, would mean you don't need to provide the hostname/ip 
* Add a command interface, to allow the reciever to be controlled via the same AmpModel
* Add other Views for Philips Hue (_work started_)
