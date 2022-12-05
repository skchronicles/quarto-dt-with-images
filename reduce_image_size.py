#!/usr/bin/env python3

from PIL import Image
import sys

# https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil
file = sys.argv[1]
foo = Image.open(file) 
width, height = foo.size
width = int(width * 0.15)
height = int(height * 0.15)

# Downsize the image with an 
# ANTIALIAS filter, gives the 
# highest quality
foo = foo.resize((width,height),Image.Resampling.LANCZOS)

# Create a new optimized and 
# scaled-down image
foo.save("{}.scaled.png".format(file.replace('.png', '')), optimize=True, quality=80)
