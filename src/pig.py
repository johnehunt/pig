from constants import *
import tkinter as tk

class PIGView(tk.Canvas):
    def __init__(self, parent,
                 width=WIDTH,
                 height=HEIGHT,
                 bg=BACKGROUND_COLOUR):
        super().__init__(parent, width=width, height=height, bg=bg)
        self.pack()

class PIGController:

    def __init__(self, root):
        self.root = root
        self.view = None

    def exit_app(self):
        self.root.quit()

class PIGMenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_file_menu()

    def create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
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

        # Setup drawing view
        self.drawing_view = PIGView(self.root)
        self.controller.view = self.drawing_view

        self.root.eval('tk::PlaceWindow . center')

    def mainloop(self):
        """Delegate method that passes responsibility onto the root"""
        self.root.mainloop()

