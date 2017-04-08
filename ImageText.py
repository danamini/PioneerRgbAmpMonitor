#!/usr/bin/env python
import Image
import ImageDraw
import ImageFont

class ImageText(object):
    """ Simple wrapper to PIL library, handling text images """

    def __init__(self, font, text, colour):
        self.image = None
        self.font = font
        self.colour = colour
        self.size = None
        self.set_text(text)

    def set_text(self, text):
        """ Set the text size and image """
        self.text = text
        self.set_size()
        self.set_image()

    def set_size(self):
        """ Set text size """
        self.size = self.font.getsize(self.text)
        return self.size

    def set_image(self):
        """ Create an image using the defined text """
        self.image = Image.new("RGB", (self.size[0], self.size[1]))
        draw = ImageDraw.Draw(self.image)
        draw.text((0, 0), self.text, font=self.font, fill=self.colour)
        return self.image
