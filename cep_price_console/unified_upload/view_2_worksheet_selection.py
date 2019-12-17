from cep_price_console.utils.log_utils import CustomAdapter, debug
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import logging


class WorksheetSelection(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        self.initial = False
        self.terminal = False
        self.view = view
        # noinspection PyArgumentList
        super().__init__(self.view, style="even.group.TFrame", padding=5, relief=tk.RIDGE, *args, **kwargs)
        self.__current_row = 0
        self.columnconfigure(0, weight=1)

        self.header_1 = ttk.Label(
            self,
            text="Step 2: Contract Details Worksheet",
            style="even.heading2.TLabel"
        )
        self.header_1.grid(row=self.current_row, column=0, sticky=tk.W)

        ttk.Separator(self).grid(row=self.current_row, column=0, sticky=tk.EW)

        self.inst_1 = ttk.Label(
            self,
            anchor=tk.NW,
            justify=tk.LEFT,
            text="Use the combobox below to select the correct worksheet to load data from.",
            style="even.notes.TLabel",
            wraplength=20
        )
        self.inst_1.grid(row=self.current_row, column=0, sticky=tk.W)

        ttk.Separator(self).grid(row=self.current_row, column=0, sticky=tk.EW)

        self.ws_sel_var = tk.StringVar(name="Worksheet Selection")
        self.ws_sel_var.trace_add('write', self.set_ws_sel)

        self.ws_sel_cmb = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.ws_sel_var,
            values=self.view.ws_sheet_names
        )
        self.ws_sel_cmb.grid(row=self.current_row, column=0, sticky=tk.EW)

        ttk.Separator(self).grid(row=self.current_row, column=0, sticky=tk.EW)

        self.header_2 = ttk.Label(
            self,
            text="Step 3: Header Row",
            style="even.heading2.TLabel"
        )
        self.header_2.grid(row=self.current_row, column=0, sticky=tk.W)

        self.inst_2 = ttk.Label(
            self,
            anchor=tk.NW,
            justify=tk.LEFT,
            text="Enter the header row",
            style="even.notes.TLabel",
            wraplength=20
        )
        self.inst_2.grid(row=self.current_row, column=0, sticky=tk.W)

        self.header_row_var = tk.IntVar(name="Header Row")

        header_validation = (self.register(self.validate_integer))

        self.header_row_entry = ttk.Entry(
            self,
            textvariable=self.header_row_var,
            validate='focusout',
            validatecommand=(header_validation, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        )
        self.header_row_entry.grid(row=self.current_row, column=0, sticky=tk.EW)

        ttk.Separator(self).grid(row=self.current_row, column=0, sticky=tk.EW)

        self.bind("<Configure>", self.on_resize)

        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_remove()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def set_ws_sel(self, *args):
        if self.ws_sel_var.get() != "":
            self.view.ws_name_selection = self.ws_sel_var.get()

    @debug(lvl=logging.DEBUG, prefix='')
    def open(self):
        self.ws_sel_var.set(self.view.ws_name_selection)
        self.ws_sel_cmb.config(values=self.view.ws_sheet_names)
        self.header_row_var.set(self.view.header_row)
        self.grid()

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        self.grid_remove()

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.inst_1.configure(wraplength=self.winfo_width())
        self.inst_2.configure(wraplength=self.winfo_width())

    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def current_row(self):
        row = self.__current_row
        self.__current_row += 1
        return row

    # noinspection PyUnusedLocal,PyProtectedMember
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_integer(self,
                         action,
                         index,
                         value_if_allowed,
                         prior_value,
                         text,
                         validation_type,
                         trigger_type,
                         widget_name):
        if str.isdigit(value_if_allowed) or value_if_allowed == "":
            if str.isdigit(value_if_allowed):
                int_val = int(value_if_allowed)
                if int_val != 0:
                    self.view.header_row = int(value_if_allowed)
                    return True
                else:
                    self.__class__.logger.log(logging.DEBUG, "Called with 0 value. No action taken.")
                    messagebox.askokcancel(
                        "Invalid Header Row",
                        "The Header Row value cannot be 0.",
                        parent=self.view
                    )
                    return False
        elif not str.isdigit(value_if_allowed) and value_if_allowed != "":
            messagebox.askokcancel(
                "Invalid Header Row",
                "The Header Row value must be an integer.",
                parent=self.view
            )
            return False
        else:
            return False
