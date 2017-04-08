 # Pioneer RGB Amp Monitor
A visual monitor using a Adafruit RGB display on a Raspberry Pi. The simple python code allows you to replicate your Pioneer AV Receivers display on a AdaFruit RGB Display.
The project uses your Pioneer receivers telnet port to integrate and read the current status of your device.

The code has been tested using a Pioneer VSX-925. It is likely to work on other 900/1000 range models. 

More information, images, parts list and unit tests to be added shortly.

## Hardware
You'll need a Raspberry Pi (2 or 3), an Adafruit RGB matrix, a 64x32 RGB LED display, and a network connected Pioneer VSX Receiver. 

These links will help: 
* https://www.adafruit.com/product/2276
* https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

## Getting Started
1. Clone the git repo to your Raspberry Pi (it's been tested on a Pi 2 and Pi 3).
2. Execute the command: `chmod +x ./run.sh`
3. Get the IP Address of you Pioneer Receiver and modify the `./run.sh` file.
4. Start the Monitor by either `./run.sh` or `sudo python AmpApp.py [address of your reciever]`

You'll need to get this github project https://github.com/adafruit/rpi-rgb-led-matrix. It contains `rgbmatrix.so` which is you'll need to copy to the directory you've download this Pioneer python code to. 

The LED-matrix library is (c) Henner Zeller h.zeller@acm.org with GNU General Public License Version 2.0 http://www.gnu.org/licenses/gpl-2.0.txt
 
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
* You'll need to run the python using sudo, as this is required to allow the Pi to access the GPIO.
* The default port to connect to the reciever is 8102, this is different on some other models. 

## Pioneer Connectivity
See https://www.pioneerelectronics.com/StaticFiles/PUSA/Files/Home%20Custom%20Install/SC-37-RS232.pdf for more details of the telnet (originally RS-232) based protocol that is used by the monitor to communicate with the reciever. 

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

## Next Steps
This is a work in progress. Next steps are:
* Provide a RESTful interface based on Flask to allow remote control
* Add Unit Tests
* Add other Views, maybe for Philips Hue
