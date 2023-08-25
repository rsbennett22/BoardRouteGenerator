import numpy as np
from PIL import Image
import math

# Load image and ensure RGB - just in case palettised
im=Image.open("img/stokt_board.png").convert("RGB")

# Make numpy array from image
npimage=np.array(im)

# Describe what a single red pixel looks like
red=np.array([255,0,0],dtype=np.uint8)

# Find [x,y] coordinates of all red pixels
reds=np.where(np.all((npimage==red),axis=-1))

print(reds[0])