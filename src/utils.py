# To get the dialog box to open when required
from tkinter import filedialog
from constants import IMAGE_FILE_TYPES

def select_filename():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title='Open Image', filetypes=IMAGE_FILE_TYPES)
    return filename
