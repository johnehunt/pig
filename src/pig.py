from constants import *
import tkinter as tk
from tkinter import ttk, Label, messagebox, simpledialog
from PIL import ImageTk, Image, ImageOps, ImageFilter, ImageEnhance
from utils import select_open_filename, select_save_filename, choose_color_rgb


class TabLabel(Label):
    def __init__(self, parent, photo_image=None, image=None, filename=None):
        super().__init__(parent, image=photo_image)
        self.image = image
        self.photo_image = photo_image
        self.filename = filename


class PIGEditorController:

    def __init__(self, editor, root):
        self.root = root
        self.editor = editor
        self.tab_views = []
        self.tab_counter = 1

    def get_current_tab_view(self):
        # This code gets the currently selected tab
        selected_tab_id = self.editor.tabbed_view.select()
        label = self.editor.tabbed_view.nametowidget(selected_tab_id)
        return label

    def get_tab_view(self, tabbed_view, filename=None, image=None):
        if image is None:
            image = Image.open(filename)

        photo_img = ImageTk.PhotoImage(image)
        # Add image to a tab
        label = TabLabel(tabbed_view,
                         image=image,
                         photo_image=photo_img,
                         filename=filename)
        label.place(x=10, y=10)
        return label

    def load_image(self):
        filename = select_open_filename()
        if filename != '':
            tab_view = self.get_tab_view(self.editor.tabbed_view, filename=filename)
            self.editor.tabbed_view.add(tab_view, text=filename)
            self.editor.tabbed_view.select(tab_view)
            self.tab_views.append(tab_view)
        else:
            messagebox.showerror("Error", "No file selected")

    def save_image(self):
        filename = select_save_filename()
        if filename != '':
            image = self._get_selected_image()
            with open(filename, 'w') as file:
                image.save(file)
        else:
            messagebox.showerror("Error", "No save file selected")

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

    def colorize_image(self):
        selected_tab_view = self.get_current_tab_view()
        selected_tab_image = selected_tab_view.image
        if selected_tab_image.mode == "L":
            replacement_black_colour = choose_color_rgb('Replace black with')
            replace_white_colour = choose_color_rgb('Replace white with')
            args = (replacement_black_colour, replace_white_colour)
            self._apply_simple_image_operation(ImageOps.colorize, 'colorize', args)
        else:
            messagebox.showerror("Error", "Colorize can only be applied to greyscale images")

    def posterize_image(self):
        args = 1
        answer = simpledialog.askinteger(title="Bits Channel Input",
                                         prompt="The number of bits to keep for each channel (1-8).",
                                         initialvalue=1,
                                         parent=self.root,
                                         minvalue=1, maxvalue=8)
        if answer is not None:
            args = answer
        self._apply_simple_image_operation(ImageOps.posterize, 'posterize', args=args)

    def solarize_image(self):
        args = 128
        answer = simpledialog.askinteger(title="Threshold Input",
                                         prompt="Threshold value for solarize? \n(All pixels above this grayscale level are inverted)",
                                         initialvalue=128,
                                         parent=self.root,
                                         minvalue=1, maxvalue=256)
        if answer is not None:
            args = answer
        self._apply_simple_image_operation(ImageOps.solarize, 'solarize', args=args)

    def quantize_image(self):
        args = 16
        answer = simpledialog.askinteger(title="Quantize Input",
                                         prompt="Value for quantization",
                                         initialvalue=16,
                                         parent=self.root,
                                         minvalue=1, maxvalue=32)
        if answer is not None:
            args = answer
        selected_tab_image = self._get_selected_image()
        self._apply_image_method(selected_tab_image.quantize, 'quantize', args)

    def enhance_color(self):
        args = 3.0
        answer = simpledialog.askfloat(title="Enhance Color",
                                         prompt="Value for enhance",
                                         initialvalue=3.0,
                                         parent=self.root,
                                         minvalue=1.0, maxvalue=9.0)
        if answer is not None:
            args = answer
        selected_tab_image = self._get_selected_image()
        enhanced_image = ImageEnhance.Color(selected_tab_image)
        self._apply_image_method(enhanced_image.enhance, 'enhance color', args)

    def enhance_contrast(self):
        args = 3.0
        answer = simpledialog.askfloat(title="Enhance Contrast",
                                         prompt="Value for enhance",
                                         initialvalue=3.0,
                                         parent=self.root,
                                         minvalue=1.0, maxvalue=9.0)
        if answer is not None:
            args = answer
        selected_tab_image = self._get_selected_image()
        enhanced_image = ImageEnhance.Contrast(selected_tab_image)
        self._apply_image_method(enhanced_image.enhance, 'enhance contrast', args)

    def brighten_image(self):
        args = 3.0
        answer = simpledialog.askfloat(title="Brighten Image",
                                       prompt="Value to brighten",
                                       initialvalue=3.0,
                                       parent=self.root,
                                       minvalue=1.0, maxvalue=9.0)
        if answer is not None:
            args = answer
        selected_tab_image = self._get_selected_image()
        enhanced_image = ImageEnhance.Brightness(selected_tab_image)
        self._apply_image_method(enhanced_image.enhance, 'brighten image', args)

    def find_edges_in_image(self):
        self._apply_filter_method('edges', ImageFilter.FIND_EDGES)

    def blur_image(self):
        self._apply_filter_method('blur', ImageFilter.BLUR)

    def contour_image(self):
        self._apply_filter_method('contour', ImageFilter.CONTOUR)

    def smooth_image(self):
        self._apply_filter_method('smooth', ImageFilter.SMOOTH)

    def sharpen_image(self):
        self._apply_filter_method('sharpen', ImageFilter.SHARPEN)

    def emboss_image(self):
        self._apply_filter_method('emboss', filter_to_apply=ImageFilter.EMBOSS)

    def edge_enhance_image(self):
        self._apply_filter_method('edge enhance', filter_to_apply=ImageFilter.EDGE_ENHANCE)

    def detail_image(self):
        self._apply_filter_method('detail', filter_to_apply=ImageFilter.DETAIL)

    def _get_selected_image(self):
        # find currently selected tab
        selected_tab_view = self.get_current_tab_view()
        selected_tab_image = selected_tab_view.image
        return selected_tab_image

    def _apply_filter_method(self, label, filter_to_apply):
        # get the image
        selected_tab_image = self._get_selected_image()
        # Select the operation
        image_method = selected_tab_image.filter
        # Apply the filter
        self._apply_image_method(image_method, label, filter=filter_to_apply)

    def _apply_image_method(self, image_method, type_of_method='filter', filter=None):
        image_with_edges = image_method(filter)
        text_label = type_of_method + str(self.tab_counter)
        tab_view = self.get_tab_view(self.editor.tabbed_view, image=image_with_edges)
        self.editor.tabbed_view.add(tab_view, text=text_label)
        self.editor.tabbed_view.select(tab_view)
        self.tab_views.append(tab_view)
        self.tab_counter = self.tab_counter + 1

    def _apply_simple_image_operation(self, image_op=None, type_of_op='', args=None):
        # find currently selected tab
        selected_tab_image = self._get_selected_image()
        # applying image operation
        if args is None:
            new_image = image_op(selected_tab_image)
        elif isinstance(args, list) or isinstance(args, tuple):
            if len(args) == 1:
                new_image = image_op(selected_tab_image, args[0])
            elif len(args) == 2:
                new_image = image_op(selected_tab_image, args[0], args[1])
            elif len(args) == 3:
                new_image = image_op(selected_tab_image, args[0], args[1], args[3])
        else:
            new_image = image_op(selected_tab_image, args)
        # Display greyscale image in a new tab
        text_label = type_of_op + str(self.tab_counter)
        # Create tab for tabbed view
        tab_view = self.get_tab_view(self.editor.tabbed_view, image=new_image)

        self.editor.tabbed_view.add(tab_view, text=text_label)
        self.editor.tabbed_view.select(tab_view)
        self.tab_views.append(tab_view)
        self.tab_counter = self.tab_counter + 1

    def on_tab_click(self, event):
        response = messagebox.askquestion('Delete Tab', 'Do you want to delete the tab?')
        if response == 'yes':
            nb = self.editor.tabbed_view
            clicked_tab = nb.tk.call(nb._w, "identify", "tab", event.x, event.y)
            print('clicked tab:', clicked_tab)
            nb.forget(clicked_tab)
            del self.tab_views[clicked_tab]

    def exit_app(self):
        self.root.quit()


class PIGMenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_file_menu()
        self.create_image_menu()

    def create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='Load Image', command=self.controller.load_image)
        file_menu.add_command(label='Save Image', command=self.controller.save_image)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.controller.exit_app)
        self.add_cascade(label='File', menu=file_menu)

    def create_image_menu(self):
        image_menu = tk.Menu(self, tearoff=0)
        image_menu.add_command(label='Greyscale Image', command=self.controller.make_greyscale_image)
        image_menu.add_separator()
        image_menu.add_command(label='Flip Image', command=self.controller.flip_image)
        image_menu.add_command(label='Mirror Image', command=self.controller.mirror_image)
        image_menu.add_command(label='Invert Image', command=self.controller.invert_image)
        image_menu.add_separator()
        image_menu.add_command(label='Enhance Color', command=self.controller.enhance_color)
        image_menu.add_command(label='Enhance Contrast', command=self.controller.enhance_contrast)
        image_menu.add_command(label='Auto Contrast', command=self.controller.apply_auto_contrast)
        image_menu.add_command(label='Brighten', command=self.controller.brighten_image)
        image_menu.add_command(label='Blur', command=self.controller.blur_image)
        image_menu.add_command(label='Contour', command=self.controller.contour_image)
        image_menu.add_command(label='Detail', command=self.controller.detail_image)
        image_menu.add_command(label='Emboss', command=self.controller.emboss_image)
        image_menu.add_command(label='Smooth', command=self.controller.smooth_image)
        image_menu.add_command(label='Sharpen', command=self.controller.sharpen_image)
        image_menu.add_separator()
        image_menu.add_command(label='Find Edges', command=self.controller.find_edges_in_image)
        image_menu.add_command(label='Edge Enhance', command=self.controller.edge_enhance_image)
        image_menu.add_separator()
        image_menu.add_command(label='Colorize Image', command=self.controller.colorize_image)
        image_menu.add_command(label='Posterize Image', command=self.controller.posterize_image)
        image_menu.add_command(label='Solarize Image', command=self.controller.solarize_image)
        image_menu.add_command(label='Quantize Image', command=self.controller.quantize_image)
        self.add_cascade(label='Image', menu=image_menu)


class PIGEditor:
    """ Main Frame responsible for the
        layout of the UI."""

    def __init__(self):
        self.root = tk.Tk()

        # Set the title of the window
        self.root.title(TITLE)

        # Set the tabbed display
        self.tabbed_view = ttk.Notebook(self.root, width=WIDTH, height=HEIGHT)
        self.tabbed_view.pack(expand=True)
        self.tabbed_view.enable_traversal()

        # Set up the controller
        self.controller = PIGEditorController(self, self.root)

        # Set up menu handling on tabs
        # bind function to notebook
        self.tabbed_view.bind('<Button-3>', self.controller.on_tab_click)
        self.tabbed_view.bind('<Button-2>', self.controller.on_tab_click)  # for mac users

        # Set up menus
        self.menubar = PIGMenuBar(self.root, self.controller)
        self.root.config(menu=self.menubar)

    def mainloop(self):
        """Delegate method that passes responsibility onto the root"""
        self.root.mainloop()
