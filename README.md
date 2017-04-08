# Pioneer RGB Amp Monitor
A visual monitor using a Adafruit RGB display on a Raspberry Pi. The simple python code allows you to replicate your Pioneer AV Receivers display on a AdaFruit RGB Display.
The project uses your Pioneer receivers telnet port to integrate and read the current status of your device.

The code has been tested using a Pioneer VSX-925. It is likely to work on other 900 range models.

More information, images, parts list and unit tests to be added shortly.

## Getting Started
Clone the git repo to your Raspberry Pi (it's been tested on a Pi 2 and Pi 3).
Execute the command: chmod +x ./run.sh
Get the IP Address of you Pioneer Receiver, and modify the ./run.sh file.
Start the Monitor by either: 
  ./run.sh 
  or,
  sudo python AmpApp.py [address of your reciever]
 
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

Note that you need to run the python using sudo, as this is required to allow the Pi to access the GPIO.
