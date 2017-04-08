#!/usr/bin/env python
""" This module is contains the access methods in to the Pioneer Receiver
    application.  """
import argparse
from AmpController import AmpController

def start():
    """ Amp application main entry point """
    try:
        parser = argparse.ArgumentParser(description='Pioneer Reciever RGB Display.')
        parser.add_argument('host',
                            help='ip address/host name of reciever')
        parser.add_argument('-r', '--retry',
                            type=bool,
                            default=True,
                            help='retry connecting if reciever not found')
        parser.add_argument('-i', '--retryInterval',
                            type=int,
                            default=15,
                            help='length, in seconds, to wait before retrying')
        parser.add_argument('-p', '--port',
                            type=int,
                            default=8102,
                            help='reciever port to connect to')
        args = parser.parse_args()

        controller = AmpController(args.host,
                                   args.retry,
                                   args.retryInterval,
                                   args.port)
        controller.run()

    except KeyboardInterrupt:
        print "User interruted. Quiting."

start()
