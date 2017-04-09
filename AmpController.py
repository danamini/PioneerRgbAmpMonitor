#!/usr/bin/env python
""" This module provides the implementation for the Pioneer Reciever controller."""
import time
import logging
from AmpModel import AmpModel
from AmpView import AmpView

class AmpController(object):
    """
    This is Amp Controller. It will create a new View and Model and provides
    the callback routing between the two of them.
    """

    def __init__(self, host, retryconnect, retryinterval, port):
        """ Constructor, set up logging, creat the model and view """
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s : %(message)s')

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initialising the Amp Controller")
        self.retryconnect = retryconnect
        self.retryinterval = retryinterval
        self.model = AmpModel(host, port, self.callback)
        self.view = AmpView()

    def run(self):
        """ The main controller loop. Stay in here until we're disconnected. """
        self.logger.debug('Controller starting')
        # If retryconnect is set to true then keep retrying
        if self.retryconnect:
            while self.model.connect() is False:
                self.logger.info('Receiver not found. Sleeping for %s second(s)',
                                 self.retryinterval)
                time.sleep(self.retryinterval)
        else:
            # Tell the model to connect to the amp
            if self.model.connect() is False:
                # we couldn't connect, so quit
                return
        # connected, get the initial amp state
        self.model.get_amp_snapshot()
        # loop forever, getting the latest data from the amp
        self.model.get_data()
        self.logger.debug('Controller has finished')

    def stop(self):
        """ Stops the contoller and disconncts from the view and model """
        self.logger.debug('Disconncecting the controller')
        if self.view != None:
            self.view.clear()
        if self.model != None:
            self.model.disconnect()
        self.view = None
        self.model = None

    def callback(self):
        """ Callback entry point to inform the view that something has changed. """
        self.logger.debug('Calling View callback')
        self.view.callback(self.model)
