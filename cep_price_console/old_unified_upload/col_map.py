from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.old_unified_upload.step import Step
from cep_price_console.old_unified_upload.model import Function
from cep_price_console.old_unified_upload.treeview import TreeviewConstructor
import tkinter as tk
import tkinter.ttk as ttk
import logging


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
        ColumnMapper.logger.log(logging.DEBUG, "Done!")
        self.treeview.grid(row=1, column=1, sticky=tk.NSEW)

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
        self.column_mapping_frame.configure(padding=5, style="Even.Group.TFrame")
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


class ColumnMapper(object):
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
    col_mapper_dict = {}

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master,
                 parent_frame,
                 grid_row,
                 desc):
        self.master = master
        self.frame = parent_frame
        self.grid_row = grid_row
        self.desc = desc

        # Field Name
        self.name = self.desc.get('name').replace("'", "").replace('"', "")
        self.label = ttk.Label(self.frame)
        self.label.grid(row=self.grid_row, column=0, sticky=tk.E)
        self.label.config(text=self.name)

        # TODO: Allow the user to edit datatypes
        # Field Datatype
        # self.datatype_var = tk.StringVar()
        # self.datatype_var.set(self.desc.get('type'))
        # self.datatype_var.trace_add('write', self.datatype_var_on_change)
        #
        # self.datatype_combo = ttk.Combobox(self.frame)
        # self.datatype_combo.grid(row=self.grid_row, column=1)
        # self.datatype_combo.config(state="readonly",
        #                            values=ColumnMapper.datatypes,
        #                            textvariable=self.datatype_var)
        # self.datatype_combo.bind('<<ComboboxSelected>>', self.datatype_combo_on_change)

        # Field Function
        self.function = None
        self.function_var = tk.StringVar()
        self.function_var.set(ColumnMapper.function_default)
        self.function_var.trace_add('write', self.function_var_on_change)

        self.function_combo = ttk.Combobox(self.frame)
        self.function_combo.grid(row=self.grid_row, column=2)
        self.function_combo.config(state="readonly",
                                   textvariable=self.function_var)
        # TODO: Allow user to do custom stuff
        # # Field Custom
        # self.custom_chk_var = tk.IntVar()
        # self.custom_chk_var.set(0)
        #
        # self.custom_chk_box = ttk.Checkbutton(self.frame)
        # self.custom_chk_box.grid(row=self.grid_row, column=3)
        # self.custom_chk_box.config(variable=self.custom_chk_var,
        #                            command=self.custom_chk_box_toggle)
        #
        # self.custom_var = tk.StringVar()
        # self.custom_var.set(ColumnMapper.custom_default)
        # self.custom_entry = ttk.Entry(self.frame)
        # self.custom_entry.grid(row=self.grid_row, column=4)
        # self.custom_entry.state(['disabled'])
        # custom_validation = (self.frame.register(self.validate_custom_value),
        #                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        # self.custom_entry.config(textvariable=self.custom_var,
        #                          validate='focusout',
        #                          validatecommand=custom_validation)

        ColumnMapper.col_mapper_dict[self.name] = self

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self, grid_row=None):
        pass
        # self.frame.columnconfigure(0, weight=1)  # TODO: Which column needs weight?
        # self.frame.rowconfigure(0, weight=1)  # TODO: Which row needs weight?

    # @debug(lvl=logging.DEBUG, prefix='')
    # def datatype_combo_on_change(self, *args):
    #     print(*args)  # TODO: Support datatype change
    #
    # @debug(lvl=logging.DEBUG, prefix='')
    # def datatype_var_on_change(self, *args):
    #     print(*args)  # TODO: Support datatype change

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def function_var_on_change(self, *args):
        if self.function is not None:
            self.function.field_desc = None
        self.function = None

        if self.function_var != ColumnMapper.function_default:
            func_obj = Function.func_dict.get(self.function_var.get())
            if func_obj is not None:
                self.function = func_obj
                self.function.field_desc = self.name
            else:
                ColumnMapper.logger.log(logging.ERROR, "Function Object Not Found: Function Variable = {0}".format(
                    self.function_var.get()))
        self.master.update_option_list()
        self.master.proceed_logic()

    # @debug(lvl=logging.DEBUG, prefix='')
    # def custom_chk_box_toggle(self, *args):
    #     if self.custom_chk_var.get() == 0:  # Unchecked
    #         ColumnMapper.logger.log(logging.DEBUG, "Button unchecked")
    #         self.custom_entry.state(['disabled'])
    #         self.custom_var.set(ColumnMapper.custom_default)
    #         self.function_combo.state(['!disabled'])
    #
    #     elif self.custom_chk_var.get() == 1:  # Checked
    #         ColumnMapper.logger.log(logging.DEBUG, "Button checked")
    #         self.custom_entry.state(['!disabled'])
    #         self.function_combo.state(['disabled'])
    #         self.function_var.set(ColumnMapper.function_default)
    #     else:
    #         ColumnMapper.logger.log(logging.ERROR, "Button not 0 or 1!")

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
