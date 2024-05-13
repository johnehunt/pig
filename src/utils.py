# To get the dialog box to open when required
from tkinter import filedialog, colorchooser
from PIL import Image, ImageOps
import numpy as np
from constants import IMAGE_FILE_TYPES


def select_open_filename():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title='Open Image', filetypes=IMAGE_FILE_TYPES)
    return filename


def select_save_filename():
    filename = filedialog.asksaveasfilename(title='Save Image', filetypes=IMAGE_FILE_TYPES)
    return filename


def choose_color_rgb(prompt):
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title=prompt)
    return color_code[0]

def tint_red(image):
    return get_image_for_channel(image, 0)

def tint_greed(image):
    return get_image_for_channel(image, 1)

def tint_blue(image):
    return get_image_for_channel(image, 2)

def get_image_for_channel(img, n):
    """Isolate the nth channel from the image.

       n = 0: red, 1: green, 2: blue
    """
    a = np.array(img)
    a[:,:,(n!=0, n!=1, n!=2)] *= 0
    return Image.fromarray(a)