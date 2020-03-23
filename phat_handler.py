#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import sys
from PIL import Image, ImageFont
import inkyphat
import textwrap

icons = {}
masks = {}
# Load our icon files and generate masks
for icon in glob.glob("resources/icon-*.png"):
    icon_name = icon.split("icon-")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image
    masks[icon_name] = inkyphat.create_mask(icon_image)

# Load the built-in FredokaOne font
font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 32)

statuses = {
    "on-a-call" : "On a call!\nCome back later",
    "do-not-disturb" : "Busy!\nCome back later",
    "busy" : "Busy!\nKnock first",
    "free" : "Welcome!\n(knock first)"
}

class DisplayPiHat():
    def __init__(self):
        pass

    def update(self, status_id):
        try:
            inkyphat.set_colour("Black")
        except ValueError:
            print('Invalid colour "{}" for V{}\n'.format(self.color, inkyphat.get_version()))
            if inkyphat.get_version() == 2:
                sys.exit(1)
            print('Defaulting to "red"')

        inkyphat.set_border(inkyphat.BLACK)

        # Load our backdrop image
        inkyphat.set_image("resources/backdrop.png")

        # Let's draw some lines!
        #inkyphat.line((69, 36, 69, 81)) # Vertical line
        #inkyphat.line((31, 35, 184, 35)) # Horizontal top line
        #inkyphat.line((69, 58, 174, 58)) # Horizontal middle line

        # And now some text
        status = statuses[status_id]

        inkyphat.text((30, 25), status, inkyphat.WHITE, font=font)

        txt = textwrap.fill(status, 16)
        w, h = inkyphat._draw.multiline_textsize(txt, font)
        x = (inkyphat.WIDTH / 2) - (w / 2)
        y = (inkyphat.HEIGHT / 2) - (h / 2)
        inkyphat._draw.multiline_text((x, y), txt, inkyphat.BLACK, font)

        self.display()

    def display(self):
        inkyphat.show()


if __name__ == "__main__":

    display = DisplayPiHat()

    display.update(list(statuses.keys())[0])
