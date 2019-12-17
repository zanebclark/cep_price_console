import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import logging
import re
from collections import OrderedDict


even_background = "honeydew2"
odd_background = "honeydew3"
heading1 = None
heading2 = None
heading3 = None
notes = None
dflt = None


# @debug(lvl=logging.NOTSET, prefix='')
def init_style(tk_obj):
    global even_background
    global odd_background
    global heading1
    global heading2
    global heading3
    global notes
    global dflt

    # Lots of theme style options
    # style = 'winnative'
    # style = 'clam'
    # style = 'alt'
    # style = 'classic'
    # style = 'vista'
    style = 'xpnative'
    ttk.Style().theme_use(style)

    default = font.Font(root=tk_obj, name="TkTextFont", exists=True)
    heading1 = default.copy()
    heading1.config(family='Verdana', size=20, weight="bold")
    heading2 = default.copy()
    heading2.config(family='Verdana', size=16, weight="normal")
    heading3 = default.copy()
    heading3.config(family='Verdana', size=13, weight="normal")
    notes = default.copy()
    notes.config(family='Verdana Italic', size=10, weight="normal")
    dflt = default.copy()
    dflt.config(family='Verdana', size=11, weight="normal")

    style = ttk.Style(tk_obj)
    style.configure("heading1.TLabel", font=heading1)
    style.configure("heading2.TLabel", font=heading2)
    style.configure("heading3.TLabel", font=heading3)
    style.configure("notes.TLabel", font=notes)
    style.configure("dflt.TLabel", font=dflt)

    style = ttk.Style(tk_obj)
    style.configure("even.heading1.TLabel", background=even_background)
    style.configure("even.heading2.TLabel", background=even_background)
    style.configure("even.heading3.TLabel", background=even_background)
    style.configure("even.notes.TLabel", background=even_background)
    style.configure("even.dflt.TLabel", background=even_background)

    style.configure("odd.heading1.TLabel", background=odd_background)
    style.configure("odd.heading2.TLabel", background=odd_background)
    style.configure("odd.heading3.TLabel", background=odd_background)
    style.configure("odd.notes.TLabel", background=odd_background)
    style.configure("odd.dflt.TLabel", background=odd_background)

    style.configure("group.TFrame", borderwidth=4)
    style.configure("even.group.TFrame", background=even_background)  # relief=tk.SUNKEN,
    style.configure("odd.group.TFrame", background=odd_background)  # relief=tk.SUNKEN,

    style.configure("group.TLabelframe", borderwidth=4)
    style.configure("even.group.TLabelframe", background=even_background)  # relief=tk.SUNKEN,
    style.configure("odd.group.TLabelframe", background=odd_background)  # relief=tk.SUNKEN,

    style.configure("heading1.TRadiobutton", font=heading1)
    style.configure("heading2.TRadiobutton", font=heading2)
    style.configure("heading3.TRadiobutton", font=heading3)
    style.configure("notes.TRadiobutton", font=notes)
    style.configure("dflt.TRadiobutton", font=dflt)

    style.configure("even.heading1.TRadiobutton", background=even_background)
    style.configure("even.heading2.TRadiobutton", background=even_background)
    style.configure("even.heading3.TRadiobutton", background=even_background)
    style.configure("even.notes.TRadiobutton", background=even_background)
    style.configure("even.dflt.TRadiobutton", background=even_background)

    style.configure("odd.heading1.TRadiobutton", background=odd_background)
    style.configure("odd.heading2.TRadiobutton", background=odd_background)
    style.configure("odd.heading3.TRadiobutton", background=odd_background)
    style.configure("odd.notes.TRadiobutton", background=odd_background)
    style.configure("odd.dflt.TRadiobutton", background=odd_background)

    style.configure("heading1.TCheckbutton", font=heading1)
    style.configure("heading2.TCheckbutton", font=heading2)
    style.configure("heading3.TCheckbutton", font=heading3)
    style.configure("notes.TCheckbutton", font=notes)
    style.configure("dflt.TCheckbutton", font=dflt)

    style.configure("even.heading1.TCheckbutton", background=even_background)
    style.configure("even.heading2.TCheckbutton", background=even_background)
    style.configure("even.heading3.TCheckbutton", background=even_background)
    style.configure("even.notes.TCheckbutton", background=even_background)
    style.configure("even.dflt.TCheckbutton", background=even_background)

    style.configure("odd.heading1.TCheckbutton", background=odd_background)
    style.configure("odd.heading2.TCheckbutton", background=odd_background)
    style.configure("odd.heading3.TCheckbutton", background=odd_background)
    style.configure("odd.notes.TCheckbutton", background=odd_background)
    style.configure("odd.dflt.TCheckbutton", background=odd_background)

    # style.map("bad.TButton",
    #           # anchor,
    #           background=[('active', '!disabled', 'CadetBlue1'), ('disabled', '!disabled', 'DarkOliveGreen1'),
    #                       ('pressed', '!disabled', 'firebrick1'), ('readonly', '!disabled', 'turquoise')],
    #           bordercolor=[('active', '!disabled', 'CadetBlue2'), ('disabled', '!disabled', 'DarkOliveGreen2'),
    #                        ('pressed', '!disabled', 'firebrick2'), ('readonly', '!disabled', 'turquoise1')],
    #           darkcolor=[('active', '!disabled', 'CadetBlue3'), ('disabled', '!disabled', 'DarkOliveGreen3'),
    #                      ('pressed', '!disabled', 'firebrick3'), ('readonly', '!disabled', 'turquoise2')],
    #           foreground=[('active', '!disabled', 'CadetBlue4'), ('disabled', '!disabled', 'DarkOliveGreen4'),
    #                       ('pressed', '!disabled', 'firebrick4'), ('readonly', '!disabled', 'turquoise3')],
    #           # font,
    #           highlightcolor=[('active', 'DeepSkyBlue1'), ('disabled', 'PaleGreen1'), ('pressed', 'red'),
    #                           ('readonly', 'turquoise4')],
    #           # highlightthickness,
    #           lightcolor=[('active', 'DeepSkyBlue2'), ('disabled', 'PaleGreen1'), ('pressed', 'red2'),
    #                       ('readonly', 'cyan')],
    #           # padding,
    #           # relief,
    #           # shiftrelief
    #           )
    # style.configure('bad.TButton', background='indian red', bordercolor='indian red', darkcolor='indian red',
    #                 foreground='indian red', highlightcolor='indian red', lightcolor='indian red')
    style.configure('bad.TButton', background='indian red')
    style.configure('bad.TButton', foreground='indian red')

    style.configure("bad.TEntry", font=heading2)
    style.configure('bad.TEntry', background='indian red')
    style.configure('bad.TEntry', foreground='indian red')
    style.configure('bad.TEntry', highlightbackground='indian red')
    style.configure('bad.TEntry', highlightthickness=12)

    # -anchor anchor
    # -background color
    # -bordercolor color
    # -darkcolor color
    # -foreground color
    # -font font
    # -highlightcolor color
    # -highlightthickness amount
    # -lightcolor color
    # -padding padding
    # -relief relief
    # -shiftrelief amount

    style.map('Bad.TCombobox', background=[('readonly', 'indian red')])
    style.map('Bad.TCombobox', fieldbackground=[('readonly', 'indian red')])
    style.map('Bad.TCombobox', selectbackground=[('readonly', 'indian red')])
    style.map('Bad.TCombobox', selectforeground=[('readonly', 'black')])

    style.map('bad.dflt.TCheckbutton',
              background=[('!selected', 'red')])

    # noinspection SpellCheckingInspection
    tk_obj.abdc = heading1
    # noinspection SpellCheckingInspection
    tk_obj.efgh = heading2
    tk_obj.ee = heading3
    tk_obj.aa = notes
    tk_obj.bb = dflt
    # tk_obj.option_readfile('optionDB.txt')


class AutoScrollbar(ttk.Scrollbar):
    """A scrollbar that hides itself if it's not needed. only \
       works if you use the grid geometry manager."""

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    @staticmethod
    def pack(**kw):
        """pack"""
        raise tk.TclError("cannot use pack with this widget")

    @staticmethod
    def place(**kw):
        """place"""
        raise tk.TclError("cannot use place with this widget")


# @debug(lvl=logging.NOTSET, prefix='')
class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame \
    see http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame. \
    Use the 'interior' attribute to place widgets inside the scrollable frame.
    """

    # noinspection PyUnusedLocal
    def __init__(self, master, canvas_background=None, fill_height=False, height=None, width=None, shrink_height=False,
                 *args, **kw):
        # noinspection PyArgumentList
        super().__init__(master, *args, **kw)
        self.shrink_height = shrink_height
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = AutoScrollbar(self, orient=tk.VERTICAL)
        vscrollbar.grid(row=0, column=2, rowspan=1, sticky=tk.NS, pady=0)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, height=height, width=width,
                                yscrollcommand=vscrollbar.set,
                                background=canvas_background)
        self.canvas.grid(row=0, column=0, rowspan=1, sticky=tk.NSEW, pady=0)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

        # track changes to the canvas and frame width and sync them, also updating the scrollbar

        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        return

    # noinspection PyUnusedLocal
    def _configure_canvas(self, event):
        self.update_idletasks()
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        if not self.shrink_height:
            if self.interior.winfo_reqheight() <= self.canvas.winfo_height():
                self.canvas.itemconfigure(self.interior_id, height=self.canvas.winfo_height())
            else:
                self.canvas.itemconfigure(self.interior_id, height=self.interior.winfo_reqheight())

    # noinspection PyUnusedLocal
    def _configure_interior(self, event):
        self.update_idletasks()
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def fit_canvas(self):
        self.update_idletasks()
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())


# @debug(lvl=logging.NOTSET, prefix='')
def center_window(win_obj, width=None, height=None):
    center_coords = []
    win_obj.update()

    if width is None:
        if win_obj.winfo_reqwidth() < win_obj.winfo_screenwidth():
            width = win_obj.winfo_reqwidth()
        else:
            width = win_obj.winfo_screenwidth()

    if height is None:
        if win_obj.winfo_reqheight() < win_obj.winfo_screenheight():
            height = win_obj.winfo_reqheight()
        else:
            height = win_obj.winfo_screenheight()

    if win_obj.state() != "zoomed":
        window_dims = (width, height)

        # Use the logo to dimension the window and center accordingly.
        screen = (win_obj.winfo_screenwidth(), win_obj.winfo_screenheight())
        for i in range(0, 2):
            i = int(round((screen[i] / 2) - (window_dims[i] / 2)))
            center_coords.append(i)

        win_obj.geometry("{0}x{1}+{2}+{3}".format(window_dims[0],
                                                  window_dims[1],
                                                  center_coords[0],
                                                  center_coords[1]))


class Loading(tk.Toplevel):
    from cep_price_console.utils.log_utils import CustomAdapter, debug
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.root = self.master.root
        super().__init__(self.root, *args, **kwargs)


def parsegeometry(geometry):
    geometry = str(geometry).replace("+", "%")
    m = re.match("(\d+)x(\d+)%([-+]?\d+)%([-+]?\d+)", geometry)
    if not m:
        raise ValueError("failed to parse geometry string")
    return map(int, m.groups())


def get_style(parent_obj, attr_string):
    for thing in list(parent_obj.configure().get("style")):
        if thing.find(parent_obj.winfo_class()) != -1:
            return ttk.Style().lookup(thing, attr_string)


class StyledButton(tk.Button):
    background = ""
    activebackground = ""
    hoverbackground = ""
    relief = ""
    overrelief = ""
    default = ""

    def __init__(self, master, **kwargs):
        remove_list = ["background", "activebackground", "relief", "overrelief", "default"]
        for string in remove_list:
            if string in kwargs.keys():
                del kwargs[string]

        super().__init__(
            master,
            background=self.__class__.background,
            activebackground=self.__class__.activebackground,
            # foreground="",
            # activeforeground="",
            relief=self.__class__.relief,
            overrelief=self.__class__.overrelief,
            default=self.__class__.default,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # noinspection PyUnusedLocal
    def on_enter(self, event):
        self['background'] = self.__class__.hoverbackground

    # noinspection PyUnusedLocal
    def on_leave(self, event):
        self['background'] = self.__class__.background


class BadButton(StyledButton):
    background = "tomato3"
    activebackground = "gray"
    hoverbackground = "tomato"
    relief = tk.RAISED
    overrelief = tk.SUNKEN
    default = tk.ACTIVE


class GreyButton(StyledButton):
    background = "SlateGray1"
    activebackground = "gray99"
    hoverbackground = "SlateGray4"
    relief = tk.RAISED
    overrelief = tk.SUNKEN
    default = tk.ACTIVE


class OrderableListFrame(ttk.Frame):
    def __init__(self,
                 parent,
                 title,
                 value_dict=None,
                 allow_reorder=True,
                 allow_delete=True,
                 allow_reset=True):
        self.default_dict = OrderedDict()
        self.item_dict = OrderedDict()
        self.title = title
        self.parent = parent
        self.allow_reorder = allow_reorder
        self.allow_delete = allow_delete
        self.allow_reset = allow_reset
        super().__init__(self.parent,
                         relief=tk.RAISED,
                         padding=5,
                         style="even.group.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.header = ttk.Label(
            self,
            text=self.title,
            style="even.heading3.TLabel",
            wraplength=2
        )
        self.header.grid(row=0, column=0, sticky=tk.NW)

        if self.allow_reset:
            self.reset_btn = GreyButton(
                self,
                text="Reset Items",
                command=lambda: self.populate(value_dict=self.default_dict)
            )
            self.reset_btn.grid(row=0, column=1, sticky=tk.SE)
        else:
            self.reset_btn = None

        self.item_list_frame = VerticalScrolledFrame(
            self,
            relief=tk.SUNKEN,
            padding=5,
            style="odd.group.TFrame",
            canvas_background=odd_background,
            shrink_height=True
        )
        self.item_list_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.item_list_frame.interior.columnconfigure(0, weight=1)
        self.item_list_frame.interior.config(style="odd.group.TFrame")

        if value_dict is not None:
            self.populate(value_dict=value_dict)

        self.bind("<Configure>", self.on_resize, "+")

    def get_open_item(self, title):
        pass

    def add_item(self, key, item):
        item.grid_init(
            key=key,
            list_frame=self,
            parent=self.item_list_frame.interior
        )
        self.default_dict[key] = item
        self.item_dict[key] = item

    def current_index(self, list_item):
        key_list = [key for key in self.item_dict.keys()]
        print("Key List: {}".format(', '.join(key_list)))
        return key_list.index(list_item.key), key_list

    def move_down(self, list_item):
        current_index, key_list = self.current_index(list_item)
        if current_index == len(key_list) - 1:
            key_list.insert(0, key_list.pop(current_index))
        else:
            key_list.insert(current_index + 1, key_list.pop(current_index))
        self.grid_all(key_list=key_list)

    def move_up(self, list_item):
        current_index, key_list = self.current_index(list_item)
        if current_index == 0:
            key_list.insert(len(key_list), key_list.pop(current_index))
        else:
            key_list.insert(current_index - 1, key_list.pop(current_index))
        self.grid_all(key_list=key_list)

    def delete_item(self, list_item):
        list_item.grid_forget()
        current_index, key_list = self.current_index(list_item)
        key_list.pop(current_index)
        self.grid_all(key_list=key_list)

    def grid_all(self, key_list=None):
        if key_list is None:
            key_list = [key for key in self.item_dict.keys()]
        counter = 0
        new_dict = OrderedDict()
        for key in key_list:
            item = self.item_dict[key]
            new_dict[key] = item
            item.grid_forget()
            item.grid(row=counter, column=0, sticky=tk.NSEW, pady=2)
            counter += 1
        self.item_dict = new_dict

    # noinspection PyUnusedLocal
    def on_resize(self, event):
        self.header.configure(wraplength=self.winfo_width())

    def populate(self, value_dict):
        for item_obj in self.item_dict.values():
            item_obj.grid_forget()
        self.item_dict = OrderedDict()
        self.default_dict = OrderedDict()
        for key, item in value_dict.items():
            self.add_item(key=key, item=item)
        self.grid_all()

        # #TODO what if value items are None?
        # if self.item_list and self.item_dict:
        #     raise ValueError
        # elif self.item_list or value_list:
        #     for item_obj in self.item_list:
        #         item_obj.grid_forget()
        #     self.item_list = []
        #     self.default_list = []
        #     for item in value_list:
        #         self.add_item(key=None, item=item)
        # elif self.item_dict or value_dict:
        #     for item_obj in self.item_dict.values():
        #         item_obj.grid_forget()
        #     self.item_dict = OrderedDict()
        #     self.default_dict = OrderedDict()
        #     for key, item in value_dict.items():
        #         self.add_item(key=key, item=item)
        # else:
        #     raise ValueError
        # self.grid_all()


class OrderableListItem(ttk.Frame):
    # noinspection PyMissingConstructor
    def __init__(self,
                 title):
        self.key = None
        self.title = title
        self.list_frame = None
        self.parent = None
        self.title_label = None
        self.move_down_btn = None
        self.move_up_btn = None
        self.delete_item = None
        self.inner_frame = None

    def grid_init(self, key, list_frame, parent, **kwargs):
        self.key = key
        self.list_frame = list_frame
        self.parent = parent
        super().__init__(
            self.parent,
            style="even.group.TFrame",
            padding=5,
            relief=tk.RAISED,
            **kwargs
        )
        # self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.title_label = ttk.Label(self, width=20, text=self.title, style="even.dflt.TLabel", wraplength=10)
        self.title_label.grid(row=0, column=0, sticky=tk.NW)

        self.inner_frame = ttk.Frame(self, style="even.group.TFrame")
        self.inner_frame.grid(row=0, column=1, padx=3, sticky=tk.NE + tk.W)
        self.inner_frame.rowconfigure(0, weight=1)
        self.inner_frame.columnconfigure(0, weight=1)

        if self.list_frame.allow_reorder:
            self.move_down_btn = GreyButton(self, text=u"\u2193", command=self.move_down)
            self.move_down_btn.grid(row=0, column=3, padx=1, sticky=tk.NE)

            self.move_up_btn = GreyButton(self, text=u"\u2191", command=self.move_up)
            self.move_up_btn.grid(row=0, column=4, padx=1, sticky=tk.NE)

        if self.list_frame.allow_delete:
            self.delete_item = BadButton(self, text="X", command=self.delete)
            self.delete_item.grid(row=0, column=5, padx=1, sticky=tk.NE)
        else:
            self.delete_item = None

        self.bind("<Configure>", self.on_resize, "+")

    def move_down(self):
        if self.list_frame.allow_reorder:
            self.list_frame.move_down(self)

    def move_up(self):
        if self.list_frame.allow_reorder:
            self.list_frame.move_up(self)

    def delete(self):
        if self.list_frame.allow_delete:
            self.list_frame.delete_item(self)

    # noinspection PyUnusedLocal
    def on_resize(self, event):
        self.title_label.configure(wraplength=self.winfo_width())


class OrderableListItemEntry(OrderableListItem):
    # noinspection PyMissingConstructor
    def __init__(self, title, dflt_entry=""):
        super().__init__(title)
        self.entry = None
        self.entry_var = None
        self.dflt_entry = dflt_entry

    def grid_init(self, key, list_frame, parent, **kwargs):
        super().grid_init(key, list_frame, parent, **kwargs)
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self.inner_frame, textvariable=self.entry_var)
        self.entry_var.set(self.dflt_entry)
        self.entry.grid(row=0, column=0, sticky=tk.NSEW)


class OrderableListItemCheckbutton(OrderableListItem):
    # noinspection PyMissingConstructor
    def __init__(self, title, checkbox_label=""):
        super().__init__(title)
        self.sel_check_btn = None
        self.checkbox_label = checkbox_label

    def grid_init(self, key, list_frame, parent, **kwargs):
        super().grid_init(key, list_frame, parent, **kwargs)
        self.sel_check_btn = ttk.Checkbutton(self.inner_frame,
                                             padding=5,
                                             text=self.checkbox_label,
                                             command=self.check_cmd,
                                             style="even.dflt.TCheckbutton")
        self.sel_check_btn.state(['!alternate', '!selected'])
        self.sel_check_btn.grid(row=0, column=0, sticky=tk.NE)

    def check_cmd(self):
        if 'selected' in self.sel_check_btn.state():
            print("Selected!")
        elif 'selected' not in self.sel_check_btn.state():
            print("Not Selected!")


class OrderableListItemEntryCheckbutton(OrderableListItemEntry):
    # noinspection PyMissingConstructor
    def __init__(self, title, dflt_entry="", checkbox_label="", show_check=False):
        super().__init__(title, dflt_entry=dflt_entry)
        self.show_check = show_check
        self.sel_check_btn = None
        self.checkbox_label = checkbox_label

    def grid_init(self, key, list_frame, parent, **kwargs):
        super().grid_init(key, list_frame, parent, **kwargs)

        self.sel_check_btn = ttk.Checkbutton(self.inner_frame,
                                             padding=5,
                                             text=self.checkbox_label,
                                             command=self.check_cmd,
                                             style="even.dflt.TCheckbutton")
        self.sel_check_btn.state(['!alternate', '!selected'])
        if self.show_check:
            self.sel_check_btn.grid(row=0, column=1, sticky=tk.NE)

    def check_cmd(self):
        if 'selected' in self.sel_check_btn.state():
            print("Selected!")
        elif 'selected' not in self.sel_check_btn.state():
            print("Not Selected!")
