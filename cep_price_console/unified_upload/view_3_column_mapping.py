from cep_price_console.utils.mypandastable import MyTable
from cep_price_console.utils.gui_utils import VerticalScrolledFrame
from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.unified_upload.step import Step
from cep_price_console.unified_upload.model import Function
from cep_price_console.unified_upload.treeview import TreeviewConstructor
import tkinter as tk
import tkinter.ttk as ttk
import logging
from pandastable import TableModel
import pandas as pd

"""
You shouldn't be using a paned window for the column entries. Turn the column label into an entry that is pre-populated 
with the current column name. Link a change in the column name to a change to the pandas column. Link a deletion of a 
column mapper to a deletion of the pandas column. Get rid of those options on the mypandastable subclass


DDI Warehouse Connection Properties
username: CEP\ddiadmin
servername: DDI-SERVER\SQLEXPRESS
Collation: SQL_Latin1_General_CP1_CI_AS
IPAll: 64374
"""


class ColumnSelection(ttk.Frame):
    acceptable_ext = ['.xlsx', '.xls']
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        self.mapper_dict = None
        self.initial = False
        self.terminal = False
        self.view = view
        # noinspection PyArgumentList
        super().__init__(self.view, style="even.group.TFrame", padding=5, relief=tk.RIDGE, *args, **kwargs)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.header = ttk.Label(self,
                                text="Step 3: Column Mapping",
                                style="even.heading2.TLabel")
        self.header.grid(row=0, column=0, sticky=tk.W)

        self.instr_sep = ttk.Separator(self)
        self.instr_sep.grid(row=1, column=0, sticky=tk.EW)

        self.inst = ttk.Label(self, anchor=tk.NW, justify=tk.LEFT)
        instr = (
            " - a) Select the workbook in question by clicking 'Browse', or by pasting the full filepath in the"
            "textbox. \n"
            "   - Browsing for the file is recommended. \n"
            "   - Only .xls and .xlsx formats are permitted at this time. If the target file is in a different format, "
            "open it in Excel and save it as an .xlsx file."
        )
        self.inst.config(text=instr, style="even.notes.TLabel", wraplength=20)  # TODO: Write notes
        self.inst.grid(row=2, column=0, sticky=tk.W)

        self.instr_sep_2 = ttk.Separator(self)
        self.instr_sep_2.grid(row=3, column=0, sticky=tk.EW)

        self.paned_outer = tk.PanedWindow(self,
                                          orient=tk.HORIZONTAL,
                                          name="paned_outer",
                                          sashrelief=tk.RAISED,
                                          sashwidth=7)

        self.paned_outer.grid(row=4, column=0, sticky=tk.NSEW)

        self.mapping_paned_frame = VerticalScrolledFrame(self.paned_outer, padding=5, relief=tk.RIDGE)
        self.mapping_paned_frame.interior.columnconfigure(0, weight=1)
        self.mapping_paned_frame.interior.rowconfigure(0, weight=1)

        self.mapping_paned_window = tk.PanedWindow(
            self.mapping_paned_frame.interior,
            orient=tk.VERTICAL,
            name="mapping_pane",
            sashrelief=tk.FLAT,
            sashwidth=5
        )

        self.mapping_paned_window.grid(row=0, column=0, sticky=tk.NSEW)

        self.paned_outer.add(self.mapping_paned_frame,
                             sticky=tk.NSEW,
                             width=480,
                             pady=5,
                             padx=5,
                             stretch="never")

        self.table_frame = ttk.Frame(self.paned_outer,
                                     padding=5,
                                     relief=tk.RIDGE)

        self.paned_outer.add(self.table_frame,
                             sticky=tk.NSEW,
                             # width=480,
                             pady=5,
                             padx=5)

        self.table = MyTable(self.table_frame, showtoolbar=False, showstatusbar=True)
        self.unbind_all("<KP_8>")
        self.unbind_all("<Return>")
        self.unbind_all("<Tab>")
        self.table.show()
        self.model = None
        self.bind("<Configure>", self.on_resize)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_remove()

    @debug(lvl=logging.DEBUG, prefix='')
    def open(self):
        if self.view.column_mapping_dataframe is None:
            self.model = TableModel(
                dataframe=pd.read_excel(
                    io=self.view.wb_filename,
                    header=self.view.header_row - 1,
                    sheet_name=self.view.ws_name_selection
                )
            )

            self.mapper_dict = {}
            for column_name in self.model.df.columns.values.tolist():
                self.mapper_dict[column_name] = ColumnMapper(
                    master_frame=self,
                    paned_frame=self.mapping_paned_window,
                    col_name=column_name
                )
            for obj in self.mapper_dict.values():
                self.mapping_paned_window.add(
                    obj,
                    minsize=30,
                    stretch="never"
                )
        else:
            self.model = self.view.column_mapping_dataframe
        self.table.updateModel(self.model)
        self.table.statusbar.update()
        self.bind_all("<KP_8>", self.table.handle_arrow_keys)
        self.bind_all("<Return>", self.table.handle_arrow_keys)
        self.bind_all("<Tab>", self.table.handle_arrow_keys)
        self.grid()

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        self.view.column_mapping_dataframe = self.table.model
        self.unbind_all("<KP_8>")
        self.unbind_all("<Return>")
        self.unbind_all("<Tab>")
        self.grid_remove()

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.inst.configure(wraplength=self.winfo_width())


class ColumnMapping(Step):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        super().__init__(namely=str(ColumnMapping.__name__), order=2, view=view, *args, **kwargs)
        self.upload_query = None
        # self.__option_list = None  # TODO: What's this?
        self.frame_main.columnconfigure(1, weight=1)
        self.frame_main.rowconfigure(1, weight=1)

        self.column_mapping_hdr = ttk.Label(self.frame_main)
        self.column_mapping_hdr.config(text="Column Mapping", style="heading1.TLabel")
        self.column_mapping_hdr.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.treeview = TreeviewConstructor(self.frame_main)
        self.__class__.logger.log(logging.DEBUG, "Done!")
        self.treeview.grid(row=1,
                           column=1,
                           sticky=tk.NSEW)

        self.canvas_frame = ttk.Frame(self.frame_main, padding=2)
        self.canvas_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)

        self.column_mapping_frame = ttk.Frame(self.canvas)
        self.column_mapping_frame.update_idletasks()
        self.column_mapping_frame.configure(padding=5, style="even.group.TFrame")
        self.column_mapping_frame.columnconfigure(0, weight=1)
        self.column_mapping_frame.rowconfigure(0, weight=1)
        self.canvas.create_window((0, 0),
                                  window=self.column_mapping_frame,
                                  anchor=tk.NW,
                                  tags="column_mapping_frame")

        self.filler_frame = ttk.Frame(self.canvas_frame)
        self.filler_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.ysb = ttk.Scrollbar(self.canvas_frame)
        self.ysb.config(orient=tk.VERTICAL, command=self.canvas.yview)
        self.ysb.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.configure(yscrollcommand=self.ysb.set, borderwidth=2, highlightthickness=0)

        self.col_mapping_instr_lbl = ttk.Label(self.column_mapping_frame)
        self.col_mapping_instr_lbl.config(text="These are the instructions on how to do this thing. \n"
                                               "1) You need to do something. \n"
                                               "2) You need to do something else. \n"
                                               "3) Finally, you need to do something else. \n"
                                               "Then you are done!")
        self.col_mapping_instr_lbl.grid(row=0, column=0)

        self.reset = ttk.Button(self.frame_cmd)
        self.reset.config(text="Reset Comboboxes")  # command=self.reset_combo_boxes)  # TODO: write function
        self.reset.grid(row=0, column=0)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        self.upload_query = self.view.model.upload_query()
        self.treeview.populate_query(query=self.upload_query, hide_list=None, id_col="line_number", limit=30)
        for col_obj in sorted(self.treeview.col_obj_dict.values(), key=lambda x: x.order):
            if col_obj.order != 0:
                ColumnMapper(master=self,
                             parent_frame=self.column_mapping_frame,
                             grid_row=col_obj.order,
                             desc=col_obj.desc)
        self.update_option_list()
        self.column_mapping_frame.update_idletasks()
        self.canvas.itemconfigure("column_mapping_frame",
                                  height=self.column_mapping_frame.winfo_reqheight(),
                                  width=self.column_mapping_frame.winfo_reqwidth())
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL),
                           width=self.column_mapping_frame.winfo_reqwidth(),
                           height=self.column_mapping_frame.winfo_reqwidth())
        # self.testing()

    @debug(lvl=logging.DEBUG, prefix='')
    def proceed_logic(self):
        func_obj = Function.func_dict.get("Vendor Part Number")
        if func_obj is not None:
            self.btn_next.state(['!disabled'])
        else:
            self.btn_next.state(['disabled'])

    @debug(lvl=logging.DEBUG, prefix='')
    def update_option_list(self):
        opt_list = [ColumnMapper.function_default]
        for func in Function.func_dict.values():
            if func.field_desc is None:
                opt_list.append(func.name)
        for colmapper in ColumnMapper.col_mapper_dict.values():
            colmapper.function_combo.config(values=opt_list)

    @debug(lvl=logging.DEBUG, prefix='')
    def testing(self):
        ColumnMapper.col_mapper_dict["Action Indicator"].function_var.set("Action Indicator")
        ColumnMapper.col_mapper_dict["Brand Long Name"].function_var.set("Brand")
        ColumnMapper.col_mapper_dict["Cost End Column Price-KANSAS CITY-KAN-17"].function_var.set("C1 Cost")
        ColumnMapper.col_mapper_dict["Item Depth"].function_var.set("Depth")
        ColumnMapper.col_mapper_dict["Description 125 Character"].function_var.set("Description")
        ColumnMapper.col_mapper_dict["Item Height"].function_var.set("Height")
        ColumnMapper.col_mapper_dict["List Price"].function_var.set("L1 Price")
        ColumnMapper.col_mapper_dict["Manufacturer Long Name"].function_var.set("Manufacturer Name")
        ColumnMapper.col_mapper_dict["Manufacturer Part Number"].function_var.set("Manufacturer Part Number")
        ColumnMapper.col_mapper_dict["Manufacturer URL"].function_var.set("Manufacturer URL")
        ColumnMapper.col_mapper_dict["Unit of Measure"].function_var.set("Primary UOM")
        ColumnMapper.col_mapper_dict["Unit of Measure Qty"].function_var.set("Primary UOM Quantity")
        ColumnMapper.col_mapper_dict["Unit within UOM"].function_var.set("Secondary UOM")
        ColumnMapper.col_mapper_dict["UNSPSC"].function_var.set("UNSPSC Code")
        ColumnMapper.col_mapper_dict["UPC Item GTIN"].function_var.set("UPC")
        ColumnMapper.col_mapper_dict["Item Number"].function_var.set("Vendor Part Number")
        ColumnMapper.col_mapper_dict["Item Number Revised"].function_var.set("Vendor Part Number Revision")
        ColumnMapper.col_mapper_dict["Item Cubic Inches"].function_var.set("Volume")
        ColumnMapper.col_mapper_dict["Item Weight"].function_var.set("Weight")
        ColumnMapper.col_mapper_dict["Item Width"].function_var.set("Width")

    @debug(lvl=logging.DEBUG, prefix='')
    def next(self, *args):
        self.complete = True
        self.view.flow_manager()


class ColumnMapper(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    datatypes = []  # TODO: Fill Out
    values = [
        'string',
        'float',
        'integer',
        'date',
        'boolean',
        'error',
        'blank'
    ]
    function_default = "Select Function"
    custom_default = "Enter Custom Header"

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master_frame,
                 paned_frame,
                 col_name,
                 *args,
                 **kwargs):
        self.paned_frame = paned_frame
        # noinspection PyArgumentList
        super().__init__(self.paned_frame, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master_frame = master_frame
        self.col_name = col_name
        self.col_datatype = self.master_frame.model.df[self.col_name].dtype

        self.label = ttk.Label(self, text=self.col_name, style="dflt.TLabel")
        self.label.grid(row=0, column=0, sticky=tk.E)

        # Datatype
        self.datatype_var = tk.StringVar()
        self.datatype_var.set(self.col_datatype)
        self.datatype_var.trace_add('write', self.datatype_var_on_change)

        self.datatype_combo = ttk.Combobox(self,
                                           state="readonly",
                                           values=ColumnMapper.datatypes,
                                           textvariable=self.datatype_var)
        self.datatype_combo.grid(row=0, column=1)
        self.datatype_combo.bind('<<ComboboxSelected>>', self.datatype_combo_on_change)

        # Field Function
        self.function = None
        self.function_var = tk.StringVar()
        self.function_var.set(ColumnMapper.function_default)
        self.function_var.trace_add('write', self.function_var_on_change)

        self.function_combo = ttk.Combobox(self,
                                           state="readonly",
                                           textvariable=self.function_var)
        self.function_combo.grid(row=0, column=2)

        self.close_btn = ttk.Button(self,
                                    text="X",
                                    command=self.remove_frame,
                                    width=3,
                                    style="bad.TButton")
        self.close_btn.grid(row=0, column=3, sticky=tk.E)

        # TODO: Allow user to do custom stuff
        # # Field Custom
        # self.custom_chk_var = tk.IntVar()
        # self.custom_chk_var.set(0)
        #
        # self.custom_chk_box = ttk.Checkbutton(self)
        # self.custom_chk_box.grid(row=0, column=3)
        # self.custom_chk_box.config(variable=self.custom_chk_var,
        #                            command=self.custom_chk_box_toggle)
        #
        # self.custom_var = tk.StringVar()
        # self.custom_var.set(ColumnMapper.custom_default)
        # self.custom_entry = ttk.Entry(self)
        # self.custom_entry.grid(row=0, column=4)
        # self.custom_entry.state(['disabled'])
        # custom_validation = (self.register(self.validate_custom_value),
        #                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        # self.custom_entry.config(textvariable=self.custom_var,
        #                          validate='focusout',
        #                          validatecommand=custom_validation)

    @debug(lvl=logging.DEBUG, prefix='')
    def remove_frame(self):
        self.paned_frame.remove(self)

    @debug(lvl=logging.DEBUG, prefix='')
    def datatype_combo_on_change(self, *args):
        print(*args)  # TODO: Support datatype change

    @debug(lvl=logging.DEBUG, prefix='')
    def datatype_var_on_change(self, *args):
        print(*args)  # TODO: Support datatype change

    @debug(lvl=logging.DEBUG, prefix='')
    def function_var_on_change(self, *args):
        pass
        # if self.function is not None:
        #     self.function.field_desc = None
        # self.function = None
        #
        # if self.function_var != ColumnMapper.function_default:
        #     func_obj = Function.func_dict.get(self.function_var.get())
        #     if func_obj is not None:
        #         self.function = func_obj
        #         self.function.field_desc = self.col_name
        #     else:
        #         self.__class__.logger.log(logging.ERROR, "Function Object Not Found: Function Variable = {0}".format(
        #             self.function_var.get()))
        # self.master.update_option_list()
        # self.master.proceed_logic()

    # @debug(lvl=logging.DEBUG, prefix='')
    # def custom_chk_box_toggle(self, *args):
    #     if self.custom_chk_var.get() == 0:  # Unchecked
    #         self.__class__.logger.log(logging.DEBUG, "Button unchecked")
    #         self.custom_entry.state(['disabled'])
    #         self.custom_var.set(ColumnMapper.custom_default)
    #         self.function_combo.state(['!disabled'])
    #
    #     elif self.custom_chk_var.get() == 1:  # Checked
    #         self.__class__.logger.log(logging.DEBUG, "Button checked")
    #         self.custom_entry.state(['!disabled'])
    #         self.function_combo.state(['disabled'])
    #         self.function_var.set(ColumnMapper.function_default)
    #     else:
    #         self.__class__.logger.log(logging.ERROR, "Button not 0 or 1!")

    # @debug(lvl=logging.DEBUG, prefix='')
    # def validate_custom_value(self,
    #                           action,
    #                           index,
    #                           value_if_allowed,
    #                           prior_value,
    #                           text,
    #                           validation_type,
    #                           trigger_type,
    #                           widget_name):
    #     pass  # TODO: Validate custom values

