from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
from cep_price_console.utils.gui_utils import center_window
import tkinter as tk
import tkinter.ttk as ttk
import logging
from tkinter import messagebox

# from cep_price_console.gui_utils import parsegeometry
# from tkinter import filedialog
# import xlsxwriter
# from cep_price_console.db_management.price_matrix_utils import MatrixSherpa
# from tkintertable.Tables import TableCanvas, Preferences
# from tkintertable.TableModels import TableModel
# import pickle


class PriceList(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        # ttk.Frame.place
        self.master = master
        self.name = str(PriceList.__name__).lower()
        super().__init__(name=self.name, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("Filtering Criteria")
        self.iconbitmap(config.ICON_FILE)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.paned_outer = PanedWindowVertical(self,
                                               name="paned_outer",
                                               sashrelief=tk.RAISED,
                                               sashwidth=7)

        self.paned_outer.grid(row=0, column=0, sticky=tk.NSEW)

        print(dir(self.paned_outer))
        for thing in range(1, 5):
            something = PanedEntryFrame(master=self.paned_outer,
                                        name=str(thing),
                                        toplevel=self)
            self.paned_outer.add(something,
                                 width=something.winfo_reqwidth(),
                                 pady=5,
                                 padx=5,
                                 stretch="always")

        center_window(win_obj=self)

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        msgbox = messagebox.askokcancel("Quit", "Do you want to quit?", parent=self)
        if msgbox:
            self.destroy()


# noinspection PyUnusedLocal
class PanedEntryFrame(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, toplevel, *args, **kwargs):
        self.toplevel = toplevel
        # noinspection PyArgumentList
        super().__init__(master, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # TODO: give it a clear name
        # TODO: use this name in a panedwindow-specific dictionary
        # TODO: use this name to remove it
        print("widgetName: {}".format(self.master.widgetName))
        print("winfo_name: {}".format(self.master.winfo_name()))

        entry_validation = (self.register(self.validate_selection),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self,
                               textvariable=self.entry_var,
                               validate='focusout',
                               validatecommand=entry_validation)
        self.entry.grid(row=0, column=0, sticky=tk.NSEW)

        self.close_btn = ttk.Button(self,
                                    text="x",
                                    command=self.remove,
                                    width=1)
        self.close_btn.grid(row=0, column=1, sticky=tk.NE)

    @debug(lvl=logging.DEBUG, prefix='')
    def remove(self):
        something = self.master.nametowidget(".pricelist.paned_outer.{}".format(self.winfo_name()))
        self.master.remove(something)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_selection(self,
                           action,
                           index,
                           value_if_allowed,
                           prior_value,
                           text,
                           validation_type,
                           trigger_type,
                           widget_name):
        # if value_if_allowed != "":
        return True


class PanedWindowBase(tk.PanedWindow):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master,
                 name,
                 orient,
                 color,
                 size,
                 sashpad,
                 disallow_dragging,
                 on_click,
                 image,
                 cursor,
                 opaqueresize,
                 handle_class,
                 *args,
                 **kwargs):
        super().__init__(master,
                         name=name,
                         showhandle=False,
                         orient=orient,
                         sashpad=sashpad,
                         opaqueresize=opaqueresize,
                         *args,
                         **kwargs)
        self._active_sash = None
        self._on_click = on_click
        self._image = image
        self._color = color
        self._cursor = cursor
        self._orient = orient

        self._handle_list = []
        self._list_of_panes = []
        self._configure_callbacks = []

        if not opaqueresize:
            disallow_dragging = True

        self._disallow_dragging = disallow_dragging

        if opaqueresize:
            self.bind('<Button-1>', self._on_mark_sash)
            self.bind('<B1-Motion>', self._on_drag_sash)
            self.bind('<ButtonRelease-1>', self._on_release)

        if self._orient == tk.VERTICAL:
            self._width = size  # TODO: I don't understand this stuff
            self._height = 2 * sashpad  # TODO: I don't understand this stuff
        elif self._orient == tk.HORIZONTAL:
            self._width = 2 * sashpad  # TODO: I don't understand this stuff
            self._height = size  # TODO: I don't understand this stuff
        else:
            raise ValueError

        self.handle_class = handle_class

    @debug(lvl=logging.DEBUG, prefix='')
    def remove(self, pane, **kwargs):
        super().remove(pane)

        self._list_of_panes.remove(pane)
        quantity_of_panes = len(self._list_of_panes)

        if quantity_of_panes >= 2:
            handle_index = quantity_of_panes-2
        #     handle = self.handle_class(self,
        #                                handle_index,
        #                                # bg=self._color,
        #                                height=self._height,
        #                                width=self._width,
        #                                cursor=self._cursor,
        #                                disallow_dragging=self._disallow_dragging,
        #                                on_click=self._on_click,
        #                                image=self._image)
        #
        #     if self._orient == tk.VERTICAL:
        #         handle.place(relx=0.5, anchor="c")
        #     elif self._orient == tk.HORIZONTAL:
        #         handle.place(rely=0.5, anchor="c")
        #     else:
        #         raise ValueError
        #
        #     self._handle_list.append(handle)
        #
        #     callback_id1 = pane.bind(
        #         "<Configure>",
        #         lambda event, handle_index=handle_index:
        #         self._on_configure_pane(handle_index), "+")
        #     callback_id2 = self._list_of_panes[handle_index].bind(
        #         "<Configure>",
        #         lambda event, handle_index=handle_index:
        #         self._on_configure_pane(handle_index), "+")
        #     self._configure_callbacks.append((callback_id1, callback_id2))

    @debug(lvl=logging.DEBUG, prefix='')
    def add(self, pane, **kwargs):
        super().add(pane, **kwargs)

        self._list_of_panes.append(pane)
        quantity_of_panes = len(self._list_of_panes)
        PanedWindowBase.logger.log(logging.DEBUG, "Quantity of panes: {}".format(quantity_of_panes))

        if quantity_of_panes >= 2:
            handle_index = quantity_of_panes-2
            PanedWindowBase.logger.log(logging.DEBUG, "Handle Index: {}".format(handle_index))
            handle = self.handle_class(self,
                                       handle_index,
                                       # bg=self._color,
                                       height=self._height,
                                       width=self._width,
                                       cursor=self._cursor,
                                       disallow_dragging=self._disallow_dragging,
                                       on_click=self._on_click,
                                       image=self._image)

            if self._orient == tk.VERTICAL:
                handle.place(relx=0.5, anchor="c")
            elif self._orient == tk.HORIZONTAL:
                handle.place(rely=0.5, anchor="c")
            else:
                raise ValueError

            self._handle_list.append(handle)

            callback_id1 = pane.bind(
                "<Configure>",
                lambda event, handle_index=handle_index:
                self._on_configure_pane(handle_index), "+")
            callback_id2 = self._list_of_panes[handle_index].bind(
                "<Configure>",
                lambda event, handle_index=handle_index:
                self._on_configure_pane(handle_index), "+")
            self._configure_callbacks.append((callback_id1, callback_id2))

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_mark_sash(self, event):
        identity = self.identify(event.x, event.y)
        print(identity)

        if len(identity) == 2:
            self._active_sash = handle_index = identity[0]
            callback_id1, callback_id2 = self._configure_callbacks[handle_index]

            self._list_of_panes[handle_index+1].unbind(callback_id1)
            self._list_of_panes[handle_index].unbind(callback_id2)
        else:
            self._active_sash = None

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def _on_release(self, event):
        handle_index = self._active_sash

        callback_id1 = self._list_of_panes[handle_index+1].bind(
            "<Configure>",
            lambda event, handle_index=handle_index: self._on_configure_pane(handle_index), "+")

        callback_id2 = self._list_of_panes[handle_index].bind(
            "<Configure>",
            lambda event, handle_index=handle_index: self._on_configure_pane(handle_index), "+")

        self._configure_callbacks[handle_index] = (callback_id1, callback_id2)

        self._active_sash = None

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_drag_sash(self, event):
        coord_x = event.x
        coord_y = event.y

        super().sash_place(self._active_sash, coord_x, coord_y)
        self._update_position_all_handles()

        return "break"


class PanedWindowVertical(PanedWindowBase):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master,
                 name,
                 color="gray",
                 size=60,
                 sashpad=2,
                 disallow_dragging=False,
                 on_click=None,
                 cursor=None,
                 opaqueresize=True,
                 *args,
                 **kwargs):

        # noinspection SpellCheckingInspection
        image = tk.PhotoImage(data="R0lGODlhGAADAPIFAEBAQGBgYICAgLu7u8zMzAAAAAAAAAAAACH5BAEAAAUA"
                                   "LAAAAAAYAAMAAAMaWBJQym61N2UZJTisb96fpxGD4JBmgZ4lKyQAOw==")

        super().__init__(master,
                         name,
                         orient=tk.VERTICAL,
                         color=color,
                         size=size,
                         sashpad=sashpad,
                         disallow_dragging=disallow_dragging,
                         on_click=on_click,
                         image=image,
                         cursor=cursor,
                         opaqueresize=opaqueresize,
                         handle_class=VerticalHandle,
                         *args,
                         **kwargs)

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_configure_pane(self, sash_index):
        x, y = super().sash_coord(sash_index)
        self._handle_list[sash_index].place(y=y)

    @debug(lvl=logging.DEBUG, prefix='')
    def _update_position_all_handles(self):
        for sash_index, handle in enumerate(self._handle_list):
            x, y = super().sash_coord(sash_index)
            handle.place(y=y)


class PanedWindowHorizontal(PanedWindowBase):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master,
                 name,
                 color="gray",
                 size=60,
                 sashpad=2,
                 disallow_dragging=False,
                 on_click=None,
                 cursor=None,
                 opaqueresize=True,
                 *args,
                 **kwargs):

        # noinspection SpellCheckingInspection
        image = tk.PhotoImage(data="R0lGODlhGAADAPIFAEBAQGBgYICAgLu7u8zMzAAAAAAAAAAAACH5BAEAAAUALAAAAAAY"
                                   "AAMAAAMaWBJQym61N2UZJTisb96fpxGD4JBmgZ4lKyQAOw==")

        super().__init__(master,
                         name,
                         orient=tk.HORIZONTAL,
                         color=color,
                         size=size,
                         sashpad=sashpad,
                         disallow_dragging=disallow_dragging,
                         on_click=on_click,
                         image=image,
                         cursor=cursor,
                         opaqueresize=opaqueresize,
                         handle_class=HorizontalHandle,
                         *args,
                         **kwargs)

    @debug(lvl=logging.DEBUG, prefix='')
    def _update_position_all_handles(self):
        for sash_index, handle in enumerate(self._handle_list):
            x, y = super().sash_coord(sash_index)
            handle.place(x=x)

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_configure_pane(self, sash_index):
        x, y = super().sash_coord(sash_index)
        self._handle_list[sash_index].place(x=x)


class Handle(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    def __init__(self, panedwindow, sash_index, disallow_dragging=False, on_click=None, *args, **kwargs):
        image = kwargs.pop("image", None)
        # noinspection PyArgumentList
        super().__init__(panedwindow, *args, **kwargs)

        self._sash_index = sash_index

        if image:
            self._event_area = ttk.Label(self, image=image)
            self._event_area.pack()
        else:
            self._event_area = self

        self._center = int(self._event_area.winfo_reqwidth()/2), int(self._event_area.winfo_reqheight()/2)

        if disallow_dragging:
            if on_click:
                self._event_area.bind('<Button-1>', lambda event: on_click())
        else:
            # noinspection PyProtectedMember
            self._event_area.bind('<Button-1>', self._initiate_motion)
            # noinspection PyProtectedMember
            self._event_area.bind('<B1-Motion>', self._on_dragging)
            # noinspection PyProtectedMember
            self._event_area.bind('<ButtonRelease-1>', self.master._on_release)

    @debug(lvl=logging.DEBUG, prefix='')
    def _initiate_motion(self, event):
        self.master._active_sash = self._sash_index

        self._dx = event.x
        self._dy = event.y

    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def sash_index(self):
        return self._sash_index

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_dragging(self, event):
        raise NotImplementedError


class VerticalHandle(Handle):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_dragging(self, event):
        y = event.y_root - self.master.winfo_rooty() - self._dy
        self.master.sash_place(self._sash_index, 1, y)
        # noinspection PyProtectedMember
        self.master._update_position_all_handles()


class HorizontalHandle(Handle):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_dragging(self, event):
        x = event.x_root - self.master.winfo_rootx() - self._dx
        self.master.sash_place(self._sash_index, x, 1)
        # noinspection PyProtectedMember
        self.master._update_position_all_handles()
