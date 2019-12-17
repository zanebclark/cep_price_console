from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils.gui_utils import center_window
import tkinter as tk
import tkinter.ttk as ttk
import logging


class Step(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    step_dict = {}

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, namely, order, *args, **kwargs):
        self.order = order
        self.namely = namely
        self.view = view
        # noinspection PyArgumentList
        super().__init__(self.view, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame_cmd = ttk.Frame(self)
        self.frame_cmd.grid(row=1, column=0, sticky=tk.SE)

        self.frame_main = ttk.Frame(self)
        self.frame_main.grid(row=0, column=0, sticky=tk.NSEW)

        self.btn_next = ttk.Button(self.frame_cmd)
        self.btn_next.config(text="Proceed")
        self.btn_next.state(['disabled'])
        self.btn_next.grid(row=0, column=3)
        self.btn_next.bind("<ButtonRelease-1>", self.next)
        self.btn_prev = ttk.Button(self.frame_cmd)
        self.btn_prev.config(text="Previous")
        self.btn_prev.grid(row=0, column=2)
        self.btn_prev.bind("<ButtonRelease-1>", self.prev)
        self.complete = False

        Step.step_dict[self.namely] = self
        center_window(win_obj=self.view)

    @debug(lvl=logging.DEBUG, prefix='')
    def open(self):
        self.grid()

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        self.grid_remove()

    @debug(lvl=logging.DEBUG, prefix='')
    def next(self, *args):
        pass

    @debug(lvl=logging.DEBUG, prefix='')
    def prev(self, *args):
        pass
