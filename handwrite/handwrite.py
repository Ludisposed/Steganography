# -*- coding: utf-8 -*-
#!/usr/bin/env python
import numpy as np
from PIL import Image, ImageDraw, ImageFont

img = Image.open("wtest.png")
img.load()
#print img.getbands()
r, g, b, a = img.split()

# draw = ImageDraw.Draw(b)
# fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 400)
# draw.text((10,10), "Hello", font=fnt, fill="#ffffff")
draw = ImageDraw.Draw(r)
fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
draw.text((10,10), "Hello", font=fnt, fill="#eeeeee")

pic=Image.merge('RGBA',(r,g,b,a))
pic.save("test1.png")