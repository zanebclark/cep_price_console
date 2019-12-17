import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from collections import OrderedDict
import logging
import os
import xlsxwriter
from tkintertable.TableModels import TableModel
from sqlalchemy.sql import literal
from sqlalchemy.sql.expression import and_, union_all
from cep_price_console.utils.log_utils import CustomAdapter, debug

# TODO: Add an "OK" button (or proceed)
# TODO: Last sold date?
# TODO: Get rid of shipping information
# TODO: Get rid of most columns
# TODO: Write validation formula for typed data


logger = CustomAdapter(logging.getLogger(str(__name__)), None)
check_btn_style_template = "{}.dflt.TCheckbutton"


@debug(lvl=logging.DEBUG, prefix='')
def vendor_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Num,
                         ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Name,
                         ARW_PRF_Mapping.vend_main_01_current.__table__.c.Status)


@debug(lvl=logging.DEBUG, prefix='')
def product_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num,
                         ARW_PRF_Mapping.prod_main_01_current.__table__.c.Desc_Full,
                         ARW_PRF_Mapping.prod_main_01_current.__table__.c.Status)


@debug(lvl=logging.DEBUG, prefix='')
def product_line_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Code,
                         ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Desc,
                         ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Major_Group)


@debug(lvl=logging.DEBUG, prefix='')
def major_group_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.major_group_main_01_current.__table__.c.Code,
                         ARW_PRF_Mapping.major_group_main_01_current.__table__.c.Desc)


@debug(lvl=logging.DEBUG, prefix='')
def customer_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    cust_shipto_union = union_all(
        session.query(
            ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.Cust_Num.label("Cust_Num"),
            ARW_PRF_Mapping.shipto_cust_01_current.__table__.c.Cust_Name.label("Cust_Name"),
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.Ship_To_Code.label("Ship_To_Code"),
            ARW_PRF_Mapping.shipto_main_01_current.__table__.c.ShipTo_Name.label("ShipTo_Name")
        ).join(
            ARW_PRF_Mapping.shipto_cust_01_current.__table__,
            ARW_PRF_Mapping.shipto_cust_01_current.Cust_Num_ShipTo_Combo ==
            ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo
        ),
        session.query(
            ARW_PRF_Mapping.cust_master_01_current.Cust_Num_ShipTo_Combo.label("Cust_Num_ShipTo_Combo"),
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Num.label("Cust_Num"),
            ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Name.label("Cust_Name"),
            literal("_All").label("Ship_To_Code"),
            literal("N/A").label("ShipTo_Name")
        )
    ).alias()
    return session.query(cust_shipto_union)


@debug(lvl=logging.DEBUG, prefix='')
def contract_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num,
                         ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Desc,
                         ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Num,
                         ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num,
                         ARW_PRF_Mapping.cntr_header_01_current.__table__.c.All_Cust_Flag)


@debug(lvl=logging.DEBUG, prefix='')
def customer_category_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Cat).distinct()


@debug(lvl=logging.DEBUG, prefix='')
def price_group_dataset(session):
    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    return session.query(ARW_PRF_Mapping.prod_main_01_current.__table__.c.Price_Group_Code).distinct()


class PriceList(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        from cep_price_console.db_management.server_utils import mysql_session_maker
        from cep_price_console.utils import config
        from cep_price_console.utils.gui_utils import center_window
        self.session = mysql_session_maker()
        self.master = master
        self.name = str(PriceList.__name__).lower()
        super().__init__(name=self.name, *args, **kwargs)
        Factor.reset(root=self)
        PanedFrame.reset(root=self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("Filtering Criteria")

        self.iconbitmap(config.FAVICON)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.paned_outer = tk.PanedWindow(self,
                                          orient=tk.HORIZONTAL,
                                          name="paned_outer",
                                          sashrelief=tk.RAISED,
                                          sashwidth=7)

        self.paned_outer.grid(row=0, column=0, sticky=tk.NSEW)

        self.factor_selection_frame = ttk.Frame(self.paned_outer,
                                                name="factor_selection_canvas_frame",
                                                style="even.group.TFrame",
                                                padding=5)
        self.factor_selection_frame.columnconfigure(0, weight=1)

        # self.column_selection_frame = ttk.Frame(self.paned_outer,
        #                                         style="odd.group.TFrame",
        #                                         padding=5)

        self.paned_factor_criteria = tk.PanedWindow(self.paned_outer,
                                                    orient=tk.HORIZONTAL,
                                                    name="paned_factor_criteria",
                                                    sashrelief=tk.RAISED,
                                                    sashwidth=7)

        self.factor_contract = Factor(dataset_query=contract_dataset(self.session),
                                      dataset_key_col=ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num,
                                      orient=tk.VERTICAL,
                                      lbl_str="Contract")

        self.factor_customer = Factor(dataset_query=customer_dataset(self.session),
                                      dataset_key_col=ARW_PRF_Mapping.shipto_main_01_current.Cust_Num_ShipTo_Combo,
                                      orient=tk.VERTICAL,
                                      lbl_str="Customer")

        self.factor_cust_category = Factor(dataset_query=customer_category_dataset(self.session),
                                           dataset_key_col=ARW_PRF_Mapping.cust_master_01_current.__table__.c.Cust_Cat,
                                           orient=tk.VERTICAL,
                                           lbl_str="Customer Category")

        self.factor_product = Factor(dataset_query=product_dataset(self.session),
                                     dataset_key_col=ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num,
                                     orient=tk.VERTICAL,
                                     lbl_str="Product")

        self.factor_product_line = Factor(dataset_query=product_line_dataset(self.session),
                                          dataset_key_col=ARW_PRF_Mapping.prod_line_main_01_current.__table__.c.Code,
                                          orient=tk.VERTICAL,
                                          lbl_str="Product Line")

        self.factor_price_group = Factor(
            dataset_query=price_group_dataset(self.session),
            dataset_key_col=ARW_PRF_Mapping.prod_main_01_current.__table__.c.Price_Group_Code,
            orient=tk.VERTICAL,
            lbl_str="Price Group")

        self.factor_primary_vendor = Factor(dataset_query=vendor_dataset(self.session),
                                            dataset_key_col=ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Num,
                                            orient=tk.VERTICAL,
                                            lbl_str="Primary Vendor")

        self.factor_secondary_vendor = Factor(dataset_query=vendor_dataset(self.session),
                                              dataset_key_col=ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Num,
                                              orient=tk.VERTICAL,
                                              lbl_str="Secondary Vendor")

        self.factor_major_group = Factor(dataset_query=major_group_dataset(self.session),
                                         dataset_key_col=ARW_PRF_Mapping.major_group_main_01_current.__table__.c.Code,
                                         orient=tk.VERTICAL,
                                         lbl_str="Major Group")

        self.test_btn = ttk.Button(self.factor_selection_frame,
                                   text="Run Price List",
                                   command=self.make_a_list)
        self.test_btn.grid(row=0, column=0)

        self.reporting_options = ReportingOptions(
            self.factor_selection_frame, relief=tk.GROOVE, padding=5, borderwidth=8
        )
        self.reporting_options.grid(row=1, column=0, sticky=tk.NW + tk.E)

        self.factor_selection = FactorSelection(
            self.factor_selection_frame, relief=tk.GROOVE, padding=5, borderwidth=8
        )
        self.factor_selection.grid(row=2, column=0, sticky=tk.NW + tk.N)

        Factor.factor_selection_populate(self.factor_selection, row=1)

        self.factor_selection_instructions = FactorSelectionInstructions(
            self.factor_selection_frame, relief=tk.GROOVE, padding=5, borderwidth=8
        )
        self.factor_selection_instructions.grid(row=3, column=0, sticky=tk.NW + tk.E)

        self.factor_selection_frame.update_idletasks()

        self.paned_outer.add(self.factor_selection_frame,
                             width=480,
                             pady=5,
                             padx=5,
                             stretch="never")
        # self.paned_outer.add(self.column_selection_frame,
        #                      width=300,
        #                      pady=5,
        #                      padx=5,
        #                      stretch="never")
        self.paned_outer.add(self.paned_factor_criteria,
                             width=0,
                             pady=5,
                             padx=5,
                             stretch="always")
        self.paned_outer.bind("<Configure>", self.test_config)

        self.factor_customer.sel_check_btn.invoke()
        # self.factor_customer.crit_obj.add_btn.invoke()
        # self.factor_customer.crit_obj.add_btn.invoke()
        # self.factor_customer.crit_obj.add_btn.invoke()
        # value_list = ["0001229_All", "0001052_00000001", "0001219_00000013"]
        self.factor_customer.crit_obj.add_btn.invoke()
        value_list = ["0001229_All"]
        for entry_dict, value in zip(self.factor_customer.crit_obj.entry_dict.values(), value_list):
            entry_obj = entry_dict["entry_obj"]
            entry_obj.value = value

        # self.factor_product.sel_check_btn.invoke()
        # self.factor_product.crit_obj.add_btn.invoke()
        # for entry_dict in self.factor_product.crit_obj.entry_dict.values():
        #     entry_obj = entry_dict["entry_obj"]
        #     entry_obj.value = "HOSS-HG12-S000"

        self.factor_product_line.sel_check_btn.invoke()
        self.factor_product_line.crit_obj.add_btn.invoke()
        for entry_dict in self.factor_product_line.crit_obj.entry_dict.values():
            entry_obj = entry_dict["entry_obj"]
            # entry_obj.value = "PLSoloTest"
            entry_obj.value = "JANI"

        center_window(win_obj=self, width=1200, height=900)

    @debug(lvl=logging.DEBUG, prefix='')
    def make_a_list(self):
        # worksheet2.repeat_rows(0, 1) to repeat rows at top while printing
        # for headers/footers
        # https://xlsxwriter.readthedocs.io/example_headers_footers.html?highlight=header
        workbook = self.get_workbook()
        self.write_worksheet(
            workbook=workbook,
            output_query=self.get_sherpa(
                min_level=self.reporting_options.min_level_chkbtn.instate(['selected']),
                expired=self.reporting_options.expired_chkbtn.instate(['selected']),
                current=self.reporting_options.current_chkbtn.instate(['selected']),
                future=self.reporting_options.future_chkbtn.instate(['selected']),
                return_mode=self.reporting_options.return_mode_combobox.get()
            ),
            sheet_name="price_list")  # TODO: Change this
        workbook.close()

    @debug(lvl=logging.DEBUG, prefix='')
    def get_workbook(self):
        filename_options = dict(
            title='Save Output',
            initialdir=str(os.path.expanduser('~')).replace('\\', '/'),
            initialfile=None,
            parent=self,
            filetypes=[('Workbook', '.xlsx')])

        fullpath_var = str(filedialog.asksaveasfilename(**filename_options)).replace("/", "\\")
        # fullpath_var = os.path.join(os.path.expanduser('~'), "Desktop", "{test_name}")
        filename, _ = os.path.splitext(fullpath_var)
        return xlsxwriter.Workbook('{}.xlsx'.format(filename))

    @debug(lvl=logging.DEBUG, prefix='')
    def write_worksheet(self, workbook, output_query, sheet_name=None):
        if sheet_name is not None:
            worksheet = workbook.add_worksheet(sheet_name)
        else:
            worksheet = workbook.add_worksheet()

        header_format = workbook.add_format({'bold': True,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'fg_color': '#D7E4BC',
                                             'border': 1})

        worksheet.freeze_panes(1, 0)
        integer_format = workbook.add_format({'num_format': '#,##0'})
        currency_format = workbook.add_format({'num_format': '#,##0.00'})
        date_format = workbook.add_format({'num_format': 'mm/dd/yy'})

        col_number = 0
        row_number = 0
        col_list = []

        for desc in output_query.column_descriptions:
            self.__class__.logger.log(logging.DEBUG, str(desc))
            name = desc.get('name').replace("'", "").replace('"', "")
            if name in (
                    # "Cust_Num_ShipTo_Combo",
                    "Cust_Num",
                    "Ship_To_Code",
                    # "Cust_Cat",
                    "Prod_Num",
                    # "Prod_Line",
                    # "Price_Group_Code",
                    # "C1_Cost",
                    # "C2_Cost",
                    # "C3_Cost",
                    # "C4_Cost",
                    # "C5_Cost",
                    # "C6_Cost",
                    # "C7_Cost",
                    # "L1_Price",
                    # "L2_Price",
                    # "L3_Price",
                    # "L4_Price",
                    # "Fut_Price",
                    # "Fut_Price_Column",
                    # "Fut_Price_Date",
                    "Days_Since_Last_Purch",
                    # "Price_Matrix_Combo_ID",
                    "Price_Level_Num",
                    "Price_Eff_Date",
                    "Price_Exp_Date",
                    "Net_Price",
                    # "Cost_Matrix_Combo_ID",
                    "Cost_Level_Num",
                    "Cost_Eff_Date",
                    "Cost_Exp_Date",
                    "Net_Cost"
            ):
                col_list.append(name)
                worksheet.write(row_number, col_number, name, header_format)
                col_number += 1

        row_number += 1
        for row in output_query.all():
            col_number = 0
            for col_name in col_list:
                # noinspection PyProtectedMember
                value = row._asdict().get(col_name)
                if isinstance(value, str):
                    value.replace("{", "").replace("}", "")
                if col_name in (
                        "C1_Cost",
                        "C2_Cost",
                        "C3_Cost",
                        "C4_Cost",
                        "C5_Cost",
                        "C6_Cost",
                        "C7_Cost",
                        "L1_Price",
                        "L2_Price",
                        "L3_Price",
                        "L4_Price",
                        "Fut_Price",
                        "Net_Cost",
                        "Net_Price"
                ):
                    worksheet.write(row_number, col_number, value, currency_format)
                elif col_name in (
                        "Days_Since_Last_Purch",
                        "Price_Level_Num",
                        "Cost_Level_Num"
                ):
                    worksheet.write(row_number, col_number, value, integer_format)
                elif col_name in (
                        "Fut_Price_Date",
                        "Price_Eff_Date",
                        "Price_Exp_Date",
                        "Cost_Eff_Date",
                        "Cost_Exp_Date"
                ):
                    if value != "0000-00-00":
                        worksheet.write(row_number, col_number, value, date_format)
                else:
                    worksheet.write(row_number, col_number, value)
                col_number += 1
            row_number += 1

        worksheet.autofilter(0, 0, row_number, col_number)

    @debug(lvl=logging.DEBUG, prefix='')
    def test_it(self, workbook):
        option_list = []
        for min_level in True, False:
            for expired in True, False:
                for current in True, False:
                    for future in True, False:
                        # for return_mode in ("all", "sales", "matrix", "sales_or_matrix"):
                        option_list.append(
                            {
                                "min_level": min_level,
                                "expired": expired,
                                "current": current,
                                "future": future,
                                "return_mode": "matrix"
                            }
                        )

        for option in option_list:
            if option["return_mode"] == "sales_or_matrix":
                ws_ret_mode = "s_or_m"
            else:
                ws_ret_mode = option["return_mode"]
            self.write_worksheet(
                workbook=workbook,
                output_query=self.get_sherpa(**option),
                sheet_name="Lvl-{min_level}_Exp-{expired}_Cur-{current}_Fut-{future}_{return_mode}".format(
                    min_level=int(option["min_level"]),
                    expired=int(option["expired"]),
                    current=int(option["current"]),
                    future=int(option["future"]),
                    return_mode=ws_ret_mode)
            )
        workbook.close()

    @debug(lvl=logging.DEBUG, prefix='')
    def get_sherpa(self,
                   min_level=False,
                   expired=True,
                   current=True,
                   future=True,
                   return_mode="all"):
        from cep_price_console.db_management.price_matrix_utils import MatrixSherpa
        matrix_sherpa = MatrixSherpa(
            min_level=min_level,
            expired=expired,
            current=current,
            future=future,
            return_mode=return_mode,
            cntr_num_list=self.factor_contract.get_values(),
            cust_num_shipto_combo_list=self.factor_customer.get_values(),
            cust_cat_list=self.factor_cust_category.get_values(),
            prod_num_list=self.factor_product.get_values(),
            prod_line_list=self.factor_product_line.get_values(),
            price_group_code_list=self.factor_price_group.get_values(),
            prim_vend_num_list=self.factor_primary_vendor.get_values(),
            secondary_vend_num_list=self.factor_secondary_vendor.get_values(),
            major_group_list=self.factor_major_group.get_values()
        )
        return matrix_sherpa.final_return_query()

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        msgbox = messagebox.askokcancel("Quit", "Do you want to quit?", parent=self)
        if msgbox:
            self.destroy()

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def test_config(self, event):
        self.factor_selection_frame.event_generate("<Configure>")


class ReportingOptions(ttk.Labelframe):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.labelwidget = ttk.Label(
            self.parent,
            text="1) Report Options",
            wraplength=20,
            style="heading3.TLabel",
        )
        # noinspection PyArgumentList
        super().__init__(self.parent, *args, labelwidget=self.labelwidget, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.columnconfigure(0, weight=1)
        self.row_count = 0
        self.option_instructions = ttk.Label(
            self,
            text=("  a) Minimum Level Only: If there are multiple 'levels' in the matrix for a product/customer match, "
                  "return only the lowest level \n  b) Time Period Options: Return expired, current, or future entries "
                  "based on today's date\n  c) Return Mode: \n    - all: Return all combinations \n    - sales: "
                  "Return only combinations that have a recorded sale\n    - matrix: Return only combinations that "
                  "have a matrix entry \n    - sales or matrix: Return combinations that have either a recorded sale "
                  "or a matrix entry"),
            wraplength=self.winfo_width(),
            style="even.notes.TLabel"
        )
        self.option_instructions.grid(row=self.row_count, column=0, columnspan=2, sticky=tk.NW + tk.E)

        self.row_count += 1
        self.min_level_chkbtn = self.add_checkbutton(self, "Minimum Level Only", columnspan=2)

        self.period_frame_label = ttk.Label(
            self,
            text="Time Period Options:",
            style="dflt.TLabel"
        )
        self.period_label_frame = ttk.Labelframe(
            self,
            borderwidth=12,
            labelwidget=self.period_frame_label
        )
        self.period_label_frame.grid(row=self.row_count, column=0, columnspan=2, sticky=tk.NW + tk.E)
        self.period_label_frame.columnconfigure(0, weight=1)
        self.row_count += 1
        self.expired_chkbtn = self.add_checkbutton(self.period_label_frame, "Expired Entries")
        self.current_chkbtn = self.add_checkbutton(self.period_label_frame, "Current Entries")
        self.future_chkbtn = self.add_checkbutton(self.period_label_frame, "Future Entries")

        self.return_mode_label = ttk.Label(
            self,
            text="Return Mode",
            style="even.dflt.TLabel",
        )
        self.return_mode_label.grid(row=self.row_count, column=0, sticky=tk.EW)

        self.return_mode_combobox = ttk.Combobox(self,
                                                 state="readonly",
                                                 values=["all", "sales", "matrix", "sales_or_matrix"],
                                                 )
        self.return_mode_combobox.set("all")
        self.return_mode_combobox.grid(row=self.row_count, column=1, sticky=tk.W)

    def add_checkbutton(self, parent, text, columnspan=None):
        if self.row_count % 2 == 0:
            style_string = check_btn_style_template.format("even")
        elif self.row_count % 2 == 1:
            style_string = check_btn_style_template.format("odd")
        else:
            raise ValueError

        checkbutton = ttk.Checkbutton(parent,
                                      text=text,
                                      # Command?
                                      style="{}".format(style_string))
        checkbutton.state(['!alternate', 'selected'])
        if columnspan is not None:
            checkbutton.grid(row=self.row_count, column=0, sticky=tk.EW, columnspan=columnspan)
        else:
            checkbutton.grid(row=self.row_count, column=0, sticky=tk.EW)
        self.row_count += 1
        return checkbutton

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.labelwidget.configure(wraplength=self.winfo_width())
        self.option_instructions.configure(wraplength=self.winfo_width())


class FactorSelection(ttk.Labelframe):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.labelwidget = ttk.Label(
            self.parent,
            text="2) Factor Selection",
            wraplength=20,
            style="heading3.TLabel",
        )
        # noinspection PyArgumentList
        super().__init__(self.parent, *args, labelwidget=self.labelwidget, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.columnconfigure(0, weight=1)
        self.factor_check_box_instr = ttk.Label(
            self,
            text=("  a) Check the box next to the entity you want to filter by. A selection dialogue will appear to "
                  "the right.\n"
                  "  b) See instructions for the selection dialogue below"),
            wraplength=self.winfo_width(),
            style="even.notes.TLabel"
        )
        self.factor_check_box_instr.grid(row=0, column=0, sticky=tk.NW + tk.E)

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.labelwidget.configure(wraplength=self.winfo_width())
        self.factor_check_box_instr.configure(wraplength=self.winfo_width())


class FactorSelectionInstructions(ttk.Labelframe):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.labelwidget = ttk.Label(
            self.parent,
            text="3) Selection Instructions",
            wraplength=20,
            style="heading3.TLabel"
        )
        # noinspection PyArgumentList
        super().__init__(self.parent, *args, labelwidget=self.labelwidget, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.columnconfigure(0, weight=1)
        instr = (
            "  a) Add a selection entity by clicking the 'Add...' button at the bottom of the dialog.\n"
            "  b) Select 'Search' to launch a dialog displaying all options. This dialog can be filtered and sorted.\n"
            "  c) To remove a selection, click on the red 'X'. To remove the entire factor, uncheck the factor on the "
            "dialogue to the left or select the red 'X' on the top right-hand corner of the factor pane."
        )

        self.factor_selection_instr = ttk.Label(
            self,
            style="even.notes.TLabel",
            text=instr,
            wraplength=self.winfo_width()
        )
        self.factor_selection_instr.grid(row=0, column=0, sticky=tk.NW + tk.E)

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.labelwidget.configure(wraplength=self.winfo_width())
        self.factor_selection_instr.configure(wraplength=self.winfo_width())


class Factor(object):
    root = None
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    fact_dict = {}

    # @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 dataset_query,
                 dataset_key_col,
                 orient,
                 lbl_str):
        self.lbl_str = lbl_str
        self.lbl_str_useful = self.lbl_str.lower().replace(" ", "_")
        self.dataset_query = dataset_query
        self.dataset_key_col = dataset_key_col
        self.orient = orient
        self.sel_check_btn = None
        self.crit_obj = None
        Factor.fact_dict[self.lbl_str] = self

    @debug(lvl=logging.DEBUG, prefix='')
    def get_values(self):
        value_list = []
        if self.crit_obj is None:
            return []
        else:
            for entry_subdict in self.crit_obj.entry_dict.values():
                entry_obj = entry_subdict["entry_obj"]
                if entry_obj.value != "":
                    value_list.append(entry_obj.value)
            return value_list

    @debug(lvl=logging.DEBUG, prefix='')
    def check_grid(self, frame, row, column=0, sticky=tk.EW):
        if row % 2 == 0:
            style_string = check_btn_style_template.format("even")
        elif row % 2 == 1:
            style_string = check_btn_style_template.format("odd")
        else:
            raise ValueError

        self.sel_check_btn = ttk.Checkbutton(frame,
                                             text="{}".format(self.lbl_str),
                                             command=self.check_cmd,
                                             style="{}".format(style_string),
                                             name="{}_sel_check_btn".format(self.lbl_str_useful))
        self.sel_check_btn.state(['!alternate', '!selected'])
        self.sel_check_btn.grid(row=row, column=column, sticky=sticky)

    @debug(lvl=logging.DEBUG, prefix='')
    def check_cmd(self):
        if self.crit_obj is None:
            self.crit_obj = PanedFrame(factor=self,
                                       dataset_query=self.dataset_query,
                                       dataset_key_col=self.dataset_key_col,
                                       orient=self.orient,
                                       lbl_str=self.lbl_str)

        if 'selected' in self.sel_check_btn.state():
            self.crit_obj.grid_frame()
        elif 'selected' not in self.sel_check_btn.state():
            self.crit_obj.remove_frame()

    @classmethod
    @debug(lvl=logging.DEBUG, prefix='')
    def reset(cls, root=None):
        cls.root = root
        cls.fact_dict = {}

    @classmethod
    @debug(lvl=logging.DEBUG, prefix='')
    def factor_selection_populate(cls, frame, row):
        row_count = row
        for fact in cls.fact_dict.values():
            fact.check_grid(frame=frame, row=row_count)
            row_count += 1
        return row_count


class PanedFrame(ttk.Frame):
    root = None
    dictionary = {}
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 factor,
                 dataset_query,
                 dataset_key_col,
                 lbl_str,
                 orient=tk.VERTICAL,
                 background="honeydew2",
                 borderwidth=5,
                 relief=tk.RIDGE,
                 sashpad=2,
                 sashrelief=tk.RAISED,
                 sashwidth=10,
                 disallow_dragging=False,
                 cursor=None,
                 opaqueresize=True,
                 *args,
                 **kwargs):
        from cep_price_console.utils.paned_window import PanedWindowHorizontal, PanedWindowVertical
        self.factor = factor
        self.dataset_query = dataset_query
        self.dataset_key_col = dataset_key_col
        self.lbl_str = lbl_str
        self.orient = orient
        # noinspection PyArgumentList
        super().__init__(Factor.root.paned_factor_criteria, *args, **kwargs)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(style="odd.group.TFrame",
                    relief=tk.GROOVE,
                    padding=5)

        self.header = ttk.Label(self,
                                text="{} Selection".format(self.lbl_str),
                                style="odd.heading2.TLabel")
        self.header.grid(row=0, column=0)

        self.close_btn = ttk.Button(self,
                                    text="X",
                                    command=self.remove_frame,
                                    width=3,
                                    style="bad.TButton")
        self.close_btn.grid(row=0, column=1, sticky=tk.NE)

        if self.orient == tk.VERTICAL:
            self.paned_window = PanedWindowVertical(self,
                                                    background=background,
                                                    borderwidth=borderwidth,
                                                    relief=relief,
                                                    sashpad=sashpad,
                                                    sashrelief=sashrelief,
                                                    sashwidth=sashwidth,
                                                    disallow_dragging=disallow_dragging,
                                                    cursor=cursor,
                                                    opaqueresize=opaqueresize)
        elif self.orient == tk.HORIZONTAL:
            self.paned_window = PanedWindowHorizontal(self,
                                                      background=background,
                                                      borderwidth=borderwidth,
                                                      relief=relief,
                                                      sashpad=sashpad,
                                                      sashrelief=sashrelief,
                                                      sashwidth=sashwidth,
                                                      disallow_dragging=disallow_dragging,
                                                      cursor=cursor,
                                                      opaqueresize=opaqueresize)
        else:
            raise ValueError

        self.paned_window.grid(row=2, column=0, sticky=tk.NSEW, columnspan=2)

        self.add_btn = ttk.Button(self,
                                  text="Add",
                                  command=self.add_entry)
        self.add_btn.grid(row=3, column=0, sticky=tk.NSEW, columnspan=2)

        self.entry_dict = OrderedDict()
        self.entry_name_seed = 0
        self.bind("<Configure>", self.on_resize)
        self.selection_top_level = None

    # noinspection PyUnusedLocal
    # @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.header.configure(wraplength=self.winfo_width()-self.add_btn.winfo_reqwidth() + 30)

    @debug(lvl=logging.DEBUG, prefix='')
    def get_new_entry_name(self):
        if self.entry_name_seed < 10:
            entry_count_str = "0" + str(self.entry_name_seed)
        elif self.entry_name_seed < 100:
            entry_count_str = str(self.entry_name_seed)
        else:
            raise ValueError
        self.entry_name_seed += 1
        return "{}_{}".format(self.winfo_name(), entry_count_str)

    @debug(lvl=logging.DEBUG, prefix='')
    def add_entry(self, *args, **kwargs):
        self.paned_reset()
        entry_obj = PanedEntryFrame(master=self.paned_window,
                                    container=self,
                                    name=self.get_new_entry_name(),
                                    *args,
                                    **kwargs)
        self.entry_dict[entry_obj.winfo_name()] = {"entry_obj": entry_obj}
        entry_validation = (entry_obj.register(self.validate_selection),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        entry_obj.entry.config(
            validate='focusout',
            validatecommand=entry_validation
        )

        entry_obj.search_btn.config(command=lambda: self.search(entry_obj=entry_obj))
        entry_obj.close_btn.config(command=lambda: self.remove_entry(entry_obj=entry_obj))

        self.paned_populate()

    @debug(lvl=logging.DEBUG, prefix='')
    def get_dataset_query(self):
        filter_list = []
        for entry_subdict in self.entry_dict.values():
            entry_obj = entry_subdict["entry_obj"]
            if entry_obj.value != "":
                filter_list.append((self.dataset_key_col != entry_obj.value))
        if filter_list:
            return self.dataset_query.filter(and_(*filter_list))
        else:
            return self.dataset_query

    @debug(lvl=logging.DEBUG, prefix='')
    def search(self, entry_obj):
        if self.selection_top_level is not None:
            self.selection_top_level.destroy()
            self.selection_top_level = None
            self.search(entry_obj)
        else:
            entry_obj.value = SelectionToplevel(self,
                                                title="{} Selection Dialog".format(self.lbl_str),
                                                header="{} Selection".format(self.lbl_str),
                                                dataset_query=self.get_dataset_query()).selection
            entry_obj.entry.validate()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_selection(self,
                           action=None,
                           index=None,
                           value_if_allowed="",
                           prior_value=None,
                           text=None,
                           validation_type=None,
                           trigger_type=None,
                           widget_name=None):
        return True

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_entry(self,
                       entry_obj,
                       padx=3,
                       pady=3,
                       stretch='never',
                       sticky=tk.NSEW,
                       min_width=80,
                       min_height=40,
                       minsize=None,
                       width=None,
                       height=None,
                       after=None,
                       before=None,
                       *args,
                       **kwargs):
        if minsize is None:
            if self.orient == tk.HORIZONTAL:
                minsize = min_width
                if width is None or width < minsize:
                    width = minsize
                self.paned_window.add(entry_obj,
                                      padx=padx,
                                      pady=pady,
                                      stretch=stretch,
                                      sticky=sticky,
                                      minsize=minsize,
                                      width=width,
                                      after=after,
                                      before=before,
                                      *args,
                                      **kwargs)
            elif self.orient == tk.VERTICAL:
                minsize = min_height
                if height is None or height < minsize:
                    height = minsize
                self.paned_window.add(entry_obj,
                                      padx=padx,
                                      pady=pady,
                                      stretch=stretch,
                                      sticky=sticky,
                                      minsize=minsize,
                                      height=height,
                                      after=after,
                                      before=before,
                                      *args,
                                      **kwargs)
            else:
                raise ValueError
        else:
            if self.orient == tk.HORIZONTAL:
                if width is None or width < minsize:
                    width = minsize
                self.paned_window.add(entry_obj,
                                      padx=padx,
                                      pady=pady,
                                      stretch=stretch,
                                      sticky=sticky,
                                      minsize=minsize,
                                      width=width,
                                      after=after,
                                      before=before,
                                      *args,
                                      **kwargs)
            elif self.orient == tk.VERTICAL:
                if height is None or height < minsize:
                    height = minsize
                self.paned_window.add(entry_obj,
                                      padx=padx,
                                      pady=pady,
                                      stretch=stretch,
                                      sticky=sticky,
                                      minsize=minsize,
                                      height=height,
                                      after=after,
                                      before=before,
                                      *args,
                                      **kwargs)
            else:
                raise ValueError

    @debug(lvl=logging.DEBUG, prefix='')
    def paned_reset(self):
        keyword_list = ["after", "before", "height", "minsize", "padx", "pady", "sticky", "width", "stretch"]
        for pane in self.paned_window.panes():
            pane_widget = self.nametowidget(pane)
            pane_dict = {}
            for kword in keyword_list:
                if self.paned_window.panecget(pane, kword) not in (None, ""):
                    pane_dict[kword] = self.paned_window.panecget(pane, kword)
            if self.orient == tk.VERTICAL:
                pane_dict["height"] = pane_widget.winfo_height()
            elif self.orient == tk.HORIZONTAL:
                pane_dict["width"] = pane_widget.winfo_width()
            else:
                raise ValueError
            self.entry_dict[pane_widget.winfo_name()]["add_dict"] = pane_dict

        self.paned_window.remove_all()

    @debug(lvl=logging.DEBUG, prefix='')
    def paned_populate(self):
        for entry_key in self.entry_dict.keys():
            entry_obj = self.entry_dict[entry_key]["entry_obj"]
            entry_obj.sash_index = None
            entry_obj.sash_object = None
            add_dict = self.entry_dict[entry_key].get("add_dict")
            if add_dict is None:
                self.populate_entry(entry_obj=entry_obj)
            else:
                self.populate_entry(entry_obj=entry_obj, **add_dict)

    @debug(lvl=logging.DEBUG, prefix='')
    def remove_entry(self, entry_obj):
        self.paned_reset()

        if entry_obj.winfo_name() in self.entry_dict.keys():
            self.entry_dict.pop(entry_obj.winfo_name())
        else:
            raise ValueError

        self.paned_populate()

    @debug(lvl=logging.DEBUG, prefix='')
    def grid_frame(self,
                   minsize=40,
                   sticky=tk.NSEW,
                   stretch="always"):
        self.factor.sel_check_btn.state(['selected'])
        self.update_idletasks()
        width = self.winfo_reqwidth()
        Factor.root.paned_factor_criteria.add(self,
                                              width=width,
                                              minsize=minsize,
                                              sticky=sticky,
                                              stretch=stretch)

    @debug(lvl=logging.DEBUG, prefix='')
    def remove_frame(self):
        from cep_price_console.utils.gui_utils import parsegeometry
        self.factor.sel_check_btn.state(['!selected'])
        self.update_idletasks()
        width = self.winfo_width()
        Factor.root.paned_factor_criteria.remove(self)
        window_width, window_height, center_width, center_height = parsegeometry(Factor.root.geometry())
        Factor.root.geometry("{0}x{1}+{2}+{3}".format(window_width - width - 7,
                                                      window_height,
                                                      center_width,
                                                      center_height))

        obj_list = []
        for entry_subdict in self.entry_dict.values():
            entry_obj = entry_subdict["entry_obj"]
            obj_list.append(entry_obj)

        for entry_obj in obj_list:
            self.remove_entry(entry_obj=entry_obj)

    @classmethod
    @debug(lvl=logging.DEBUG, prefix='')
    def reset(cls, root=None):
        cls.root = root
        cls.dictionary = {}


# noinspection PyUnusedLocal
class PanedEntryFrame(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 master,
                 container,
                 name,
                 value="",
                 borderwidth=5,
                 cursor=None,
                 padding=0,
                 relief=tk.RIDGE,
                 style="odd.group.TFrame",
                 takefocus=True,
                 *args,
                 **kwargs):
        self.container = container
        value = value
        # noinspection PyArgumentList
        super().__init__(master,
                         name=name,
                         borderwidth=borderwidth,
                         cursor=cursor,
                         padding=padding,
                         relief=relief,
                         style=style,
                         takefocus=takefocus,
                         *args,
                         **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry_var.set(value)
        self.entry = ttk.Entry(self,
                               textvariable=self.entry_var)
        self.entry.state(['disabled'])
        self.entry.grid(row=0, column=0, sticky=tk.NSEW)

        self.search_btn = ttk.Button(self,
                                     text="Search")
        self.search_btn.grid(row=0, column=1, sticky=tk.NS)

        self.close_btn = ttk.Button(self,
                                    text="x",
                                    width=1,
                                    style="bad.TButton")
        self.close_btn.grid(row=0, column=2, sticky=tk.NE + tk.S)

        self.sash_index = None
        self.sash_object = None

    @property
    @debug(lvl=logging.NOTSET)
    def value(self):
        return self.entry_var.get()

    @value.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def value(self, val):
        self.entry_var.set(val)


class SelectionToplevel(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, header, dataset_query, title=None, *args, **kwargs):
        from cep_price_console.utils import config
        from cep_price_console.utils.mytkintertable import MyCanvas
        super().__init__(*args, **kwargs)

        if title:
            self.title(title)

        self.iconbitmap(config.FAVICON)
        self.master = master

        self.master.selection_top_level = self
        self.__selection = ""

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.header = ttk.Label(self,
                                style="odd.heading2.TLabel",
                                text=header,
                                wraplength=self.winfo_width())
        self.header.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)
        instr = ("Select an entry below by:\n"
                 "    1) Double-clicking on any cell of a row. \n"
                 "    2) Right-clicking on any cell of a row and choosing 'Select'\n"
                 "    3) Highlighting the row and pressing the 'Select' button below.\n"
                 "Right-click on a column to sort by a column.Filter records by right-clicking on any cell and "
                 "selecting 'Filter Records' Note: Due to a software bug, you cannot sort and filter data at the same "
                 "time.")
        self.instr = ttk.Label(self,
                               style="odd.dflt.TLabel",
                               text=instr,
                               wraplength=self.winfo_width(),
                               padding=5)
        self.instr.grid(row=1, column=0, sticky=tk.NSEW, columnspan=2)

        self.tkintertable_frame = ttk.Frame(self)
        self.tkintertable_frame.rowconfigure(1, weight=1)
        self.tkintertable_frame.columnconfigure(1, weight=1)
        self.tkintertable_frame.grid(row=2, column=0, sticky=tk.NSEW, columnspan=2)

        self.select_btn = ttk.Button(self,
                                     command=self.select,
                                     default=tk.ACTIVE,
                                     text="Select")
        self.select_btn.grid(row=3, column=0, sticky=tk.NE + tk.S)

        self.close_btn = ttk.Button(self,
                                    command=self.close,
                                    text="Cancel")
        self.close_btn.grid(row=3, column=1, sticky=tk.NE + tk.S)

        self.bind("<Return>", self.select, "+")
        self.bind("<Escape>", self.close, "+")
        self.bind("<Configure>", self.on_resize, "+")

        self.dataset_query = dataset_query
        # noinspection PyProtectedMember
        data = {row[0]: row._asdict() for row in self.dataset_query.all()}

        self.tkintertable_model = TableModel()
        self.tkintertable_model.importDict(data)

        self.tkintertable_table = MyCanvas(self.tkintertable_frame,
                                           model=self.tkintertable_model,
                                           read_only=False)
        self.tkintertable_table.createTableFrame()

        # self.grab_set()

        self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.geometry("+{}+{}".format(self.master.winfo_rootx() + 50,
                                      self.master.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def close(self, *args):
        self.master.focus_set()
        if hasattr(self.tkintertable_table, 'filterwin'):
            self.tkintertable_table.closeFilterFrame()
        self.destroy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def select(self, *args):
        self.selection = self.tkintertable_table.get_currentRecordName()

    @property
    @debug(lvl=logging.NOTSET)
    def selection(self):
        return self.__selection

    @selection.setter
    @debug(lvl=logging.DEBUG, prefix="")
    def selection(self, value):
        self.__selection = value
        self.withdraw()
        self.update_idletasks()
        self.close()

    # noinspection PyUnusedLocal
    def on_resize(self, event):
        self.instr.configure(wraplength=self.winfo_width())
        self.header.configure(wraplength=self.winfo_width())
