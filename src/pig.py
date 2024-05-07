from constants import *
import tkinter as tk
from tkinter import ttk, Label, messagebox
from PIL import ImageTk, Image, ImageOps, ImageFilter
from utils import select_filename
from collections import namedtuple

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
        self._apply_simple_image_operation(ImageOps.grayscale, 'greyscale')

    def apply_auto_contrast(self):
        self._apply_simple_image_operation(ImageOps.autocontrast, 'auto contrast')

    def flip_image(self):
        self._apply_simple_image_operation(ImageOps.flip, 'flip')

    def mirror_image(self):
        self._apply_simple_image_operation(ImageOps.mirror, 'mirror')

    def invert_image(self):
        self._apply_simple_image_operation(ImageOps.invert, 'invert')

    def posterize_image(self):
        args=1
        self._apply_simple_image_operation(ImageOps.posterize, 'posterize', args=args)

    def solarize_image(self):
        args = 128
        self._apply_simple_image_operation(ImageOps.solarize, 'solarize', args=args)

    def find_edges_in_image(self):
        # find currently selected tab
        selected_tab_view = self.editor.get_current_tab_view()
        selected_tab_image = selected_tab_view.image
        # apply edge finding function
        image_with_edges = selected_tab_image.filter(ImageFilter.FIND_EDGES)
        text_label = 'edges' + str(self.tab_counter)
        tab_view = TabView(self.editor.tabbed_view, image=image_with_edges, text_label=text_label)
        self.tab_views.append(tab_view)
        self.tab_counter = self.tab_counter + 1

    def _apply_simple_image_operation(self, image_op=None, type_of_op='', args=None):
        # find currently selected tab
        selected_tab_view = self.editor.get_current_tab_view()
        selected_tab_image = selected_tab_view.image
        # applying image operation
        if args is None:
            new_image = image_op(selected_tab_image)
        else:
            new_image = image_op(selected_tab_image, args)
        # Display greyscale image in a new tab
        text_label = type_of_op + str(self.tab_counter)
        tab_view = TabView(self.editor.tabbed_view, image=new_image, text_label=text_label)
        self.tab_views.append(tab_view)
        self.tab_counter = self.tab_counter + 1


    def exit_app(self):
        self.root.quit()


class PIGMenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_file_menu()
        self.create_image_menu()
        self.create_edit_menu()

    def create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='Load Image', command=self.controller.load_image)
        file_menu.add_command(label='Exit', command=self.controller.exit_app)
        self.add_cascade(label='File', menu=file_menu)

    def create_image_menu(self):
        image_menu = tk.Menu(self, tearoff=0)
        image_menu.add_command(label='Greyscale Image', command=self.controller.make_greyscale_image)
        image_menu.add_command(label='Auto Contrast', command=self.controller.apply_auto_contrast)
        image_menu.add_command(label='Find edges', command=self.controller.find_edges_in_image)
        self.add_cascade(label='Image', menu=image_menu)

    def create_edit_menu(self):
        edit_menu = tk.Menu(self, tearoff=0)
        edit_menu.add_command(label='Flip Image', command=self.controller.flip_image)
        edit_menu.add_command(label='Mirror Image', command=self.controller.mirror_image)
        edit_menu.add_command(label='Invert Image', command=self.controller.invert_image)
        edit_menu.add_separator()
        edit_menu.add_command(label='Posterize Image', command=self.controller.posterize_image)
        edit_menu.add_command(label='Solarize Image', command=self.controller.solarize_image)
        self.add_cascade(label='Edit', menu=edit_menu)


class PIGEditor:
    """ Main Frame responsible for the
        layout of the UI."""

    def __init__(self):
        self.root = tk.Tk()

        # Set the title of the window
        self.root.title(TITLE)

        # Set the tabbed display
        self.tabbed_view = ttk.Notebook(self.root, width=800, height=600)
        self.tabbed_view.pack(expand=True)

        # Set up the controller
        self.controller = PIGEditorController(self, self.root)

        # Set up menus
        self.menubar = PIGMenuBar(self.root, self.controller)
        self.root.config(menu=self.menubar)

    def get_current_tab_view(self):
        # This code gets the currently selected tab
        selected_tab_id = self.tabbed_view.select()
        label = self.tabbed_view.nametowidget(selected_tab_id)
        return label

    def mainloop(self):
        """Delegate method that passes responsibility onto the root"""
        self.root.mainloop()
