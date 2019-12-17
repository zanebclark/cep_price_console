from cep_price_console.utils.log_utils import CustomAdapter, debug
import tkinter as tk
import tkinter.ttk as ttk
import logging


logger = CustomAdapter(logging.getLogger(str(__name__)), None)


class PanedWindowBase(tk.PanedWindow):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master,
                 orient,
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
                         showhandle=False,
                         orient=orient,
                         sashpad=sashpad,
                         opaqueresize=opaqueresize,
                         *args,
                         **kwargs)
        self._active_sash = None
        self._on_click = on_click
        self._image = image
        self._cursor = cursor
        self._orient = orient

        self._pane_list = []

        self._handle_list = []
        self._list_of_panes = []
        self._dict_of_handles = {}
        self._dict_of_panes = {}
        self._configure_callbacks = []

        if not opaqueresize:
            disallow_dragging = True

        self._disallow_dragging = disallow_dragging

        if opaqueresize:
            self.bind('<Button-1>', self._on_mark_sash)
            self.bind('<B1-Motion>', self._on_drag_sash)
            self.bind('<ButtonRelease-1>', self._on_release)

        if self._orient == tk.VERTICAL:
            self._width = size
            self._height = 2 * sashpad
        elif self._orient == tk.HORIZONTAL:
            self._width = 2 * sashpad
            self._height = size
        else:
            raise ValueError

        self.handle_class = handle_class

    @debug(lvl=logging.DEBUG, prefix='')
    def remove_all(self):
        for handle in self._handle_list:
            handle.place_forget()
            del handle

        self._handle_list = []

        for pane in self._list_of_panes:
            pane.unbind("<Configure>")
            super().remove(pane)

        self._list_of_panes = []

        self._active_sash = None

    # noinspection PyShadowingNames
    @debug(lvl=logging.DEBUG, prefix='')
    def add(self, pane, **kwargs):
        super().add(pane, **kwargs)
        self._list_of_panes.append(pane)
        quantity_of_panes = len(self._list_of_panes)
        PanedWindowBase.logger.log(logging.DEBUG, "Quantity of panes: {}".format(quantity_of_panes))

        if quantity_of_panes >= 2:
            sash_index = quantity_of_panes-2
            pane.sash_index = sash_index
            PanedWindowBase.logger.log(logging.DEBUG, "Handle Index: {}".format(pane.sash_index))
            handle = self.handle_class(self,
                                       sash_index,
                                       height=self._height,
                                       width=self._width,
                                       cursor=self._cursor,
                                       disallow_dragging=self._disallow_dragging,
                                       on_click=self._on_click,
                                       image=self._image)
            pane.sash_object = handle

            if self._orient == tk.VERTICAL:
                handle.place(relx=0.5, anchor="c")
            elif self._orient == tk.HORIZONTAL:
                handle.place(rely=0.5, anchor="c")
            else:
                raise ValueError

            self._handle_list.append(handle)
            PanedWindowBase.logger.log(logging.DEBUG, "Callback 1: Sash Index: {}".format(pane.sash_index))
            callback_id1 = pane.bind(
                "<Configure>",
                lambda event, sash_index=sash_index:
                self._on_configure_pane(sash_index), "+")
            PanedWindowBase.logger.log(logging.DEBUG, "Callback 2: Sash Index: {}".format(pane.sash_index))
            callback_id2 = self._list_of_panes[sash_index].bind(
                "<Configure>",
                lambda event, sash_index=sash_index:
                self._on_configure_pane(sash_index), "+")
            self._configure_callbacks.append((callback_id1, callback_id2))

    @debug(lvl=logging.DEBUG, prefix='')
    def _on_mark_sash(self, event):
        identity = self.identify(event.x, event.y)
        if len(identity) == 2:
            self._active_sash = sash_index = identity[0]
            callback_id1, callback_id2 = self._configure_callbacks[sash_index]
            self._list_of_panes[sash_index+1].unbind(callback_id1)
            self._list_of_panes[sash_index].unbind(callback_id2)
        else:
            self._active_sash = None

    # noinspection PyUnusedLocal, PyShadowingNames
    @debug(lvl=logging.DEBUG, prefix='')
    def _on_release(self, event):
        sash_index = self._active_sash
        if sash_index is not None:
            callback_id1 = self._list_of_panes[sash_index+1].bind(
                "<Configure>",
                lambda event, sash_index=sash_index: self._on_configure_pane(sash_index), "+")

            callback_id2 = self._list_of_panes[sash_index].bind(
                "<Configure>",
                lambda event, sash_index=sash_index: self._on_configure_pane(sash_index), "+")

            self._configure_callbacks[sash_index] = (callback_id1, callback_id2)

            self._active_sash = None

    # noinspection PyUnresolvedReferences
    @debug(lvl=logging.DEBUG, prefix='')
    def _on_drag_sash(self, event):
        identity = self.identify(event.x, event.y)
        if identity not in (None, "") and self._active_sash is not None:
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
                 # name,
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
                         # name,
                         orient=tk.VERTICAL,
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
                 # name,
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
                         # name,
                         orient=tk.HORIZONTAL,
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
