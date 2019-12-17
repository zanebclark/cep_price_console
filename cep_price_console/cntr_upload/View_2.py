from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import logging
from cep_price_console.cntr_upload.Treeview import TreeviewConstructor, TreeColumn, TreeRow
from cep_price_console.cntr_upload.CntrUploadTab import CntrUploadTab
from cep_price_console.utils.log_utils import CustomAdapter, debug
from sqlalchemy import Integer, VARCHAR, DATE, DECIMAL, INT
from dateutil.parser import parse

even_background = "honeydew2"
odd_background = "honeydew3"


class Step2ColumnMapping(CntrUploadTab):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, master, tab_text, tab_state='normal'):
        self.cntr_wb = None
        self.treeview_value_dict = {}
        self.upload_map_dict = None
        self.combobox_obj_dict = {}
        self.str_vars = {}
        self.header_combo_boxes = []
        # solostyle = Style()
        # solostyle.configure("Solo.TFrame", , relief=GROOVE, background="blue")
        CntrUploadTab.__init__(self,
                               master,
                               tab_text,
                               tab_state)
        self.frame_main.columnconfigure(1, weight=1)
        self.frame_main.rowconfigure(1, weight=1)

        self.column_mapping_hdr = Label(self.frame_main, text="Column Mapping")
        self.column_mapping_hdr.grid(row=0, column=0, columnspan=2, sticky=W)
        # self.worksheet_full = None

        self.treeview_frame = Frame(self.frame_main)
        self.treeview_frame.grid(row=1, column=1, sticky=NSEW)

        self.treeview = TreeviewConstructor(self, self.treeview_frame, False)

        self.canvas_frame = Frame(self.frame_main, padding=2)
        self.canvas_frame.grid(row=1, column=0, sticky=NSEW)
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.ysb = Scrollbar(self.canvas_frame, orient=VERTICAL,)

        self.canvas = Canvas(self.canvas_frame,
                             yscrollcommand=self.ysb.set,
                             borderwidth=2,
                             highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)

        self.column_mapping_frame = Frame(self.canvas, padding=5, style="even.group.TFrame")
        self.column_mapping_frame.update_idletasks()
        self.column_mapping_frame.columnconfigure(0, weight=1)
        self.column_mapping_frame.rowconfigure(0, weight=1)

        self.canvas.create_window((0, 0), window=self.column_mapping_frame, anchor=N + W, tags="column_mapping_frame")

        self.filler_frame = Frame(self.canvas_frame)
        self.filler_frame.grid(row=1, column=0, sticky=NSEW)

        self.ysb.config(command=self.canvas.yview)
        self.ysb.grid(row=0, column=1, sticky=NS)

        self.col_mapping_instr_lbl = Label(self.column_mapping_frame,
                                           text="These are the instructions on how to do this thing. \n"
                                                "1) You need to do something. \n"
                                                "2) You need to do something else. \n"
                                                "3) Finally, you need to do something else. \n"
                                                "Then you are done!", background=even_background)
        self.col_mapping_instr_lbl.grid(row=0, column=0, sticky=EW)

        self.hdr_mapping_frame = Frame(self.column_mapping_frame, padding=5, style="odd.group.TFrame")
        self.hdr_mapping_frame.columnconfigure(0, weight=1)
        self.hdr_mapping_frame.grid(row=1, column=0, sticky=NSEW, pady=2)

        self.hdr_mapping_label = Label(self.hdr_mapping_frame, style="odd.heading3.TLabel",
                                       text="Contract Header Columns:")
        self.hdr_mapping_label.grid(row=0, column=0, sticky=SW)

        self.period_1_mapping_frame = Frame(self.column_mapping_frame, padding=5, style="even.group.TFrame")
        self.period_1_mapping_frame.grid(row=2, column=0, sticky=NSEW, pady=2)
        self.period_1_mapping_frame.columnconfigure(0, weight=1)

        self.period_1_mapping_label = Label(self.period_1_mapping_frame, style="even.heading3.TLabel",
                                            text="Period 1 Columns:")
        self.period_1_mapping_label.grid(row=0, column=0, sticky=SW)

        self.period_2_mapping_frame = Frame(self.column_mapping_frame, padding=5, style="odd.group.TFrame")
        self.period_2_mapping_frame.grid(row=3, column=0, sticky=NSEW, pady=2)
        self.period_2_mapping_frame.columnconfigure(0, weight=1)

        self.period_2_mapping_label = Label(self.period_2_mapping_frame, style="odd.heading3.TLabel",
                                            text="Period 2 Columns:")
        self.period_2_mapping_label.grid(row=0, column=0, sticky=SW)

        self.period_3_mapping_frame = Frame(self.column_mapping_frame, padding=5, style="even.group.TFrame")
        self.period_3_mapping_frame.grid(row=4, column=0, sticky=NSEW, pady=2)
        self.period_3_mapping_frame.columnconfigure(0, weight=1)

        self.period_3_mapping_label = Label(self.period_3_mapping_frame, style="even.heading3.TLabel",
                                            text="Period 3 Columns:")
        self.period_3_mapping_label.grid(row=0, column=0, sticky=SW)

        self.reset = Button(self.frame_cmd, text="Reset Comboboxes", command=self.reset_combo_boxes)
        self.reset.grid(row=0, column=0)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        self.cntr_wb = self.cont.fetch_workbook()

        for col in self.cntr_wb.col_dict.values():
            tv_col_obj = TreeColumn(
                order=col.col_num_one_indexed,
                col_id=col.hdr_id,
                hdr_txt=col.hdr_id.replace("_", " "),
                display=True
            )
            self.treeview.col_obj_dict[tv_col_obj.col_id] = tv_col_obj
        self.treeview.populate_cols()

        for row_num in sorted(self.cntr_wb.row_dict.keys()):
            row_obj = self.cntr_wb.row_dict[row_num]
            tv_row_obj = TreeRow(
                treeview_const=self.treeview,
                iid=row_obj.row_num_one_indexed
            )
            for cell in row_obj.row_cells:
                self.__class__.logger.log(logging.NOTSET, "Cell Info: {0}".format(cell.formatted_value))
                tv_row_obj.xl_cells[cell.col_num_one_indexed] = cell
            self.treeview.item_obj_dict[tv_row_obj.iid] = tv_row_obj
        self.treeview.populate_items()
        self.treeview.stripe_rows()

        frame_dict = {
            "VendCntrNum": (1, self.hdr_mapping_frame),
            "VendProdNum": (2, self.hdr_mapping_frame),
            "CustProdNum": (3, self.hdr_mapping_frame),
            "QBreak": (4, self.hdr_mapping_frame),
            "UOM": (5, self.hdr_mapping_frame),
            "P1_ContrPrice": (1, self.period_1_mapping_frame),
            "P1_ContrCost": (2, self.period_1_mapping_frame),
            "P1_EffDate": (3, self.period_1_mapping_frame),
            "P1_ExpDate": (4, self.period_1_mapping_frame),
            "P2_ContrPrice": (1, self.period_2_mapping_frame),
            "P2_ContrCost": (2, self.period_2_mapping_frame),
            "P2_EffDate": (3, self.period_2_mapping_frame),
            "P2_ExpDate": (4, self.period_2_mapping_frame),
            "P3_ContrPrice": (1, self.period_3_mapping_frame),
            "P3_ContrCost": (2, self.period_3_mapping_frame),
            "P3_EffDate": (3, self.period_3_mapping_frame),
            "P3_ExpDate": (4, self.period_3_mapping_frame)
        }

        self.upload_map_dict = self.cont.fetch_upload_map_dict()

        for upload_id, (grid_row, frame) in frame_dict.items():
            self.__class__.logger.log(logging.DEBUG, "Upload ID: {0}".format(upload_id))
            combo = UploadMultiCombobox(
                master=self,
                frame=frame,
                grid_row=grid_row,
                upload_col=self.upload_map_dict.get(upload_id)
            )
            self.combobox_obj_dict[combo.upload_col.mapping_id] = combo

        self.column_mapping_frame.update_idletasks()

        self.canvas.itemconfigure("column_mapping_frame",
                                  height=self.column_mapping_frame.winfo_reqheight(),
                                  width=self.column_mapping_frame.winfo_reqwidth())
        self.canvas.config(scrollregion=self.canvas.bbox(ALL),
                           width=self.column_mapping_frame.winfo_reqwidth(),
                           height=self.column_mapping_frame.winfo_reqwidth())
        # self.testing()
        # self.ecolab_testing()

    @debug(lvl=logging.DEBUG, prefix='')
    def reset_combo_boxes(self):
        # self.manager.busy()
        for combo in self.combobox_obj_dict.values():
            combo.header_var.set("Select Worksheet Header")
            combo.data_var.set("Select Datatype")
        # self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def proceed_logic(self, *args):
        price_cost_uses = 0
        if self.combobox_obj_dict["P1_ContrPrice"].header_var.get() != 'Select Worksheet Header' \
                or self.combobox_obj_dict["P1_ContrCost"].header_var.get() != 'Select Worksheet Header':
            price_cost_uses += 1

        if self.combobox_obj_dict["P2_ContrPrice"].header_var.get() != 'Select Worksheet Header' \
                or self.combobox_obj_dict["P2_ContrCost"].header_var.get() != 'Select Worksheet Header':
            price_cost_uses += 1

        if self.combobox_obj_dict["P3_ContrPrice"].header_var.get() != 'Select Worksheet Header' \
                or self.combobox_obj_dict["P3_ContrPrice"].header_var.get() != 'Select Worksheet Header':
            price_cost_uses += 1

        if self.combobox_obj_dict["VendProdNum"].header_var.get() != 'Select Worksheet Header' \
                and price_cost_uses != 0:
            self.btn_next.state(['!disabled'])
            self.btn_next.bind("<ButtonRelease-1>", self.proceeding)
        else:
            self.btn_next.state(['disabled'])
            self.btn_next.unbind("<ButtonRelease-1>")

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def proceeding(self, *args):
        # self.manager.busy()
        self.cont.reset_contract()
        self.cont.upload_contract()
        if self.ecolab_check():
            self.master.step_3.populate_frame()
            self.master.tab_switcher(2)
        else:
            self.reset_combo_boxes()
            # and compare the contract numbers to the contract numbers in the system
        # self.manager.not_busy()

    @debug(lvl=logging.DEBUG, prefix='')
    def ecolab_check(self):
        cntr_distinct_values = self.cont.fetch_distinct_cntr()
        ecolab_cntr = False
        for (vend_cntr,) in cntr_distinct_values:
            self.__class__.logger.log(logging.DEBUG, "Distinct Cntr Value: {0}".format(vend_cntr))
            if vend_cntr is not None:
                cntr_details = self.cont.fetch_cntr_details(vend_cntr)
                for query_row in cntr_details.all():
                    self.__class__.logger.log(logging.DEBUG, "Vendor Number: {0}".format(query_row.Vendor_Number))
                    if query_row.Vendor_Number == "00257":
                        self.__class__.logger.log(logging.DEBUG, "Ecolab Contract. Apply logic")
                        ecolab_cntr = True
        if ecolab_cntr:
            p1_cost = self.combobox_obj_dict["P1_ContrCost"].header_var.get()
            self.__class__.logger.log(logging.DEBUG, "Period {num} Cost: {cost}".format(num="1", cost=p1_cost))
            p2_cost = self.combobox_obj_dict["P2_ContrCost"].header_var.get()
            self.__class__.logger.log(logging.DEBUG, "Period {num} Cost: {cost}".format(num="2", cost=p2_cost))
            p3_cost = self.combobox_obj_dict["P3_ContrCost"].header_var.get()
            self.__class__.logger.log(logging.DEBUG, "Period {num} Cost: {cost}".format(num="3", cost=p3_cost))
            default = "Select Worksheet Header"
            if p1_cost != default or p2_cost != default or p3_cost != default:
                self.__class__.logger.log(logging.DEBUG, "One or more cost fields set")
                messagebox.askokcancel(
                    "Ecolab Contracts Don't Dictate Costs",
                    "One or more cost columns have been selected. Ecolab contracts dictate price, not cost.",
                    parent=self.master
                )
                return False
            else:
                self.cont.ecolab_rule()
                return True
        else:
            return True

    @debug(lvl=logging.DEBUG, prefix='')
    def testing(self):
        self.combobox_obj_dict["VendProdNum"].header_var.set("Product")
        self.combobox_obj_dict["VendProdNum"].header_combo_on_change("")
        self.combobox_obj_dict["P1_ContrCost"].header_var.set("Price")
        self.combobox_obj_dict["P1_ContrCost"].header_combo_on_change("")
        self.combobox_obj_dict["P1_EffDate"].header_var.set("Valid From")
        self.combobox_obj_dict["P1_EffDate"].header_combo_on_change("")
        self.combobox_obj_dict["P1_ExpDate"].header_var.set("Valid To")
        self.combobox_obj_dict["P1_ExpDate"].header_combo_on_change("")

    @debug(lvl=logging.DEBUG, prefix='')
    def ecolab_testing(self):
        self.combobox_obj_dict["VendCntrNum"].header_var.set("Contract Num")
        self.combobox_obj_dict["VendCntrNum"].header_combo_on_change("")
        self.combobox_obj_dict["VendProdNum"].header_var.set("Ecolab ProdCd")
        self.combobox_obj_dict["VendProdNum"].header_combo_on_change("")

        self.combobox_obj_dict["P1_ContrPrice"].header_var.set("Curr Price")
        self.combobox_obj_dict["P1_ContrPrice"].header_combo_on_change("")
        self.combobox_obj_dict["P1_ContrPrice"].data_var.set("float")
        self.combobox_obj_dict["P1_ContrPrice"].data_combo_on_change("")

        self.combobox_obj_dict["P1_EffDate"].header_var.set("Curr Beg Dt")
        self.combobox_obj_dict["P1_EffDate"].header_combo_on_change("")
        self.combobox_obj_dict["P1_EffDate"].data_var.set("date")
        self.combobox_obj_dict["P1_EffDate"].data_combo_on_change("")

        self.combobox_obj_dict["P1_ExpDate"].header_var.set("Curr End Dt")
        self.combobox_obj_dict["P1_ExpDate"].header_combo_on_change("")
        self.combobox_obj_dict["P1_ExpDate"].data_var.set("date")
        self.combobox_obj_dict["P1_ExpDate"].data_combo_on_change("")

        self.combobox_obj_dict["P2_ContrPrice"].header_var.set("Future Price")
        self.combobox_obj_dict["P2_ContrPrice"].header_combo_on_change("")
        self.combobox_obj_dict["P2_ContrPrice"].data_var.set("float")
        self.combobox_obj_dict["P2_ContrPrice"].data_combo_on_change("")

        self.combobox_obj_dict["P2_EffDate"].header_var.set("Future Beg Dt")
        self.combobox_obj_dict["P2_EffDate"].header_combo_on_change("")
        self.combobox_obj_dict["P2_EffDate"].data_var.set("date")
        self.combobox_obj_dict["P2_EffDate"].data_combo_on_change("")

        self.combobox_obj_dict["P2_ExpDate"].header_var.set("Future End Dt")
        self.combobox_obj_dict["P2_ExpDate"].header_combo_on_change("")
        self.combobox_obj_dict["P2_ExpDate"].data_var.set("date")
        self.combobox_obj_dict["P2_ExpDate"].data_combo_on_change("")


class UploadMultiCombobox(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    conversion_dict = dict(
        string=(VARCHAR,),
        float=(DECIMAL,),
        integer=(Integer, INT),
        date=(DATE,),
        boolean=(Integer, VARCHAR, INT),
        error=(),
        blank=(Integer, VARCHAR, DATE, DECIMAL, INT))

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, frame, grid_row, upload_col=None):
        self.master = master
        self.frame_master = frame
        self.grid_row = grid_row
        self.upload_col = upload_col
        self.ws_col_sel = None
        self.background = None

        for thing in list(self.frame_master.configure().get("style")):
            if thing.find("TFrame") != -1:
                style = thing
                self.background = Style().lookup(style, "background")
                if self.background == even_background:
                    self.label_style = "even.dflt.TLabel"
                    self.checkbox_style = "even.dflt.TCheckbutton"
                elif self.background == odd_background:
                    self.label_style = "odd.dflt.TLabel"
                    self.checkbox_style = "odd.dflt.TCheckbutton"
                break
        self.frame_main = Frame(self.frame_master)
        self.frame_main.grid(row=self.grid_row, column=0)
        # self.manager = BusyManager(self.frame_main)

        self.label = Label(self.frame_main, text=self.upload_col.label, style=self.label_style)
        self.label.grid(row=0, column=0, columnspan=2, sticky=EW)

        self.header_var = StringVar()
        self.header_var.trace_add('write', self.header_var_on_change)

        self.header_combo = Combobox(
            self.frame_main,
            state="readonly",
            values=[col.hdr_id.replace("_", " ") for col in self.master.cntr_wb.col_dict.values()],
            textvariable=self.header_var
        )

        self.header_combo.grid(row=1, column=0, sticky=E)
        self.header_combo.bind('<<ComboboxSelected>>', self.header_combo_on_change)

        self.data_var = StringVar()
        self.data_var.trace_add('write', self.data_combo_on_change)

        self.data_combo = Combobox(
            self.frame_main,
            state="readonly",
            values=list(self.__class__.conversion_dict.keys()),
            textvariable=self.data_var
        )
        self.data_combo.grid(row=1, column=1, sticky=E)

        self.static_value_label = Label(self.frame_main, text="Static Value:", style=self.label_style)
        self.static_value_label.grid(row=0, column=2, columnspan=2, sticky=EW)

        self.static_value_checkbutton_var = IntVar()

        self.static_value_checkbutton = Checkbutton(self.frame_main,
                                                    style=self.checkbox_style,
                                                    variable=self.static_value_checkbutton_var,
                                                    command=self.static_value_toggle)
        self.static_value_checkbutton.grid(row=1, column=2)

        self.static_value_entry_var = StringVar()
        static_validation = (self.frame_main.register(self.validate_static_value),
                             '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.static_value_entry = Entry(self.frame_main,
                                        textvariable=self.static_value_entry_var,
                                        validate='focusout',
                                        validatecommand=static_validation)
        self.static_value_entry.grid(row=1, column=3)
        self.static_value_entry.state(['disabled'])

        self.header_var.set("Select Worksheet Header")
        self.data_var.set("Select Datatype")

        # self.data_combo.bind('<<ComboboxSelected>>', self.data_combo_on_change)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def static_value_toggle(self, *args):
        if self.static_value_checkbutton_var.get() == 0:  # Unchecked
            self.static_value_entry.state(['disabled'])
            self.static_value_entry_var.set("")

            self.header_combo.state(['!disabled'])
            # self.header_var.set("Select Worksheet Header")

            self.data_combo.state(['!disabled'])
            # self.data_var.set("Select Datatype")

        elif self.static_value_checkbutton_var.get() == 1:  # Checked
            self.static_value_entry.state(['!disabled'])

            self.header_combo.state(['disabled'])
            self.header_var.set("Select Worksheet Header")

            self.data_combo.state(['disabled'])
            self.data_var.set("Select Datatype")

        print("Hey!")
        print(self.static_value_checkbutton_var.get())
        print(self.static_value_entry_var.get())

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def header_var_on_change(self, *args):
        # self.manager.busy()
        self.__class__.logger.log(logging.DEBUG, "Header Variable: {0}".format(self.header_var.get()))
        if self.header_var.get() == "Select Worksheet Header":
            self.data_combo.state(['disabled'])
        else:
            self.data_combo.state(['!disabled'])
        # self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def header_combo_on_change(self, *args):
        # self.manager.busy()
        if self.header_var.get() != "Select Worksheet Header":
            self.__class__.logger.log(logging.DEBUG, "Header Var: {0}".format(self.header_var.get()))
            for col in self.master.cntr_wb.col_dict.values():
                self.__class__.logger.log(logging.DEBUG, "Col Hdr: {0}".format(col.hdr_id.replace("_", " ")))
                if self.header_var.get() == col.hdr_id.replace("_", " "):
                    self.__class__.logger.log(logging.DEBUG, "Header Var: {0}".format(self.header_var.get()))
                    self.__class__.logger.log(logging.DEBUG, "Tv Header Text: {0}".format(col.hdr_cell.raw_val))
                    self.ws_col_sel = col
                    self.upload_col.ws_col_obj = self.ws_col_sel
                    self.upload_col.static_value = None
                    break
            self.__class__.logger.log(logging.DEBUG, "Format Selection: {0}".format(self.ws_col_sel.fmt_selection))
            self.data_var.set(self.ws_col_sel.fmt_selection)
            self.master.proceed_logic()
        # self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def data_combo_on_change(self, *args):
        # self.manager.busy()
        self.__class__.logger.log(logging.DEBUG, "DataVar: {0}".format(self.data_var.get()))
        if self.header_var.get() != "Select Worksheet Header":
            self.ws_col_sel.fmt_selection = self.data_var.get()
            if not isinstance(self.upload_col.datatype, self.__class__.conversion_dict.get(self.data_var.get())):
                self.data_combo.config(style="Bad.TCombobox")
            else:
                self.data_combo.config(style="TCombobox")
            self.master.treeview.tv_refresh()
        else:
            self.data_combo.config(style="TCombobox")
        # self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_static_value(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type,
                              widget_name):
        # self.manager.busy()
        if value_if_allowed is not None:
            if isinstance(self.upload_col.datatype, VARCHAR):
                try:
                    str_val = str(value_if_allowed)
                except ValueError:
                    self.__class__.logger.log(
                        logging.ERROR,
                        "{upload_id} static value must be a string. Type {type} detected.".format(
                            upload_id=self.upload_col.mapping_id,
                            type=str(type(value_if_allowed))
                        )
                    )
                    messagebox.askokcancel(
                        "Invalid Static Value Entry",
                        "{upload_id} static value must be a string. Type {type} detected.".
                        format(upload_id=self.upload_col.mapping_id,
                               type=str(type(value_if_allowed))),
                        parent=self.frame_main)
                    self.static_value_entry_var.set("")
                    self.upload_col.static_value = None
                    # self.manager.not_busy()
                    return False
                else:
                    self.__class__.logger.log(
                        logging.DEBUG, "Static Value: {0}".format(self.static_value_entry_var.get())
                    )
                    self.static_value_entry_var.set(str_val)
                    self.upload_col.static_value = self.static_value_entry_var.get()
                    self.upload_col.ws_col_obj = None
                    # self.manager.not_busy()
                    return True
            elif isinstance(self.upload_col.datatype, DECIMAL):
                try:
                    float_val = float(value_if_allowed)
                except ValueError:
                    self.__class__.logger.log(
                        logging.ERROR,
                        "{upload_id} static value must be a float. Type {type} detected.".format(
                            upload_id=self.upload_col.mapping_id,
                            type=str(type(value_if_allowed))
                        )
                    )
                    messagebox.askokcancel(
                        "Invalid Static Value Entry",
                        "{upload_id} static value must be a float. Type {type} detected.".
                        format(upload_id=self.upload_col.mapping_id,
                               type=str(type(value_if_allowed))),
                        parent=self.frame_main
                    )
                    self.static_value_entry_var.set("")
                    self.upload_col.static_value = None
                    # self.manager.not_busy()
                    return False
                else:
                    self.__class__.logger.log(
                        logging.DEBUG, "Static Value: {0}".format(self.static_value_entry_var.get())
                    )
                    self.static_value_entry_var.set(float_val)
                    self.upload_col.static_value = self.static_value_entry_var.get()
                    self.upload_col.ws_col_obj = None
                    # self.manager.not_busy()
                    return True
            elif isinstance(self.upload_col.datatype, (Integer, INT)):
                try:
                    int_val = int(value_if_allowed)
                except ValueError:
                    self.__class__.logger.log(
                        logging.ERROR,
                        "{upload_id} static value must be an integer. Type {type} detected.".format(
                            upload_id=self.upload_col.mapping_id,
                            type=str(type(value_if_allowed))
                        )
                    )
                    messagebox.askokcancel(
                        "Invalid Static Value Entry",
                        "{upload_id} static value must be an integer. Type {type} detected.".
                        format(upload_id=self.upload_col.mapping_id,
                               type=str(type(value_if_allowed))),
                        parent=self.frame_main
                    )
                    self.static_value_entry_var.set("")
                    self.upload_col.static_value = None
                    # self.manager.not_busy()
                    return False
                else:
                    self.__class__.logger.log(
                        logging.DEBUG, "Static Value: {0}".format(self.static_value_entry_var.get())
                    )
                    self.static_value_entry_var.set(int_val)
                    self.upload_col.static_value = self.static_value_entry_var.get()
                    self.upload_col.ws_col_obj = None
                    # self.manager.not_busy()
                    return True
            elif isinstance(self.upload_col.datatype, DATE):
                try:
                    date_val = parse(value_if_allowed)
                except ValueError:
                    self.__class__.logger.log(
                        logging.ERROR,
                        "{upload_id} static value must be a date-like string.".format(
                            upload_id=self.upload_col.mapping_id
                        )
                    )
                    messagebox.askokcancel(
                        "Invalid Static Value Entry",
                        "{upload_id} static value must be a date-like string.".
                        format(upload_id=self.upload_col.mapping_id),
                        parent=self.frame_main
                    )
                    self.static_value_entry_var.set("")
                    self.upload_col.static_value = None
                    # self.manager.not_busy()
                    return False
                else:
                    self.__class__.logger.log(
                        logging.DEBUG, "Static Value: {0}".format(self.static_value_entry_var.get())
                    )
                    self.static_value_entry_var.set(date_val)
                    self.upload_col.static_value = self.static_value_entry_var.get()
                    self.upload_col.ws_col_obj = None
                    # self.manager.not_busy()
                    return True
        else:
            self.static_value_entry_var.set("")
            self.upload_col.static_value = None
            # self.manager.not_busy()
            return False
