from cep_price_console.utils.log_utils import CustomAdapter, debug
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import logging
import os
import pathlib


class FileSelection(ttk.Frame):
    acceptable_ext = ['.xlsx', '.xls']
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        self.initial = True
        self.terminal = False
        self.view = view
        # noinspection PyArgumentList
        super().__init__(self.view, style="even.group.TFrame", padding=5, relief=tk.RIDGE, *args, **kwargs)
        self.columnconfigure(0, weight=1)

        self.header = ttk.Label(self,
                                text="Step 1: Contract Filename",
                                style="even.heading2.TLabel")
        self.header.grid(row=0, column=0, sticky=tk.W, columnspan=2)

        self.instr_sep = ttk.Separator(self)
        self.instr_sep.grid(row=1, column=0, sticky=tk.EW, columnspan=2)

        self.inst = ttk.Label(self, anchor=tk.NW, justify=tk.LEFT)
        instr = (
            " a) Select the workbook in question by clicking 'Browse', or by pasting the full filepath in the"
            "textbox. \n"
            "   - Browsing for the file is recommended. \n"
            "   - Only .xls and .xlsx formats are permitted at this time. If the target file is in a different format, "
            "open it in Excel and save it as an .xlsx file."
        )
        self.inst.config(text=instr, style="even.notes.TLabel", wraplength=20)  # TODO: Write notes
        self.inst.grid(row=2, column=0, sticky=tk.W, columnspan=2)

        self.instr_sep_2 = ttk.Separator(self)
        self.instr_sep_2.grid(row=3, column=0, sticky=tk.EW, columnspan=2)

        # region Contract Upload Filename  #############################################################################
        self.fullpath_var = tk.StringVar(name="Workbook Fullpath")

        fullpath_validation = (self.register(self.validate_fullpath),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.filename_entry = ttk.Entry(self,
                                        textvariable=self.fullpath_var,
                                        validate='focusout',
                                        validatecommand=fullpath_validation)
        self.filename_entry.grid(row=4, column=0, sticky=tk.EW)

        self.filename_btn = ttk.Button(self,
                                       text="Browse",
                                       command=self.file_dialog)
        self.filename_btn.grid(row=4, column=1, sticky=tk.E)

        self.bind("<Configure>", self.on_resize)

        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_remove()

    @debug(lvl=logging.DEBUG, prefix='')
    def open(self):
        self.fullpath_var.set(self.view.wb_filename)
        self.grid()

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        self.grid_remove()

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.inst.configure(wraplength=self.winfo_width())

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
                        return False
                    else:
                        try:
                            self.view.wb_filename = path_obj.resolve()
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
                            return False
                        else:
                            return True
                else:
                    messagebox.askokcancel(
                        "File Not Found",
                        "File not found: {0}".format(value_if_allowed),
                        parent=self.view
                    )
                    return False
            else:
                FileSelection.logger.log(logging.DEBUG, "set_fullpath: Invalid file extension messagebox called")
                messagebox.askokcancel(
                    "Invalid Extension",
                    "Invalid file extension. Supported extensions include: {ext_list}".format(
                        ext_list=FileSelection.acceptable_ext
                    ), parent=self.view)
                return False
        else:
            return True

    @debug(lvl=logging.DEBUG, prefix='')
    def file_dialog(self):
        filename_options = dict(
            title='Select Worksheet',
            initialdir=os.path.expanduser('~'),
            initialfile=None,
            parent=self.view,
            filetypes=[('Excel Files', FileSelection.acceptable_ext)]
        )
        self.fullpath_var.set(tk.filedialog.askopenfilename(**filename_options))
        self.filename_entry.validate()
