# To get the dialog box to open when required
from tkinter import filedialog, colorchooser
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
