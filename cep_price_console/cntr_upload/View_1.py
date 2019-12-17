from cep_price_console.cntr_upload.CntrUploadTab import CntrUploadTab
from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import os
import logging


class Step1FileSelection(CntrUploadTab):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, tab_text, tab_state='normal'):
        CntrUploadTab.__init__(self,
                               master,
                               tab_text,
                               tab_state)
        self.file_selection_hdr = ttk.Label(self.frame_main)

        # Contract Upload Filename
        self.filename_frame = ttk.Frame(self.frame_main)
        self.filename_lbl = ttk.Label(self.filename_frame)
        self.fullpath_var = tk.StringVar()
        self.filename_entry = ttk.Entry(self.filename_frame)
        self.filename_btn = ttk.Button(self.filename_frame)
        self.filename_focus = False

        # Contract Details Worksheet
        self.ws_list = []
        self.ws_sel_frame = ttk.Frame(self.frame_main)
        self.ws_sel_lbl = ttk.Label(self.ws_sel_frame)
        self.ws_sel_var = tk.StringVar()
        self.ws_sel_cmb = ttk.Combobox(self.ws_sel_frame, state="readonly")

        # Header Row
        self.header_row_frame = ttk.Frame(self.frame_main)
        self.header_row_lbl = ttk.Label(self.header_row_frame)
        self.header_row_var = tk.IntVar()
        self.header_row_entry = ttk.Entry(self.header_row_frame)
        self.last_cell_btn = ttk.Button(self.header_row_frame)

        # Last Cell
        self.last_cell_frame = ttk.Frame(self.frame_main)
        self.last_row_lbl = ttk.Label(self.last_cell_frame)
        self.last_row_var = tk.IntVar()
        self.last_row_entry = ttk.Entry(self.last_cell_frame)
        self.last_col_lbl = ttk.Label(self.last_cell_frame)
        self.last_col_var = tk.IntVar()
        self.last_col_entry = ttk.Entry(self.last_cell_frame)

        self.populate_frame()

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        self.frame_main.columnconfigure(0, weight=2)
        self.frame_main.columnconfigure(1, weight=1)
        self.frame_main.columnconfigure(2, weight=1)

        # Configure Header Label
        self.file_selection_hdr.config(text="File Selection", font=('Verdana Bold', '20'))
        self.file_selection_hdr.grid(row=0, column=0, sticky=tk.NW)

        # Configure Contract Filename Widgets
        self.filename_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW)
        self.filename_frame.columnconfigure(0, weight=1)
        self.filename_lbl.config(text="Contract Filename")
        self.filename_lbl.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        fullpath_validation = (self.filename_frame.register(self.validate_fullpath),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.filename_entry.config(textvariable=self.fullpath_var,
                                   validate='focusout',
                                   validatecommand=fullpath_validation)
        self.filename_entry.grid(row=1, column=0, sticky=tk.EW)
        self.filename_btn.config(text="Browse", command=self.file_dialog)
        self.filename_btn.grid(row=1, column=1, sticky=tk.E)

        # Configure Contract Details Worksheet
        self.ws_sel_frame.grid(row=2, column=0, sticky=tk.EW)
        self.ws_sel_frame.columnconfigure(0, weight=1)
        self.ws_sel_lbl.config(text="Contract Details Worksheet")
        self.ws_sel_lbl.grid(row=0, column=0, sticky=tk.EW)
        self.ws_sel_var.trace_add('write', self.set_ws_sel)
        self.ws_sel_cmb.config(textvariable=self.ws_sel_var)
        self.ws_sel_cmb.grid(row=1, column=0, sticky=tk.EW)

        # Configure Header Row Widgets
        self.header_row_frame.grid(row=2, column=1, sticky=tk.EW)
        self.header_row_frame.columnconfigure(0, weight=1)
        self.header_row_lbl.config(text="Header Row")
        self.header_row_lbl.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
        header_validation = (self.header_row_frame.register(self.validate_header_row),
                             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.header_row_entry.config(textvariable=self.header_row_var,
                                     validate='focusout',
                                     validatecommand=header_validation)
        self.header_row_entry.grid(row=1, column=0, sticky=tk.EW)
        self.last_cell_btn.config(text="Detect", command=self.last_cell_detect)
        self.last_cell_btn.grid(row=1, column=1, sticky=tk.E)

        self.last_cell_frame.grid(row=2, column=2, sticky=tk.EW)
        self.last_row_lbl.config(text="Last Row")
        self.last_row_lbl.grid(row=0, column=0, sticky=tk.EW)
        last_row_validation = (self.last_cell_frame.register(self.validate_last_row),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.last_row_entry.config(textvariable=self.last_row_var,
                                   validate='focusout',
                                   validatecommand=last_row_validation)
        self.last_row_entry.grid(row=1, column=0)
        self.last_row_var.trace_add('write', self.set_last_row)
        self.last_col_lbl.config(text="Last Column")
        self.last_col_lbl.grid(row=0, column=1, sticky=tk.EW)
        last_col_validation = (self.last_cell_frame.register(self.validate_last_col),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.last_col_entry.config(textvariable=self.last_col_var,
                                   validate='focusout',
                                   validatecommand=last_col_validation)
        self.last_col_entry.grid(row=1, column=1)
        self.last_col_var.trace_add('write', self.set_last_col)
        self.btn_next.bind("<ButtonRelease-1>", self.proceeding)
        self.flow_manager('reset')
        # self.testing()
        # self.ecolab_testing()

    @debug(lvl=logging.DEBUG, prefix='')
    def testing(self):
        filename = config.MEDIA_PATH / "PA_30019324_0062156167_20181129105241.xlsx"
        self.fullpath_var.set(filename)
        self.filename_entry.validate()
        self.ws_sel_cmb.set('Product Addendum')
        self.header_row_var.set(5)
        self.header_row_entry.validate()

    @debug(lvl=logging.DEBUG, prefix='')
    def ecolab_testing(self):
        filename = config.MEDIA_PATH / "ECOW 14221 5-14-19.xls"
        self.fullpath_var.set(filename)
        self.filename_entry.validate()
        self.ws_sel_cmb.set('DistributorPricingRpt')
        self.header_row_var.set(21)
        self.header_row_entry.validate()
        self.last_cell_detect()

    @debug(lvl=logging.DEBUG, prefix='')
    def file_dialog(self):
        self.manager.busy()
        filename_options = dict(
            title='Select Contract',
            initialdir=str(os.path.expanduser('~')).replace('\\', '/'),
            initialfile=None,
            parent=self.master,
            filetypes=[(
                'Excel Files',
                ('.xlsx',
                 '.xlsm',
                 '.xlsb',
                 '.xltx',
                 '.xltm',
                 '.xls',
                 '.xlt',
                 '.xls',
                 '.xml',
                 '.xml',
                 '.xlam',
                 '.xla',
                 '.xlw',
                 '.xlr,'))]
        )
        self.fullpath_var.set(str(filedialog.askopenfilename(**filename_options)).replace("/", "\\"))
        self.filename_entry.validate()
        # self.set_fullpath()
        self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def set_ws_sel(self, *args):
        self.manager.busy()
        if self.ws_sel_var.get() not in (None, ""):
            Step1FileSelection.logger.log(logging.NOTSET, "Called: {0}".format(self.ws_sel_var.get()))
            self.flow_manager('hdr_detect')
            self.cont.set_ws_sel(self.ws_sel_var.get())
        else:
            Step1FileSelection.logger.log(logging.NOTSET, "Called without value. No action taken.")
        self.manager.not_busy()

    @debug(lvl=logging.DEBUG, prefix='')
    def last_cell_detect(self):
        self.manager.busy()
        Step1FileSelection.logger.log(logging.DEBUG, "Called: {0}".format(str(self.header_row_var.get())))
        try:
            last_row, last_col = self.cont.set_header_row(self.header_row_var.get())
        except Exception as ex:
            messagebox.askokcancel(
                type(ex).__name__,
                ex.args,
                parent=self.master
            )
            self.header_row_var.set("")
            self.last_row_var.set("")
            self.last_col_var.set("")
        else:
            Step1FileSelection.logger.log(logging.NOTSET, "Last Row: {0}, Last Col: {1}".format(last_row, last_col))
            self.last_row_var.set(last_row)
            self.last_row_entry.validate()
            self.last_col_var.set(last_col)
            self.last_col_entry.validate()
            self.flow_manager('last_cell')
        self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def set_last_row(self, *args):
        try:
            value = self.last_row_var.get()
        except tk.TclError:
            Step1FileSelection.logger.log(logging.NOTSET, "Called. Value wasn't an integer. No action taken.")
        else:
            if value != 0:
                Step1FileSelection.logger.log(logging.NOTSET, "Called: {0}".format(str(value)))
                self.cont.set_last_row(value)
            else:
                Step1FileSelection.logger.log(logging.NOTSET, "Called with 0 value. No action taken.")

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def set_last_col(self, *args):
        try:
            value = self.last_col_var.get()
        except tk.TclError:
            Step1FileSelection.logger.log(logging.NOTSET, "Called. Value wasn't an integer. No action taken.")
        else:
            if value != 0:
                Step1FileSelection.logger.log(logging.NOTSET, "Called: {0}".format(str(value)))
                self.cont.set_last_col(value)
            else:
                Step1FileSelection.logger.log(logging.NOTSET, "Called with 0 value. No action taken.")

    @debug(lvl=logging.DEBUG, prefix='')
    def flow_manager(self, status):
        if status == 'reset':
            self.fullpath_var.set("")
            self.filename_entry.state(['!disabled'])
            self.filename_btn.state(['!disabled'])
            self.ws_sel_var.set("")
            self.ws_sel_cmb.config(value=None)
            self.ws_sel_cmb.state(['disabled'])
            self.header_row_var.set(0)
            self.header_row_entry.state(['disabled'])
            self.last_cell_btn.state(['disabled'])
            self.last_row_var.set(0)
            self.last_row_entry.state(['disabled'])
            self.last_col_var.set(0)
            self.last_col_entry.state(['disabled'])
            self.btn_next.state(['disabled'])
        elif status == 'sel_ws':
            self.filename_entry.state(['!disabled'])
            self.filename_btn.state(['!disabled'])
            self.ws_sel_var.set("")
            self.ws_sel_cmb.state(['!disabled'])
            self.header_row_var.set(0)
            self.header_row_entry.state(['disabled'])
            self.last_cell_btn.state(['disabled'])
            self.last_row_var.set(0)
            self.last_row_entry.state(['disabled'])
            self.last_col_var.set(0)
            self.last_col_entry.state(['disabled'])
            self.btn_next.state(['disabled'])
        elif status == 'hdr_detect':
            self.filename_entry.state(['!disabled'])
            self.filename_btn.state(['!disabled'])
            self.ws_sel_cmb.state(['!disabled'])
            self.header_row_var.set(0)
            self.header_row_entry.state(['!disabled'])
            self.last_cell_btn.state(['!disabled'])
            self.last_row_var.set(0)
            self.last_row_entry.state(['disabled'])
            self.last_col_var.set(0)
            self.last_col_entry.state(['disabled'])
            self.btn_next.state(['disabled'])
        elif status == 'last_cell':
            self.filename_entry.state(['!disabled'])
            self.filename_btn.state(['!disabled'])
            self.ws_sel_cmb.state(['!disabled'])
            self.header_row_entry.state(['!disabled'])
            self.last_cell_btn.state(['!disabled'])
            self.last_row_entry.state(['!disabled'])
            self.last_col_entry.state(['!disabled'])
            self.btn_next.state(['!disabled'])
        elif status == 'proceed':
            self.filename_entry.state(['readonly'])
            self.filename_btn.state(['readonly'])
            self.ws_sel_cmb.state(['readonly'])
            self.header_row_entry.state(['readonly'])
            self.last_cell_btn.state(['readonly'])
            self.last_row_entry.state(['readonly'])
            self.last_col_entry.state(['readonly'])
            self.btn_next.state(['!disabled'])

    # noinspection PyUnusedLocal,PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def proceeding(self, *args):
        self.manager.busy()
        self.master.step_2.populate_frame()
        self.master.tab_switcher(1)
        self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_header_row(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type,
                            widget_name):
        self.manager.busy()
        if value_if_allowed != "":
            if str.isdigit(value_if_allowed):
                try:
                    int_val = int(value_if_allowed)
                except TypeError:
                    Step1FileSelection.logger.log(logging.DEBUG, "Invalid messagebox called")
                    messagebox.askokcancel(
                        "Invalid Header Row Entry",
                        "The header row value must be an integer.",
                        parent=self.master
                    )
                    self.header_row_var.set(0)
                    self.manager.not_busy()
                    return False
                else:
                    if int_val != 0:
                        Step1FileSelection.logger.log(logging.DEBUG, "Called: {0}".format(str(int_val)))
                        self.manager.not_busy()
                        return True
                    else:
                        Step1FileSelection.logger.log(logging.DEBUG, "Called without value. No action taken.")
                        self.manager.not_busy()
                        return False
            else:
                messagebox.askokcancel(
                    "Invalid Header Row Entry",
                    "The header row value must be an integer.",
                    parent=self.master
                )
                self.header_row_var.set(0)
                self.manager.not_busy()
                return False
        else:
            self.header_row_var.set(0)
            self.manager.not_busy()
            return True

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_fullpath(self,
                          action,
                          index,
                          value_if_allowed,
                          prior_value,
                          text,
                          validation_type,
                          trigger_type,
                          widget_name):
        self.manager.busy()
        if value_if_allowed != "":
            filename, file_extension = os.path.splitext(value_if_allowed)
            if file_extension.lower().strip() in (".xlsx", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xls", ".xlt",
                                                  ".xls", ".xml", ".xml", ".xlam", ".xla", ".xlw", ".xlr"):
                Step1FileSelection.logger.log(logging.NOTSET, "set_fullpath called. Filepath valid. Extension "
                                                              "valid. Filepath: {0}".format(value_if_allowed))
                try:
                    self.cont.set_ws_fullpath(value_if_allowed)
                except FileNotFoundError:
                    messagebox.askokcancel(
                        "File Not Found",
                        "File not found: {0}".format(value_if_allowed),
                        parent=self.master
                    )
                    self.fullpath_var.set("")
                    self.flow_manager('reset')
                    self.manager.not_busy()
                    return False
                except Exception as ex:
                    template = "Set filepath\nAn exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    result = message
                    Step1FileSelection.logger.log(logging.DEBUG, "is_pathname_valid Called. Result: {0}".
                                                  format(result))
                    messagebox.askokcancel(
                        type(ex).__name__,
                        message,
                        parent=self.master
                    )
                    self.fullpath_var.set("")
                    self.flow_manager('reset')
                    self.manager.not_busy()
                    return False
                else:
                    self.ws_list = self.cont.fetch_ws_list()
                    self.ws_sel_cmb.config(values=self.ws_list)
                    self.flow_manager('sel_ws')
                    self.manager.not_busy()
                    return True
            else:
                Step1FileSelection.logger.log(logging.DEBUG,
                                              "set_fullpath: Invalid file extension messagebox called")
                messagebox.askokcancel(
                    "Invalid Extension",
                    "Invalid file extension. Supported extensions include: "
                    ".xlsx, .xlsm, .xlsb, .xltx, .xltm, .xls, .xlt, .xls, .xml, .xml, .xlam, .xla, .xlw, .xlr,",
                    parent=self.master
                )
                self.fullpath_var.set("")
                self.flow_manager('reset')
                self.manager.not_busy()
                return False
        else:
            self.flow_manager('reset')
            self.manager.not_busy()
            return True

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_last_row(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type,
                          widget_name):
        self.manager.busy()
        if value_if_allowed != "":
            if str.isdigit(value_if_allowed):
                if value_if_allowed != 0:
                    Step1FileSelection.logger.log(logging.NOTSET, "Called: {0}".format(str(value_if_allowed)))
                    try:
                        self.cont.set_last_row(value_if_allowed)
                    except Exception as ex:
                        template = "Set last row: An exception of type {0} occured. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        result = message
                        Step1FileSelection.logger.log(logging.DEBUG, "validate_last_row Called. Result: {0}".
                                                      format(result))
                        messagebox.askokcancel(
                            type(ex).__name__,
                            message,
                            parent=self.master
                        )
                        self.cont.set_last_row(None)
                        self.last_row_var.set("")
                        self.manager.not_busy()
                        return False
                    else:
                        return True
                else:
                    Step1FileSelection.logger.log(logging.ERROR, "Called with 0 value. No action taken.")
                    messagebox.askokcancel(
                        "Invalid Last Row Entry",
                        "The last row value cannot be 0.",
                        parent=self.master
                    )
                    self.cont.set_last_row(None)
                    self.last_row_var.set("")
                    self.manager.not_busy()
                    return False
            else:
                messagebox.askokcancel(
                    "Invalid Last Row Entry",
                    "The last row value must be an integer.",
                    parent=self.master
                )
                self.cont.set_last_row(None)
                self.last_row_var.set("")
                self.manager.not_busy()
                return False
        else:
            self.cont.set_last_row(None)
            self.manager.not_busy()
            return False

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_last_col(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type,
                          widget_name):
        self.manager.busy()
        if value_if_allowed != "":
            if str.isdigit(value_if_allowed):
                if value_if_allowed != 0:
                    Step1FileSelection.logger.log(logging.NOTSET, "Called: {0}".format(str(value_if_allowed)))
                    try:
                        self.cont.set_last_col(value_if_allowed)
                    except Exception as ex:
                        template = "Set last col: An exception of type {0} occured. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        result = message
                        Step1FileSelection.logger.log(logging.DEBUG, "validate_last_col Called. Result: {0}".
                                                      format(result))
                        messagebox.askokcancel(
                            type(ex).__name__,
                            message,
                            parent=self.master
                        )
                        self.cont.set_last_col(None)
                        self.last_col_var.set("")
                        self.manager.not_busy()
                        return False
                    else:
                        return True
                else:
                    Step1FileSelection.logger.log(logging.ERROR, "Called with 0 value. No action taken.")
                    messagebox.askokcancel(
                        "Invalid Last Col Entry",
                        "The last col value cannot be 0.",
                        parent=self.master
                    )
                    self.cont.set_last_col(None)
                    self.last_col_var.set("")
                    self.manager.not_busy()
                    return False
            else:
                messagebox.askokcancel(
                    "Invalid Last Col Entry",
                    "The last col value must be an integer.",
                    parent=self.master
                )
                self.cont.set_last_col(None)
                self.last_col_var.set("")
                self.manager.not_busy()
                return False
        else:
            self.cont.set_last_col(None)
            self.manager.not_busy()
            return False







