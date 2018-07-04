# -*- coding: utf-8 -*-
#!/usr/bin/env python
import numpy as np
from PIL import Image, ImageDraw, ImageFont

'''
TODO: 
1. Detect best(darkest) place to write
2. can be write in different band, so detect the best band(to write per letter)
'''


def write_message(content, font_path,image_file, output_path):
    image = Image.open(image_file)
    image.load()
    bands = image.split()
    draw = ImageDraw.Draw(bands[0])
    font = ImageFont.truetype(font_path, 20)
    draw.text((10,10), content, font=font, fill="#ffffff")
    picture = Image.merge('RGBA',bands)
    picture.save(output_path)

if __name__ == "__main__":
    write_message("Hello", "/Library/Fonts/AmericanTypewriter.ttc", "test.png", "output_path.png")
