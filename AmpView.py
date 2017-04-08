#!/usr/bin/env python
""" For driving an Adafruit RGB display view."""
import logging
from threading import Timer
import Image
import ImageDraw
import ImageFont
from ImageText import ImageText
from rgbmatrix import Adafruit_RGBmatrix

class AmpView(object):
    """ This is the Amp View, which displays reciever details on the Adafruit RGB matrix.
        It's set up for a 32x64 RGB display. """

    RED = (255, 0, 0)
    DIM_RED = (128, 0, 0)
    GREEN = (0, 255, 0)
    DIM_GREEN = (0, 128, 0)
    BLUE = (155, 48, 255)
    DIM_BLUE = (77, 24, 128)

    FONT1 = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    FONT2 = '/home/pi/rpi-rgb-led-matrix-master/fonts/5x7.pil'
    FONT3 = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

    PANEL_HEIGHT = 32
    PANELS = 2
    PANEL_WIDTH = 64

    def __init__(self):
        """ Initialise a new twitter display """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initialising the Amp View")
        self.matrix = Adafruit_RGBmatrix(AmpView.PANEL_HEIGHT, AmpView.PANELS)
        self.__load_fonts()

        self.volume = ""
        self.source = ""
        self.timer = None
        self.model = None

    def callback(self, model):
        """ This is the only public method, the entry point to updating the display."""
        self.model = model
        self.__refresh_display_vol(model.volumne)
        self.__refresh_display_front_line(model.display)
        self.__refresh_display_source(model.source)
        self.__refresh_display_input_res(model.input_resolution)
        self.__refresh_display_speakers(self.model.input_left_channel,
                                        self.model.input_center_channel,
                                        self.model.input_right_channel,
                                        self.model.input_left_back_channel,
                                        self.model.input_right_back_channel,
                                        self.model.input_lfe_channel,
                                        self.model.output_left_channel,
                                        self.model.output_center_channel,
                                        self.model.output_right_channel,
                                        self.model.output_left_back_channel,
                                        self.model.output_right_back_channel,
                                        self.model.output_sub_channel)
        self.timer = Timer(5, self.__dim)
        self.timer.start()

    def __clear(self):
        """ Clear the matrix display and reset the timer """
        self.logger.debug('Clear called')
        self.matrix.Clear()
        self.model = None
        self.timer = None
        self.matrix = None

    def __load_fonts(self):
        """ Load the fonts that will be used by the display """
        self.font1 = ImageFont.truetype(AmpView.FONT1, 10)
        self.font2 = ImageFont.load(AmpView.FONT2)
        self.font3 = ImageFont.truetype(AmpView.FONT3, 8)

    def __refresh_display_vol(self, msg):
        self.logger.debug("refresh vol: " + msg)
        self.__clear_region(0)
        self.__show_text(self.font3, msg, 0, AmpView.BLUE)

    def __refresh_display_front_line(self, msg):
        self.logger.debug("refresh front line: " + msg)
        self.__clear_region(9)
        self.__show_text(self.font1, msg, 9, AmpView.RED)

    def __refresh_display_source(self, msg):
        self.logger.debug("refresh source: " + msg)
        self.__clear_region(20)
        self.__show_text(self.font1, msg, 20, AmpView.GREEN)

    def __refresh_display_input_res(self, msg):
        self.logger.debug("refresh input resolution: " + msg)
        self.__clear_region(0, 25, 32, 8)
        self.__show_text(self.font3, msg, 0, AmpView.BLUE, 25)

    def __refresh_display_speakers(self,
                                   input_left_channel,
                                   input_center_channel,
                                   input_right_channel,
                                   input_left_back_channel,
                                   input_right_back_channel,
                                   input_lfe_channel,
                                   output_left_channel,
                                   output_center_channel,
                                   output_right_channel,
                                   output_left_back_channel,
                                   output_right_back_channel,
                                   output_sub_channel):
        """ The 5.1 channel speaker display """
        self.__draw_speakers(8, 1,
                             input_left_channel,
                             input_center_channel,
                             input_right_channel,
                             input_left_back_channel,
                             input_right_back_channel,
                             input_lfe_channel,
                             output_left_channel,
                             output_center_channel,
                             output_right_channel,
                             output_left_back_channel,
                             output_right_back_channel,
                             output_sub_channel)

    def __refresh_display_vol_dim(self, msg):
        """ The db volume display """
        self.logger.debug("dim vol: " + msg)
        self.__clear_region(0)
        self.__show_text(self.font3, msg, 0, AmpView.DIM_BLUE)

    def __refresh_display_frontline_dim(self, msg):
        self.logger.debug("dim front line: " + msg)
        self.__clear_region(9)
        self.__show_text(self.font1, msg, 9, AmpView.DIM_RED)

    def __refresh_display_source_dim(self, msg):
        self.logger.debug("dim source: " + msg)
        self.__clear_region(20)
        self.__show_text(self.font1, msg, 20, AmpView.DIM_GREEN)

    def __refresh_display_input_res_dim(self, msg):
        self.logger.debug("dim input resolution: " + msg)
        self.__clear_region(0, 25, 32, 8)
        self.__show_text(self.font3, msg, 0, AmpView.DIM_BLUE, 25)

    def __refresh_display_inputfreq_dim(self, msg):
        self.logger.debug("dim input frequency: " + msg)
        #self.clear_region(0,25,32,8)
        #self.show_text(self.font3, msg, 0, AmpView.DIM_BLUE, 25)

    def __refresh_display_speakers_dim(self,
                                       input_left_channel,
                                       input_center_channel,
                                       input_right_channel,
                                       input_left_back_channel,
                                       input_right_back_channel,
                                       input_lfe_channel,
                                       output_left_channel,
                                       output_center_channel,
                                       output_right_channel,
                                       output_left_back_channel,
                                       output_right_back_channel,
                                       output_sub_channel):
        self.__draw_speakers(8, 1,
                             input_left_channel,
                             input_center_channel,
                             input_right_channel,
                             input_left_back_channel,
                             input_right_back_channel,
                             input_lfe_channel,
                             output_left_channel,
                             output_center_channel,
                             output_right_channel,
                             output_left_back_channel,
                             output_right_back_channel,
                             output_sub_channel)

    def __clear_region(self, row, col=0, width=64, height=12):
        image = Image.new("RGB", (width, height), "black")
        ImageDraw.Draw(image)
        self.matrix.SetImage(image.im.id, col, row)

    def __show_text(self, font, msg, row, colour, col=0):
        msg = msg.strip()
        image = ImageText(font, msg, colour)
        self.matrix.SetImage(image.image.im.id, col, row)

        if len(msg) > 2:
            if ord(msg[0]) == 5 and ord(msg[1]) == 6:
                self.__draw_dolby_image(11, 0, colour)

        if len(msg) > 5:
            if ord(msg[4]) == 8:
                self.__draw_prologic_image(11, 26, colour)

    def __dim(self):
        self.__refresh_display_vol_dim(self.model.volumne)
        self.__refresh_display_frontline_dim(self.model.display)
        self.__refresh_display_source_dim(self.model.source)
        self.__refresh_display_input_res_dim(self.model.input_resolution)
        self.__refresh_display_inputfreq_dim(self.model.input_frequency)
        self.__refresh_display_speakers_dim(self.model.input_left_channel,
                                            self.model.input_center_channel,
                                            self.model.input_right_channel,
                                            self.model.input_left_back_channel,
                                            self.model.input_right_back_channel,
                                            self.model.input_lfe_channel,
                                            self.model.output_left_channel,
                                            self.model.output_center_channel,
                                            self.model.output_right_channel,
                                            self.model.output_left_back_channel,
                                            self.model.output_right_back_channel,
                                            self.model.output_sub_channel)
        self.timer.cancel()

    def __draw_dolby_image(self, row, column, colour):
        """ draw the dolby double DD image """
        image = Image.new("RGB", (12, 10), "black")
        draw = ImageDraw.Draw(image)
        draw.line([0, 0, 4, 0], fill=colour)
        draw.line([0, 0, 0, 6], fill=colour)
        draw.line([0, 6, 4, 6], fill=colour)
        draw.line([4, 6, 4, 0], fill=colour)
        draw.point([3, 1], fill=colour)
        draw.point([3, 5], fill=colour)

        draw.line([6, 0, 10, 0], fill=colour)
        draw.line([6, 0, 6, 6], fill=colour)
        draw.line([6, 6, 10, 6], fill=colour)
        draw.line([10, 6, 10, 0], fill=colour)
        draw.point([7, 1], fill=colour)
        draw.point([7, 5], fill=colour)

        self.matrix.SetImage(image.im.id, column, row)

    def __draw_prologic_image(self, row, column, colour):
        image = Image.new("RGB", (5, 10), "black")
        draw = ImageDraw.Draw(image)
        draw.line([0, 0, 4, 0], fill=colour)
        draw.line([1, 0, 1, 6], fill=colour)
        draw.line([0, 6, 4, 6], fill=colour)
        draw.line([3, 6, 3, 0], fill=colour)

        self.matrix.SetImage(image.im.id, column, row)

    def __draw_speakers(self,
                        row,
                        column,
                        l,
                        c,
                        r,
                        lb,
                        rb,
                        lfe,
                        output_l,
                        output_c,
                        output_r,
                        output_lb,
                        output_rb,
                        output_sub):
        """ Draw the speakers using on pixel each. It's configured for 5.1 layout """
        image = Image.new("RGB", (14, 3), "black")
        draw = ImageDraw.Draw(image)

        if l:
            draw.point([0, 0], fill=(25, 25, 112))
        if c:
            draw.point([1, 0], fill=(25, 25, 112))
        if r:
            draw.point([2, 0], fill=(25, 25, 112))
        if lb:
            draw.point([0, 1], fill=(25, 25, 112))
        if rb:
            draw.point([2, 1], fill=(25, 25, 112))
        if lfe:
            draw.point([3, 1], fill=(25, 25, 112))
        if output_l:
            draw.point([6, 0], fill=(25, 25, 112))
        if output_c:
            draw.point([7, 0], fill=(25, 25, 112))
        if output_r:
            draw.point([8, 0], fill=(25, 25, 112))
        if output_lb:
            draw.point([6, 1], fill=(25, 25, 112))
        if output_rb:
            draw.point([8, 1], fill=(25, 25, 112))
        if output_sub:
            draw.point([9, 1], fill=(25, 25, 112))

        self.matrix.SetImage(image.im.id, column, row)
