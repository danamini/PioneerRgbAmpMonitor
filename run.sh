#!/bin/bash
echo Starting Amp App

# use the default arguments, change this address match your pioneer recievers
# us need to run as sudo as Raspberry Pi GPIO access requires this.
sudo python AmpApp.py 192.168.0.125