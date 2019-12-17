from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
from cep_price_console.old_unified_upload.step import Step
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import pathlib
import logging
import os

# TODO: Include the ability to define the quoting character, pass it to the model for the import_sql function


class FileSelection(Step):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    acceptable_ext = ['.xlsx', '.xls']
    vendor_default = "Select Vendor"

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, *args, **kwargs):
        super().__init__(namely=str(FileSelection.__name__), order=1, *args, **kwargs)
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.rowconfigure(1, weight=1)
        self.frame_main.rowconfigure(2, weight=1)
        self.file_selection_hdr = ttk.Label(self.frame_main)
        self.file_selection_hdr.config(text="File Selection", style="heading1.TLabel")
        self.file_selection_hdr.grid(row=0, column=0, sticky=tk.NW)

        # region Input Frame  ##########################################################################################
        input_style = "even"
        self.input_frame = ttk.Frame(self.frame_main)
        self.input_frame.configure(padding=5, style=input_style+".group.TFrame")
        self.input_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.input_header = ttk.Label(self.input_frame)
        self.input_header.config(text="Input Selection", style=input_style+".heading2.TLabel")
        self.input_header.grid(row=0, column=0, sticky=tk.W, columnspan=2)

        self.input_instr_sep = ttk.Separator(self.input_frame)
        self.input_instr_sep.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

        self.input_inst = ttk.Label(self.input_frame, anchor=tk.NW, justify=tk.LEFT)
        instr = "Step 1: Select the workbook in question by clicking 'Browse', or by pasting the full filepath in " \
                "the Step 1 textbox. \n\t(Browsing for the file is recommended.) Only .xls and .xlsx formats are " \
                "permitted at this time. If the \n\ttarget file is in a different format, open it in Excel and save " \
                "it as an .xlsx file. \nStep 2: Use the combobox under Step 2 to select the correct worksheet to " \
                "load data from.  \nStep 3: The values on this row will be used to make columnar distinctions in " \
                "the next step."
        self.input_inst.config(text=instr, style=input_style+".notes.TLabel")  # TODO: Write notes
        self.input_inst.grid(row=2, column=0, sticky=tk.W, columnspan=2)

        self.input_instr_sep = ttk.Separator(self.input_frame)
        self.input_instr_sep.grid(row=3, column=0, columnspan=2, sticky=tk.EW)

        # region Contract Upload Filename  #############################################################################
        self.filename_frame = ttk.Frame(self.input_frame)
        self.filename_frame.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
        self.filename_frame.columnconfigure(0, weight=1)

        self.filename_lbl = ttk.Label(self.filename_frame)
        self.filename_lbl.config(text="Step 1: Contract Filename", style=input_style+".heading3.TLabel")
        # TODO: Write heading 3 style
        self.filename_lbl.grid(row=0, column=0, columnspan=2, sticky=tk.EW)

        self.fullpath_var = tk.StringVar(name="Workbook Fullpath")

        self.filename_entry = ttk.Entry(self.filename_frame)
        fullpath_validation = (self.filename_frame.register(self.validate_fullpath),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.filename_entry.config(textvariable=self.fullpath_var,
                                   validate='focusout',
                                   validatecommand=fullpath_validation)
        self.filename_entry.grid(row=1, column=0, sticky=tk.EW)

        self.filename_btn = ttk.Button(self.filename_frame)
        self.filename_btn.config(text="Browse", command=self.file_dialog)
        self.filename_btn.grid(row=1, column=1, sticky=tk.E)

        self.filename_focus = False
        # endregion ####################################################################################################

        # region Contract Details Worksheet  ###########################################################################
        self.ws_list = []
        self.ws_sel_frame = ttk.Frame(self.input_frame)
        self.ws_sel_frame.grid(row=5, column=0, sticky=tk.NSEW)
        self.ws_sel_frame.columnconfigure(0, weight=1)

        self.ws_sel_lbl = ttk.Label(self.ws_sel_frame)
        self.ws_sel_lbl.config(text="Step 2: Contract Details Worksheet", style=input_style+".heading3.TLabel")
        self.ws_sel_lbl.grid(row=0, column=0, sticky=tk.EW)

        self.ws_sel_var = tk.StringVar(name="Worksheet Selection")
        self.ws_sel_var.trace_add('write', self.set_ws_sel)

        self.ws_sel_cmb = ttk.Combobox(self.ws_sel_frame, state="readonly")
        self.ws_sel_cmb.config(textvariable=self.ws_sel_var)
        self.ws_sel_cmb.grid(row=1, column=0, sticky=tk.EW)
        # endregion ####################################################################################################

        # region Header Row  ###########################################################################################
        self.header_row_frame = ttk.Frame(self.input_frame)
        self.header_row_frame.grid(row=5, column=1, sticky=tk.NSEW)
        self.header_row_frame.columnconfigure(0, weight=1)

        self.header_row_lbl = ttk.Label(self.header_row_frame)
        self.header_row_lbl.config(text="Step 3: Header Row", style=input_style+".heading3.TLabel")
        self.header_row_lbl.grid(row=0, column=0, columnspan=2, sticky=tk.EW)

        self.header_row_var = tk.IntVar(name="Header Row")
        self.header_row_var.trace_add('write', self.set_header_row)

        self.header_row_entry = ttk.Entry(self.header_row_frame)
        header_validation = (self.header_row_frame.register(self.validate_header_row),
                             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.header_row_entry.config(textvariable=self.header_row_var,
                                     validate='focusout',
                                     validatecommand=header_validation)
        self.header_row_entry.grid(row=1, column=0, sticky=tk.EW)
        # endregion ####################################################################################################
        # endregion ####################################################################################################

        # region Parameters Frame  #####################################################################################
        self.param_style = "odd"
        self.param_frame = ttk.Frame(self.frame_main)
        self.param_frame.configure(padding=5, style=self.param_style+".group.TFrame")
        self.param_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.param_header = ttk.Label(self.param_frame)
        self.param_header.config(text="Parameter Selection", style=self.param_style+".heading2.TLabel")
        self.param_header.grid(row=0, column=0, sticky=tk.W, columnspan=5)

        self.param_hdr_sep = ttk.Separator(self.param_frame)
        self.param_hdr_sep.grid(row=1, column=0, sticky=tk.EW, columnspan=5)

        instr = "These are instructions"

        self.param_inst = ttk.Label(self.param_frame)
        self.param_inst.config(text=instr, style=self.param_style+".notes.TLabel")
        self.param_inst.grid(row=2, column=0, sticky=tk.W, columnspan=5)

        self.param_inst_sep = ttk.Separator(self.param_frame)
        self.param_inst_sep.grid(row=3, column=0, sticky=tk.EW, columnspan=5)

        self.all_prim_chk_box = ttk.Checkbutton(self.param_frame)
        self.all_prim_chk_box.grid(row=2, column=1, sticky=tk.W)
        self.all_prim_chk_box.config(text="All Primary",
                                     command=self.all_primary,
                                     style=self.param_style+".dflt.TCheckbutton")
        self.all_prim_chk_box.state(['!alternate', '!selected'])

        self.all_vend_chk_box = ttk.Checkbutton(self.param_frame)
        self.all_vend_chk_box.grid(row=2, column=2, sticky=tk.W)
        self.all_vend_chk_box.config(text="All Vendors",
                                     command=self.all_vendors,
                                     style=self.param_style+".dflt.TCheckbutton")
        self.all_vend_chk_box.state(['!alternate', '!selected'])

        self.param_add_btn = ttk.Button(self.param_frame)
        self.param_add_btn.config(text="Add Parameter", command=self.add_param)
        self.param_add_btn.grid(row=2, column=3, sticky=tk.E)

        self.__param_row = 3
        # endregion ####################################################################################################
        self.btn_prev.grid_forget()
        self.match_mode = None
        self.flow_manager()
        # self.testing()

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def param_row(self):
        self.__param_row += 1
        return self.__param_row

    @debug(lvl=logging.DEBUG, prefix='')
    def all_primary(self):
        ParameterSelection.empty_list()
        self.all_vend_chk_box.state(['!selected'])
        self.flow_manager()

    @debug(lvl=logging.DEBUG, prefix='')
    def all_vendors(self):
        ParameterSelection.empty_list()
        self.all_prim_chk_box.state(['!selected'])
        self.flow_manager()

    @debug(lvl=logging.DEBUG, prefix='')
    def opt_list(self):
        listy = self.view.model.fetch_vendors()
        if ParameterSelection.param_list:
            for param in ParameterSelection.param_list:
                if param.var.get() != FileSelection.vendor_default:
                    listy.remove(param.var.get())
            for param in ParameterSelection.param_list:
                param.combobox.config(values=listy)
        return listy

    @debug(lvl=logging.DEBUG, prefix='')
    def file_dialog(self):
        # self.manager.busy() # TODO: Do I need a manager?
        filename_options = dict(
            title='Select Worksheet',
            initialdir=os.path.expanduser('~'),
            initialfile=None,
            parent=self.view,
            filetypes=[('Excel Files', FileSelection.acceptable_ext)]
        )
        self.fullpath_var.set(tk.filedialog.askopenfilename(**filename_options))
        self.filename_entry.validate()
        # self.manager.not_busy() # TODO: Do I need a manager?

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
        # self.manager.busy() # TODO: Do I need a manager?
        if value_if_allowed != "":
            path_obj = pathlib.Path(value_if_allowed)
            if len(path_obj.suffixes) == 1 and path_obj.suffix in FileSelection.acceptable_ext:
                FileSelection.logger.log(logging.DEBUG,
                                         "set_fullpath called. Filepath valid. Extension valid. Filepath: {0}".format(
                                             value_if_allowed))
                if path_obj.exists() and path_obj.is_file():
                    try:
                        path_obj.resolve()
                    except FileExistsError:
                        messagebox.askokcancel(
                            "File Not Found",
                            "File not found: {0}".format(value_if_allowed),
                            parent=self.view
                        )
                        self.view.model.wb_filename_obj = ""
                        self.flow_manager()
                        # self.manager.not_busy() # TODO: Do I need a manager?
                        return False
                    except Exception as ex:
                        template = "Set filepath\nAn exception of type {0} occured. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        FileSelection.logger.log(logging.DEBUG,
                                                 "is_pathname_valid Called. Result: {0}".format(message))
                        messagebox.askokcancel(
                            type(ex).__name__,
                            message,
                            parent=self.view
                        )
                        self.view.model.wb_filename_obj = ""
                        self.flow_manager()
                        # self.manager.not_busy() # TODO: Do I need a manager?
                        return False
                    else:
                        try:
                            self.view.model.wb_filename_obj = path_obj
                        except Exception as ex:
                            template = "Set filepath\nAn exception of type {0} occured. Arguments:\n{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            FileSelection.logger.log(logging.DEBUG,
                                                     "is_pathname_valid Called. Result: {0}".format(message))
                            messagebox.askokcancel(
                                type(ex).__name__,
                                message,
                                parent=self.view
                            )
                            self.view.model.wb_filename_obj = ""
                            self.flow_manager()
                            # self.manager.not_busy() # TODO: Do I need a manager?
                            return False
                        else:
                            self.view.model.ws_name = ""
                            self.view.model.header_row = 0
                            self.ws_sel_cmb.config(values=self.view.model.wb.sheet_names())
                            self.flow_manager()
                            # self.manager.not_busy() # TODO: Do I need a manager?
                            return True
                else:
                    messagebox.askokcancel(
                        "File Not Found",
                        "File not found: {0}".format(value_if_allowed),
                        parent=self.view
                    )
                    self.view.model.wb_filename_obj = ""
                    self.flow_manager()
                    # self.manager.not_busy() # TODO: Do I need a manager?
                    return False
            else:
                FileSelection.logger.log(logging.DEBUG, "set_fullpath: Invalid file extension messagebox called")
                messagebox.askokcancel(
                    "Invalid Extension",
                    "Invalid file extension. Supported extensions include: {ext_list}".format(
                        ext_list=FileSelection.acceptable_ext),
                    parent=self.view
                )
                self.view.model.wb_filename_obj = ""
                self.flow_manager()
                # self.manager.not_busy() # TODO: Do I need a manager?
                return False
        else:
            self.view.model.wb_filename_obj = ""
            self.flow_manager()
            # self.manager.not_busy() # TODO: Do I need a manager?
            return True

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def set_ws_sel(self, *args):
        # self.manager.busy()  # TODO: Do I need a manager?
        if self.ws_sel_var.get() != "":
            if self.ws_sel_var.get() != self.view.model.ws_name:
                self.view.model.ws_name = self.ws_sel_var.get()
                self.view.model.header_row = 0
                self.flow_manager()
        else:
            self.view.model.ws_name = ""
        # self.manager.not_busy()  # TODO: Do I need a manager?

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
                         widget_name,
                         variable):
        # self.manager.busy()  # TODO: Do I need a manager?
        if value_if_allowed != 0:
            try:
                int_value = int(value_if_allowed)
            except ValueError:
                messagebox.askokcancel(
                    "Invalid {0}".format(variable._name),
                    "The {0} value must be an integer.".format(variable._name),
                    parent=self.view
                )
                variable.set("")
                # self.manager.not_busy()  # TODO: Do I need a manager?
                return False
            else:
                if int_value != 0:
                    return True
                else:
                    FileSelection.logger.log(logging.ERROR, "Called with 0 value. No action taken.")
                    messagebox.askokcancel(
                        "Invalid {0}".format(variable._name),
                        "The {0} value cannot be 0.".format(variable._name),
                        parent=self.view
                    )
                    variable.set("")
                    # self.manager.not_busy()  # TODO: Do I need a manager?
                    return False
        else:
            # self.manager.not_busy()  # TODO: Do I need a manager?
            return False

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_header_row(self,
                            action,
                            index,
                            value_if_allowed,
                            prior_value,
                            text,
                            validation_type,
                            trigger_type,
                            widget_name):
        return self.validate_integer(action,
                                     index,
                                     value_if_allowed,
                                     prior_value,
                                     text,
                                     validation_type,
                                     trigger_type,
                                     widget_name,
                                     variable=self.header_row_var)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def set_header_row(self, *args):
        # self.manager.not_busy()  # TODO: Do I need a manager?
        try:
            value = self.header_row_var.get()
        except tk.TclError:
            FileSelection.logger.log(logging.NOTSET, "Called. Value wasn't an integer. No action taken.")
        else:
            if self.header_row_var.get() != 0:
                try:
                    self.view.model.header_row = self.header_row_var.get()
                    self.flow_manager()
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    # noinspection PyProtectedMember
                    FileSelection.logger.log(logging.DEBUG,
                                             "{0} Called. Result: {1}".format(self.header_row_var._name, message))
                    messagebox.askokcancel(
                        type(ex).__name__,
                        message,
                        parent=self.view
                    )
                    self.header_row_var.set(0)
                    self.flow_manager()
        # self.manager.not_busy()  # TODO: Do I need a manager?

    @debug(lvl=logging.DEBUG, prefix='')
    def flow_manager(self):
        if self.view.model.wb_filename_obj == "":
            self.fullpath_var.set("")
        else:
            self.fullpath_var.set(self.view.model.wb_filename_obj.resolve())
        self.ws_sel_var.set(self.view.model.ws_name)
        self.header_row_var.set(self.view.model.header_row)

        FileSelection.logger.log(
            logging.DEBUG,
            "Flow Manager: \n\t"
            "Fullpath: {fullpath}\n\t"
            "Worksheet: {ws} \n\t"
            "Header Row: {header} ".format(fullpath=self.fullpath_var.get(),
                                           ws=self.ws_sel_var.get(),
                                           header=self.header_row_var.get()))
        if self.fullpath_var.get() == "":
            self.ws_sel_var.set("")
            self.ws_sel_cmb.config(value="")
            self.ws_sel_cmb.state(['disabled'])
            self.header_row_var.set(0)
            self.header_row_entry.state(['disabled'])
            self.btn_next.state(['disabled'])
        else:
            self.fullpath_var.set(self.view.model.wb_filename_obj.resolve())
            self.ws_sel_cmb.state(['!disabled'])
            self.ws_sel_cmb.config(values=self.view.model.wb.sheet_names())

            if self.ws_sel_var.get() == "":
                self.header_row_var.set(0)
                self.header_row_entry.state(['disabled'])
                self.btn_next.state(['disabled'])
            else:
                self.ws_sel_var.set(self.view.model.ws_name)
                self.header_row_entry.state(['!disabled'])

                if self.header_row_var.get() == 0:
                    self.btn_next.state(['disabled'])
                else:
                    all_sel = []
                    if ParameterSelection.param_list:
                        for param in ParameterSelection.param_list:
                            if param.var.get() != ParameterSelection.vendor_default:
                                if 'selected' in param.prim_chk_box.state() or 'selected' in param.sec_chk_box.state():
                                    all_sel.append(param.var.get())
                                else:
                                    self.btn_next.state(['disabled'])
                                    return
                    if 'selected' in self.all_vend_chk_box.state():
                        all_sel.extend(self.opt_list())
                    if 'selected' in self.all_prim_chk_box.state():
                        all_sel.extend(self.opt_list())
                    if not all_sel:
                        self.btn_next.state(['disabled'])
                    else:
                        self.btn_next.state(['!disabled'])

    @debug(lvl=logging.DEBUG, prefix='')
    def testing(self):
        self.fullpath_var.set(config.MEDIA_PATH / "LAGB_02-25-2019_test3.xlsx")
        self.filename_entry.validate()
        self.ws_sel_cmb.set('ESSENDANT FEBRUARY')
        self.header_row_var.set(1)
        self.header_row_entry.validate()
        vendor = ParameterSelection(master=self, main_frame=self.param_frame, style_prefix=self.param_style)
        vendor.var.set("00374__ESSENDANT COMPANY LLC")
        vendor.mode()
        vendor.sec_chk_box.state(['selected'])
        self.flow_manager()
        self.btn_next.state(['selected'])
        self.btn_next.invoke()

    @debug(lvl=logging.DEBUG, prefix='')
    def next(self, *args):
        self.complete = True

        self.view.model.all_primary_vend = False
        if 'selected' in self.all_prim_chk_box.state():
            self.view.model.all_primary_vend = True

        self.view.model.all_vend_chk_box = False
        if 'selected' in self.all_vend_chk_box.state():
            self.view.model.all_vend_chk_box = True

        self.view.model.sel_list = []
        if ParameterSelection.param_list:
            self.view.model.sel_list = ParameterSelection.param_list
        self.view.flow_manager()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def add_param(self, *args):
        self.all_vend_chk_box.state(['!selected'])
        self.all_prim_chk_box.state(['!selected'])
        ParameterSelection(master=self, main_frame=self.param_frame, style_prefix=self.param_style)
        self.flow_manager()


class ParameterSelection(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    vendor_default = "Select Vendor"
    param_list = []

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, main_frame, style_prefix):
        self.master = master
        self.row = self.master.param_row
        self.main_frame = main_frame
        # self.selection = None

        self.var = tk.StringVar()
        self.var.set(FileSelection.vendor_default)
        self.var.trace_add('write', self.mode)

        self.combobox = ttk.Combobox(self.main_frame, state="readonly")
        self.combobox.grid(row=self.row, column=0)
        self.combobox.config(textvariable=self.var, values=self.master.opt_list(), width=50)

        self.prim_chk_box = ttk.Checkbutton(self.main_frame)
        self.prim_chk_box.grid(row=self.row, column=1, sticky=tk.W)
        self.checkbox_style = style_prefix+".dflt.TCheckbutton"
        self.prim_chk_box.config(text="Primary", command=self.mode, style=self.checkbox_style)
        self.prim_chk_box.state(['!alternate', '!selected'])

        self.sec_chk_box = ttk.Checkbutton(self.main_frame)
        self.sec_chk_box.grid(row=self.row, column=2, sticky=tk.W)
        self.sec_chk_box.config(text="Secondary", command=self.mode, style=self.checkbox_style)
        self.sec_chk_box.state(['!alternate', '!selected'])

        # TODO: return exclude checkbox
        # self.exc_chk_box = ttk.Checkbutton(self.main_frame)
        # self.exc_chk_box.grid(row=self.row, column=3, sticky=tk.W)
        # self.exc_chk_box.config(text="Exclude", command=self.mode, style=style_prefix+".dflt.TCheckbutton")
        # self.exc_chk_box.state(['!alternate', '!selected'])

        self.mode()
        ParameterSelection.param_list.append(self)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def mode(self, *args):
        # self.combobox.state(['!disabled'])
        # self.prim_chk_box.state(['!disabled'])
        # self.sec_chk_box.state(['!disabled'])
        if self.var.get() == ParameterSelection.vendor_default:
            self.prim_chk_box.config(style=self.checkbox_style)
            self.prim_chk_box.state(['disabled', '!selected', '!alternate'])
            self.sec_chk_box.config(style=self.checkbox_style)
            self.sec_chk_box.state(['disabled', '!selected', '!alternate'])
        elif self.var.get() != ParameterSelection.vendor_default:
            self.prim_chk_box.state(['!disabled', '!alternate'])
            self.sec_chk_box.state(['!disabled', '!alternate'])

            if 'selected' in self.prim_chk_box.state() or 'selected' in self.sec_chk_box.state():
                if 'selected' in self.prim_chk_box.state():
                    if 'hover' in self.prim_chk_box.state():
                        self.prim_chk_box.config(style=self.checkbox_style)
                        self.prim_chk_box.state(['!alternate'])
                        self.sec_chk_box.config(style=self.checkbox_style)
                        self.sec_chk_box.state(['!selected', '!alternate'])
                if 'selected' in self.sec_chk_box.state():
                    if 'hover' in self.sec_chk_box.state():
                        self.sec_chk_box.config(style=self.checkbox_style)
                        self.sec_chk_box.state(['!alternate'])
                        self.prim_chk_box.config(style=self.checkbox_style)
                        self.prim_chk_box.state(['!selected', '!alternate'])
            elif 'selected' not in self.prim_chk_box.state() and 'selected' not in self.sec_chk_box.state():
                self.prim_chk_box.config(style="bad.dflt.TCheckbutton")
                self.prim_chk_box.state(['!selected', '!alternate'])
                self.sec_chk_box.config(style="bad.dflt.TCheckbutton")
                self.sec_chk_box.state(['!selected', '!alternate'])
        self.master.flow_manager()

    @classmethod
    @debug(lvl=logging.DEBUG, prefix='')
    def empty_list(cls):
        for param in cls.param_list:
            param.var.set(ParameterSelection.vendor_default)
            param.combobox.grid_forget()
            param.prim_chk_box.grid_forget()
            param.sec_chk_box.grid_forget()
            # param.exc_chk_box.grid_forget()
        cls.param_list = []
