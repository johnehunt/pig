from constants import *
import tkinter as tk
from tkinter import ttk, Label, messagebox
from PIL import ImageTk, Image, ImageOps
from utils import select_filename


class TabLabel(Label):
    def __init__(self, parent, photo_image=None, image=None, filename=None):
        super().__init__(parent, image=photo_image)
        self.image = image
        self.filename = filename



class TabView:
    def __init__(self, tabbed_view, filename=None, image=None, text_label=None):
        self.tabbed_view = tabbed_view
        if image is None:
            self.image = Image.open(filename)
        else:
            self.image = image
        self.photo_img = ImageTk.PhotoImage(self.image)
        # Add image to a tab
        self.label = TabLabel(self.tabbed_view,
                              photo_image=self.photo_img,
                              image=self.image,
                              filename=filename)
        self.label.place(x=10, y=10)
        if text_label is None:
            self.tabbed_view.add(self.label, text=filename)
        else:
            self.tabbed_view.add(self.label, text=text_label)



class PIGMenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_file_menu()
        self.create_image_menu()

    def create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='Load Image', command=self.controller.load_image)
        file_menu.add_command(label='Exit', command=self.controller.exit_app)
        self.add_cascade(label='File', menu=file_menu)

    def create_image_menu(self):
        image_menu = tk.Menu(self, tearoff=0)
        image_menu.add_command(label='Greyscale Image', command=self.controller.make_greyscale_image)
        self.add_cascade(label='Image', menu=image_menu)


class PIGEditorController:

    def __init__(self, editor, root):
        self.root = root
        self.editor = editor
        self.tab_views = []
        self.tab_counter = 1

    def load_image(self):
        filename = select_filename()
        if filename != '':
            tab_view = TabView(self.editor.tabbed_view, filename=filename)
            self.tab_views.append(tab_view)
        else:
            messagebox.showerror("Error", "No file selected")

    def make_greyscale_image(self):
        # find currently selected tab
        selected_tab_view = self.editor.get_current_tab_view()
        selected_tab_image = selected_tab_view.image
        # applying grayscale method
        grey_scale_image = ImageOps.grayscale(selected_tab_image)
        text_label = 'greyscale' + str(self.tab_counter)
        tab_view = TabView(self.editor.tabbed_view, image=grey_scale_image, text_label=text_label)
        self.tab_views.append(tab_view)
        self.tab_counter = self.tab_counter + 1


    def exit_app(self):
        self.root.quit()


class PIGEditor:
    """ Main Frame responsible for the
        layout of the UI."""

    def __init__(self):
        self.root = tk.Tk()

        # Set the title of the window
        self.root.title(TITLE)

        # Set the tabbed display
        self.tabbed_view = ttk.Notebook(self.root,width=800, height=600)
        self.tabbed_view.pack(expand=True)

        # Set up the controller
        self.controller = PIGEditorController(self, self.root)

        # Set up menus
        self.menubar = PIGMenuBar(self.root, self.controller)
        self.root.config(menu=self.menubar)

    def get_current_tab_view(self):
        # This code gets the currently selected tab
        selected_tab_id = self.tabbed_view.select()
        print(selected_tab_id)
        # tab = self.tabbed_view.tab(selected_tab_id, "text")
        # print(tab)
        # idx = self.tabbed_view.index(selected_tab_id)
        # print(idx)
        # current = self.tabbed_view.index("current")
        # print(current)
        # # tab = self.tabbed_view[str(current)]
        # # print(tab)
        label = self.tabbed_view.nametowidget(selected_tab_id)
        print(label)
        return label

    def mainloop(self):
        """Delegate method that passes responsibility onto the root"""
        self.root.mainloop()
