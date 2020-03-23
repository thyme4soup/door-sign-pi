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
font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 36)

statuses = {
    "on-a-call" : "On a call! Come back later",
    "do-not-disturb" : "Busy! Come back later",
    "busy" : "Busy! Knock first",
    "free" : "Welcome! (knock first)"
}

class DisplayPiHat():
    def __init__(self):
        pass

    def update(self, status_id):
        inkyphat.set_border(inkyphat.BLACK)

        # Load our backdrop image
        inkyphat.set_image("resources/backdrop.png")

        # Let's draw some lines!
        #inkyphat.line((69, 36, 69, 81)) # Vertical line
        #inkyphat.line((31, 35, 184, 35)) # Horizontal top line
        #inkyphat.line((69, 58, 174, 58)) # Horizontal middle line

        # And now some text
        inkyphat.text((30, 25), statuses[status_id], inkyphat.WHITE, font=font)

        self.display()

    def display(self):
        inkyphat.show()


if __name__ == "__main__":

    display = DisplayPiHat()

    display.update(list(statuses.keys())[0])
