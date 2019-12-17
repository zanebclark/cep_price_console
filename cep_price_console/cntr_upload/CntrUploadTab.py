import tkinter as tk
import tkinter.ttk as ttk
import logging
from cep_price_console.utils.log_utils import CustomAdapter, debug


class CntrUploadTab (object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, master, tab_text, tab_state='normal'):
        self.master = master
        self.cont = self.master.vc
        self.nbook = self.master.nb
        self.tab_text = tab_text
        self.__tab_id = self.master.tab_id_assignment()
        self.tab_state = tab_state
        self.frame_base = ttk.Frame(self.nbook)
        self.frame_cmd = ttk.Frame(self.frame_base)
        self.frame_main = ttk.Frame(self.frame_base)
        self.btn_next = ttk.Button(self.frame_cmd)
        self.btn_prev = ttk.Button(self.frame_cmd)
        self.widgets = []
        self.manager = BusyManager(self.frame_main)

    # region tab_text
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def tab_text(self):
        return self.__tab_text

    @tab_text.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def tab_text(self, value):
        if isinstance(value, str):
            self.__tab_text = value
        else:
            CntrUploadTab.logger.error("CntrUploadTab: tab_text not string: {0}".format(str(type(value))))
    # endregion

    # region tab_id
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def tab_id(self):
        return self.__tab_id

    @tab_id.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def tab_id(self, value):
        if isinstance(value, int):
            self.__tab_id = value
        else:
            CntrUploadTab.logger.error("CntrUploadTab: tab_id not integer: {0}".format(str(type(value))))
    # endregion

    # region tab_state
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def tab_state(self):
        return self.__tab_state

    @tab_state.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def tab_state(self, value):
        states = ('normal', 'disabled', 'hidden')
        if value in states:
            self.__tab_state = value
        else:
            CntrUploadTab.logger.error("Tab State ({0}) not a valid value: {1}".format(value, states))
    # endregion

    @debug(lvl=logging.NOTSET, prefix='')
    def nbook_add(self):
        CntrUploadTab.logger.log(logging.NOTSET, "Tab ID: {0}".format(str(self.tab_id)))
        self.nbook.add(self.frame_base, text=self.tab_text, state=self.tab_state)
        self.frame_base.columnconfigure(0, weight=1)
        self.frame_base.rowconfigure(0, weight=1)
        self.frame_main.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame_cmd.grid(row=1, column=0, sticky=tk.SE)
        if self.tab_id != self.master.max_tab_id:
            self.btn_next.config(text="Proceed")
            self.btn_next.state(['disabled'])
            self.btn_next.grid(row=0, column=2)
        if self.tab_id != 0:
            self.btn_prev.config(text="Previous", command=lambda: self.master.tab_switcher(self.tab_id - 1))
            self.btn_prev.grid(row=0, column=1)

    @debug(lvl=logging.DEBUG, prefix='')
    def add_widget(self, widget: object):
        self.widgets.append(widget)

    @debug(lvl=logging.NOTSET, prefix='')
    def toggle_tab(self, tab_state: str):
        self.tab_state = tab_state
        self.nbook.tab(self.tab_id, state=self.tab_state)


class BusyManager:
    def __init__(self, widget):
        self.toplevel = widget.winfo_toplevel()
        self.widgets = {}

    def busy(self, widget=None):

        # attach busy cursor to toplevel, plus all windows
        # that define their own cursor.

        if widget is None:
            w = self.toplevel  # myself
        else:
            w = widget

        if not self.widgets.get(str(w)):
            try:
                # attach cursor to this widget
                cursor = w.cget("cursor")
                if cursor != "watch":
                    self.widgets[str(w)] = (w, cursor)
                    w.config(cursor="watch")
                else:
                    pass
            except tk.TclError:
                pass
        else:
            pass

        for w in w.children.values():
            self.busy(w)

    def not_busy(self):
        # restore cursors
        for w, cursor in self.widgets.values():
            try:
                w.config(cursor=cursor)
            except tk.TclError:
                pass
        self.widgets = {}

