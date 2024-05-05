from constants import *
import tkinter as tk
from PIL import ImageTk, Image
# To get the dialog box to open when required
from tkinter import filedialog

class PIGView(tk.Canvas):
    def __init__(self, parent, controller,
                 width=WIDTH,
                 height=HEIGHT,
                 bg=BACKGROUND_COLOUR):
        super().__init__(parent, width=width, height=height, bg=bg)
        self.controller = controller
        self.pack()

class PIGController:

    def __init__(self, root):
        self.root = root
        self.image = None
        self.photo_img = None
        self.view = None

    def select_filename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title='Open')
        return filename

    def load_image(self):
        filename = self.select_filename()
        self.image = Image.open(filename)
        self.photo_img = ImageTk.PhotoImage(self.image)
        # Setup drawing view
        self.view = PIGView(self.root,
                            controller=self,
                            width=self.photo_img.width(),
                            height=self.photo_img.height())
        self.view.create_image(20, 20, anchor=tk.NW, image=self.photo_img)
        self.root.eval('tk::PlaceWindow . center')

    def exit_app(self):
        self.root.quit()

class PIGMenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_file_menu()

    def create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='Load Image', command=self.controller.load_image)
        file_menu.add_command(label='Exit', command=self.controller.exit_app)
        self.add_cascade(label='File', menu=file_menu)


class PIGEditor:
    """ Main Frame responsible for the
        layout of the UI."""

    def __init__(self):
        self.root = tk.Tk()

        # Set the title of the window
        self.root.title(TITLE)

        # Set up the controller
        self.controller = PIGController(self.root)

        # Set up menus
        self.menubar = PIGMenuBar(self.root, self.controller)
        self.root.config(menu=self.menubar)


    def mainloop(self):
        """Delegate method that passes responsibility onto the root"""
        self.root.mainloop()

