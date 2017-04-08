#!/usr/bin/env python
""" This module provides an implementation of the Pioneer Reciever VSX-925 Telnet
    communication protocol. It's very basic, having the ability to make requests
    to the reciever, and handle unsolicitied responses.
    This implementation should work on othr VSX-xxx receivers, but has only
    been tested against a VSX-925."""
import logging
import telnetlib
import time
import socket
import AmpConstants
from AmpDataMappings import AmpDataMappings

class AmpModel(object):
    """ Pioneer Reciever VSX-925 telnet access model."""
    def __init__(self, host, port, event_callback):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initialising the Amp Model")
        self.host = host
        self.port = port
        self.event_callback = event_callback
        self.volumne = ""
        self.display = ""
        self.source = ""
        self.sourcecode = ""
        self.video_info = ""
        self.audio_info = ""
        self.input_resolution = ""
        self.input_frequency = ""
        self.input_left_channel = False
        self.input_center_channel = False
        self.input_right_channel = False
        self.input_left_back_channel = False
        self.input_right_back_channel = False
        self.input_lfe_channel = False
        self.output_left_channel = False
        self.output_center_channel = False
        self.output_right_channel = False
        self.output_left_back_channel = False
        self.output_right_back_channel = False
        self.output_sub_channel = False
        self.telnet = None
        self.connected = False
        self.running = False
        self.mappings = AmpDataMappings()

    def connect(self):
        """ Connect to the Reciever."""
        self.logger.debug("Model connecting")
        self.connected = False
        try:
            self.logger.debug('Connect to Reciever %s:%s',
                              self.host,
                              self.port)
            self.telnet = telnetlib.Telnet(self.host, self.port)
            self.connected = True
            self.logger.debug('Connected successfully')
        except socket.error:
            self.logger.error('Failed to connect to reciever')
        self.running = True
        return self.connected

    def disconnect(self):
        """ Disconnect from the telnet session to the Reciever."""
        self.logger.debug('model is disconnecting')
        self.event_callback = None
        if self.telnet != None:
            self.telnet.close()
        self.running = False

    def get_amp_snapshot(self):
        """ Force an snapshot of the current state from the reciever."""
        self.amp_request(AmpConstants.VOLUME_REQUEST)
        self.amp_request(AmpConstants.FRONT_LINE_REQUEST)
        self.amp_request(AmpConstants.F_REQUEST)
        self.amp_request(AmpConstants.VIDEO_INFO_REQUEST)
        self.amp_request(AmpConstants.AUDIO_INFO_REQUEST)
        self.event_callback()

    def amp_request(self, request):
        """ helper to make an amp request, wait for a response, and process it """
        self.telnet.write(request)
        time.sleep(AmpConstants.COMMAND_WAIT)
        self.process_amp_data(self.telnet.read_some())

    def get_data(self):
        """ Main processsing loop. Sit here waiting for telnet data. When we have
            some decode it and raise a callback event."""
        while self.running:
            telnetdata = self.telnet.read_some()
            if self.process_amp_data(telnetdata):
                self.event_callback()
            time.sleep(AmpConstants.COMMAND_WAIT)
        self.logger.debug('Exiting get_data, is running has been set to false')

    def process_amp_data(self, msg):
        """ Process each line of telnet data that we have recieved. Setting the
            approproate model values as we decode them."""
        changed = False
        lines = msg.splitlines(False)
        for line in lines:
            if len(line) > 0:
                self.logger.debug('raw data : %s', line)
            if line.startswith(AmpConstants.VOLUME_RESPONSE_PREFIX):
                volume = line.strip(AmpConstants.VOLUME_RESPONSE_PREFIX)
                val = (float(161) - int(volume)) * 0.5
                val = val * -1
                self.logger.debug('VOL= %s', str(val))
                if self.volumne != (str(val)):
                    self.volumne = str(val)
                    changed = True
            if line.startswith(AmpConstants.FRONT_LINE_RESPONSE_PREFIX):
                line = line = line[4:]
                line = line.decode("hex")
                self.logger.debug('FL= %s', line)
                line = line.strip()
                if line != self.display:
                    self.display = line
                    changed = True
                    self.get_audio_data()
                    self.get_video_data()
            if line.startswith(AmpConstants.SOURCE_RESPONSE_PREFIX):
                line = line = line[2:]
                self.logger.debug('FN= %s', line)
                if self.sourcecode != line:
                    self.sourcecode = line
                    self.get_source_name(self.sourcecode)
            if line.startswith(AmpConstants.AUDIO_RESPONSE_PREFIX):
                line = line = line[3:]
                self.logger.debug('AST= %s', line)
                if self.audio_info != line:
                    self.audio_info = line
                    self.set_channel_data(self.audio_info)
                    changed = True
            if line.startswith(AmpConstants.VIDEO_RESPONSE_PREFIX):
                line = line = line[3:]
                self.logger.debug('VST= %s', line)
                if self.video_info != line:
                    self.video_info = line
                    self.set_video_data(self.video_info)
                    changed = True
            if line.startswith(AmpConstants.VIDEO_IMAGE_RESPONSE_PREFIX):
                line = line = line[6:]
                self.logger.debug('RGB= %s', line)
                if self.source != line:
                    self.source = line
                    changed = True
        return changed

    def get_source_name(self, source_code):
        """ Request the name of the current reciever source."""
        self.telnet.write(AmpConstants.SOURCE_INFO_REQUEST_PREFIX + source_code + '\r')

    def get_audio_data(self):
        """ Request details of the audio source data from the reciever."""
        self.telnet.write(AmpConstants.AUDIO_INFO_REQUEST)

    def get_video_data(self):
        """ Request details of the video source data from the reciever."""
        self.telnet.write(AmpConstants.VIDEO_INFO_REQUEST)

    def set_video_data(self, video_info):
        """ If we've recieved updated video information then extract the resolution."""
        if len(video_info) > 3:
            self.input_resolution = self.mappings.get_input_resolution(int(self.video_info[1:3]))

    def set_channel_data(self, audio_data):
        """ Convert the recieved multi-channel information in to their approriate
            model property."""
        self.input_frequency = self.mappings.get_input_frequency(int(audio_data[2:4]))
        self.logger.debug("Setting channel data: %s", str(len(audio_data)))

        if len(audio_data) < 29:
            self.input_left_channel = False
            self.input_center_channel = False
            self.input_right_channel = False
            self.input_left_back_channel = False
            self.input_right_back_channel = False
            self.input_lfe_channel = False
            self.output_left_channel = False
            self.output_center_channel = False
            self.output_right_channel = False
            self.output_left_back_channel = False
            self.output_right_back_channel = False
            self.output_sub_channel = False

        if len(audio_data) > 12:
            self.input_left_channel = int(audio_data[4:5]) == 1
            self.input_center_channel = int(audio_data[5:6]) == 1
            self.input_right_channel = int(audio_data[6:7]) == 1
            self.input_left_back_channel = int(audio_data[7:8]) == 1
            self.input_right_back_channel = int(audio_data[8:9]) == 1
            self.input_lfe_channel = int(audio_data[12:13]) == 1

        if len(audio_data) > 28:
            self.output_left_channel = int(audio_data[20:21]) == 1
            self.output_center_channel = int(audio_data[21:22]) == 1
            self.output_right_channel = int(audio_data[22:23]) == 1
            self.output_left_back_channel = int(audio_data[23:24]) == 1
            self.output_right_back_channel = int(audio_data[24:25]) == 1
            self.output_sub_channel = int(audio_data[28:29]) == 1

        self.logger.debug("IN L  = " + str(self.input_left_channel))
        self.logger.debug("IN C  = " + str(self.input_center_channel))
        self.logger.debug("IN R  = " + str(self.input_right_channel))
        self.logger.debug("IN LB = " + str(self.input_left_back_channel))
        self.logger.debug("IN RB = " + str(self.input_right_back_channel))
        self.logger.debug("IN LFE= " + str(self.input_lfe_channel))
        self.logger.debug("OU L  = " + str(self.output_left_channel))
        self.logger.debug("OU C  = " + str(self.output_center_channel))
        self.logger.debug("OU R  = " + str(self.output_right_channel))
        self.logger.debug("OU LB = " + str(self.output_left_back_channel))
        self.logger.debug("OU RB = " + str(self.output_right_back_channel))
        self.logger.debug("OU SB = " + str(self.output_sub_channel))
