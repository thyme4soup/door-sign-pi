#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import sys
from PIL import Image, ImageFont
import inkyphat

icons = {}
masks = {}
# Load our icon files and generate masks
for icon in glob.glob("resources/icon-*.png"):
    icon_name = icon.split("icon-")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image
    masks[icon_name] = inkyphat.create_mask(icon_image)

# Load the built-in FredokaOne font
font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 20)

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
        inkyphat.clear()
        inkyphat.set_border(inkyphat.BLACK)

        # Load our backdrop image
        # inkyphat.set_image("resources/backdrop.png")

        # Let's draw some lines!
        # And now some text
        status = statuses[status_id]

        w, h = inkyphat._draw.multiline_textsize(status, font)
        x = (inkyphat.WIDTH / 2) - (w / 2)
        y = (inkyphat.HEIGHT / 2) - (h / 2)
        inkyphat._draw.multiline_text((x, y), status, inkyphat.BLACK, font)

        self.display()

    def display(self):
        inkyphat.show()


if __name__ == "__main__":

    display = DisplayPiHat()

    display.update(list(statuses.keys())[0])
