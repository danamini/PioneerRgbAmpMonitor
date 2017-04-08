#!/usr/bin/env python
""" Helper to convert between raw values and strings."""

class AmpDataMappings(object):
    """ Simple mapping class between returned data and display values."""
    INPUT_TERMINAL = ['---',
                      'VIDEO',
                      'S-VIDEO',
                      'COMPONENT',
                      'HDMI',
                      'Self OSD/JPEG']
    INPUT_RESOLUTION = ['---',
                        '480/60i',
                        '576/50i',
                        '480/60p',
                        '576/50p',
                        '720/60p',
                        '720/50p',
                        '1080/60i',
                        '1080/50i',
                        '1080/60p',
                        '1080/50p',
                        '1080/24p']
    INPUT_FREQUENCY = ['32kHz',
                       '44.1kHz',
                       '48kHz',
                       '88.2kHz',
                       '96kHz',
                       '176.4kHz',
                       '192kHz']

    def get_input_terminal(self, terminal_code):
        """ Convert the received input terminal information in to a string."""
        return self.INPUT_TERMINAL[terminal_code]

    def get_input_resolution(self, resolution_code):
        """ Convert the recieved input resoliution in to a string."""
        return self.INPUT_RESOLUTION[resolution_code]

    def get_input_frequency(self, frequency_code):
        """ Convert the recieved input frequency in to a string."""
        return self.INPUT_FREQUENCY[frequency_code]
