import logging
import sys
import tkinter as tk
from tkinter import messagebox
from cep_price_console.utils.log_utils import CustomAdapter, debug

"""
I don't want to use slots for the functions. That would limit the user to opening up one of any given window at a time. 
I don't think this limitation makes sense. If I don't use slots, I need to name individual windows in some way. 

Windows Need: 
 - Unique name
    window name appended with some id number? 
    window class has a dictionary that keeps track of open windows and available window titles. 
    When a window is initialized, it is added to the class dictionary. 
    The key is the window's name. To generate the next available incrementation, append an incrementing counter to the 
        window name
    then, check the dictionary for key existence. If there's no key there now, make one. 
    You would be working up from 1 with every assignment. 
    
    There are windows that don't make sense to duplicate. 
    
    So, allow for toggling of duplication
    
    Each window should have a show, hide, close function. 
    The window's state should be saved in a StringVar so that the OptionMenu can keep track of it.
    
    Each window should have label text. Wait, that the name above. 
    
    Ok. Let's write this thing. 
"""


class Dashboard(tk.Tk):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, *args, **kwargs):
        super().__init__()
        from cep_price_console.utils import config
        self.config_gui_obj = config.config_gui_obj
        config.init_config()
        config.file_check()
        config.sect_mysql_database.test_creds()

        from cep_price_console.cntr_upload.Cont import CntrUploadCont
        from cep_price_console.old_unified_upload.view import View
        from cep_price_console.unified_upload.view import View as NewView
        from cep_price_console.utils.gui_utils import center_window, init_style
        from cep_price_console.price_list.price_list_2 import PriceList
        from cep_price_console.variance_report.variance_view import SalesVarianceView
        from cep_price_console.db_management.ARW_PRF import ArwPrfImporter

        self.init_logger()
        self.scheduled_init()
        # # TODO: Do I need this logic?
        # if log_setup_msg == "New File":
        #     log_setup_msg = setup_logging()

        init_style(self)
        # self.center_coords = []
        error_msg = []
        error_title = []

        self.title("{}".format(config.APP_TITLE))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        try:
            # Create a photo image from the logo, convert to a logo.
            self.img = tk.PhotoImage(master=self, file=config.ICON_FILE)
        except tk.TclError:
            # Gracefully handle being unable to locate the logo
            error_title.append("Logo File Missing")
            error_msg.append("Logo File Missing:\nUnable to locate {filename} in the following directory: {directory}"
                             .format(filename=config.ICON_FILE.name,
                                     directory=config.ICON_FILE.parent))
        else:
            self.logo = tk.Canvas(self, width=self.img.width(), height=self.img.height())
            self.logo.create_image(0, 0, image=self.img, anchor=tk.NW)
            self.logo.grid(row=0, column=0)  # sticky=tk.NW + tk.E)

        try:
            # Attempt to load the favicon
            self.iconbitmap(config.FAVICON)
        except tk.TclError:
            # Gracefully handle being unable to locate the favicon
            error_title.append("Favicon File Missing")
            error_msg.append("Favicon File Missing:\n"
                             "Unable to locate {filename} in the following directory: {directory}"
                             .format(filename=config.FAVICON.name,
                                     directory=config.FAVICON.parent))
        except Exception as ex:
            # Log the very strange errors
            template = "Favicon: An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.__class__.logger.error(message)

        # Hit the user with all of the errors that you racked up
        if error_title:
            error_title_string = ", ".join(error_title)

            error_str = ""
            for pos, error in enumerate(error_msg, 1):
                error_str += str(pos) + ": " + error
                if pos != len(error_msg):
                    error_str += "\n\n"
            messagebox.showwarning(
                error_title_string,
                error_str)

        self.menu_bar = tk.Menu(self)
        self.upload_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.upload_menu.add_command(
            label="Contract Upload Helper",
            command=lambda: self.grid_class(CntrUploadCont),
            state="disabled")
        self.upload_menu.add_command(
            label="Unified Upload",
            command=lambda: self.grid_class(View),
            state="disabled")
        self.upload_menu.add_command(
            label="New Unified Upload",
            command=lambda: self.grid_class(NewView),
            state="disabled")
        self.menu_bar.add_cascade(label="Upload", menu=self.upload_menu)

        self.reporting_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.reporting_menu.add_command(label="Sales Variance Report",
                                        command=lambda: self.grid_class(SalesVarianceView))
        # self.reporting_menu.add_command(label="Sales Variance Report Test",
        #                                 command=lambda: self.variance_test())
        self.reporting_menu.add_command(
            label="Price List",
            command=lambda: self.grid_class(PriceList),
            state="disabled")
        self.menu_bar.add_cascade(label="Reporting", menu=self.reporting_menu)

        self.manage_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.manage_server_menu = tk.Menu(self.manage_menu, tearoff=0)

        self.manage_server_menu.add_command(
            label="Drop/Recreate Database",
            command=lambda: ArwPrfImporter(relative_filename=config.ARW_PRF_MAPPING_FILE).recreate())
        self.manage_server_menu.add_command(
            label="Overwrite Mapping",
            command=lambda: ArwPrfImporter(relative_filename=config.ARW_PRF_MAPPING_FILE).write_mapping())
        self.manage_server_menu.add_command(
            label="Scheduled Script",
            command=lambda: ArwPrfImporter(relative_filename=config.ARW_PRF_MAPPING_FILE).scheduled_script())
        self.manage_server_menu.add_command(
            label="Daily Script",
            command=lambda: self.scheduled_daily())

        self.manage_menu.add_cascade(label="Manage Database", menu=self.manage_server_menu)

        self.manage_menu.add_command(label="Configure", command=lambda: self.show_config_gui())
        self.menu_bar.add_cascade(label="Management", menu=self.manage_menu)

        self.config(menu=self.menu_bar)

        self.update()
        self.current_frame = None

        center_window(win_obj=self, height=600, width=800)
        # self.open_windows_dict = {
        #     "one": "one",
        #     "two": "two",
        #     "three": "three",
        #     "four": "four",
        #     "five": "five",
        #     "six": "six",
        #     "seven": "seven",
        #     "eight": "eight",
        #     "nine": "nine",
        # }
        # self.open_windows_menu = None

        self.mainloop()

    @debug(lvl=logging.DEBUG, prefix='')
    def show_config_gui(self):
        self.current_frame = self.config_gui_obj.show(self)
        self.menu_bar.add_command(label="--Close--", command=lambda: self.close_class())

    @debug(lvl=logging.NOTSET, prefix='')
    def grid_class(self, new_class, grid_inst=False):
        if not grid_inst:
            self.current_frame = new_class(self)
            self.menu_bar.add_command(label="--Close--", command=lambda: self.close_class())
        else:
            self.current_frame = new_class
            self.current_frame.deiconify()
            self.current_frame.update_values()
            self.menu_bar.add_command(label="--Close--", command=lambda: self.current_frame.withdraw())

    @debug(lvl=logging.DEBUG, prefix='')
    def close_class(self):
        self.current_frame.close()
        self.menu_bar.delete("--Close--")

    @debug(lvl=logging.DEBUG, prefix='')
    def init_logger(self):
        from cep_price_console.utils.log_utils import setup_logging
        log_setup_msg = setup_logging()

        logger = logging.getLogger(str(__name__))
        logger.info('Log Initiated')
        for line in log_setup_msg:
            logger.log(logging.DEBUG, "    {}".format(line))

    @debug(lvl=logging.DEBUG, prefix='')
    def scheduled_init(self):
        from cep_price_console.db_management.ARW_PRF import ArwPrfImporter
        from cep_price_console.utils.arguments import arguments
        from cep_price_console.utils import config

        importer = ArwPrfImporter(relative_filename=config.ARW_PRF_MAPPING_FILE)

        if arguments.schedule_mode is not None:
            if arguments.schedule_mode == "recreate":
                importer.recreate()
            if arguments.schedule_mode == "update":
                importer.scheduled_script()
            if arguments.schedule_mode == "daily":
                self.scheduled_daily()
            sys.exit()

    @debug(lvl=logging.DEBUG, prefix='')
    def scheduled_daily(self):
        from cep_price_console.db_management.server_utils import mssql_test_creds
        if mssql_test_creds():
            from cep_price_console.db_management.server_utils import mysql_engine, mssql_session_maker
            from cep_price_console.db_management.ddi_data_warehouse import DDIDataWarehouse, aging_definition, \
                ar_history, branch, buy_line, cust_category, customer, division, inventory, inventory_history, \
                invoice_detail, invoice_header, invoice_summary, invoice_variance, price_group, prod_line, product, \
                purchase_order_detail, purchase_order_header, salesman, ship_to, ship_via, territory, user, vm, \
                vm_category, \
                warehouse, webcat
            from cep_price_console.db_management.mssql_database import MSSQL_Database
            table_list = [
                aging_definition,
                ar_history,
                branch,
                buy_line,
                cust_category,
                customer,
                division,
                inventory,
                inventory_history,
                invoice_detail,
                invoice_header,
                invoice_summary,
                invoice_variance,
                price_group,
                prod_line,
                product,
                purchase_order_detail,
                purchase_order_header,
                salesman,
                ship_to,
                ship_via,
                territory,
                user,
                vm,
                vm_category,
                warehouse,
                webcat]
            DDIDataWarehouse.metadata.drop_all(tables=table_list)
            DDIDataWarehouse.metadata.create_all(tables=table_list)

            mssql_session = mssql_session_maker()

            for table_obj in MSSQL_Database.metadata.tables.values():
                query_first = mssql_session.query(table_obj).first()
                if query_first is not None:
                    query = mssql_session.query(table_obj)
                    # noinspection PyProtectedMember
                    mysql_engine.execute(
                        DDIDataWarehouse.metadata.tables[
                            "DDIDataWarehouse.{}".format(table_obj.name)].insert(),
                        [row._asdict() for row in query]
                    )
        else:
            self.logger.error("Some error", exc_true=True)
            raise ValueError

    @debug(lvl=logging.DEBUG, prefix='')
    def variance_test(self):
        from cep_price_console.variance_report.variance_view import multiple_tester
        multiple_tester(
            self,
            comparison_value=1,
            date_style_value=1,
            # start_month_value="1017",
            # end_month_value="0719",
            start_month_value="Jan",
            start_year_value="2017",
            end_month_value="Mar",
            end_year_value="2019",
            include_summary=True,
            compare_summary=True,
            include_individual=False,
            compare_individual=False,
            column_list=[
                # Non-Metric, Grouping
                "Price_Group_Code",
                "Primary_Vend",
                "Prod_Line",

                # Non-Metric
                # "C1_Cost",
                # "Cust_Part_Num",
                # "Desc_Full",
                # "Display_UOM",
                # "L1_Price",
                # "Mfg_No",
                # "Price_UOM",
                # "Primary_Vend_Part_Num",
                "Prod_Num",
                # "Purch_UOM",
                # "Status",
                # "UOM_Factor_Desc"
                # "UPC",

                # Metric
                # "Commission",
                # "Cost",
                # "GL_Cost",
                # "GL_Profit",
                # "Original_Quantity",
                # "Profit",
                "Quantity_Shipped",
                "Revenue",
                # "Salesman_Cost",
                # "Salesman_Profit"
            ],
            check_list=[
                # "Price_Group_Code",
                "Primary_Vend",
                # "Prod_Line"
            ],
            comp_list=[
                "Variance",
                "Percentage Variance"
            ],
            filename="error_check",
            # vl_cntr_num=["0001229"],
            # vl_cust_cat=["ENTG"],
            vl_cust_num=["0001229", "0001178"],
            # vl_cust_num_shipto=["0001015_00000002"],
            # vl_prod_num=["BOYM-MVLP-F11B"],
            # vl_prod_line=["SAFE"],
            # vl_price_group_code=["SoloTest"],
            vl_primary_vend_num=["00374"],
            # vl_vend_num=["00374"],
            # vl_major_group=["Test"]
        )

    # @debug(lvl=logging.DEBUG, prefix='')
    # def open_window(self):
    #     if len(self.open_windows_dict.values()) == 0:
    #         pass
    #     else:
    #         self.open_windows_menu = tk.Menu(self.menu_bar, tearoff=0)
    #
    #         for window in self.open_windows_dict.values():
    #             submenu = tk.Menu(self.open_windows_menu, tearoff=0)
    #             submenu.add_radiobutton(label="{}_thing_1".format(window))
    #             submenu.add_radiobutton(label="{}_thing_2".format(window))
    #             submenu.add_radiobutton(label="{}_thing_3".format(window))
    #             submenu.add_radiobutton(label="{}_thing_4".format(window))
    #             submenu.add_radiobutton(label="{}_thing_5".format(window))
    #             self.open_windows_menu.add_cascade(label="submenu", menu=submenu)
    #         self.menu_bar.add_cascade(label="Open Windows", menu=self.open_windows_menu)

# class WindowedFrame(VerticalScrolledFrame):
#     logger = CustomAdapter(logging.getLogger(str(__name__)), None)
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def __init__(self, master, height=None, width=None, *args, **kwargs):
#         self.master = master
#         super().__init__(self.master, height=None, width=None, *args, **kwargs)
#         self.grid(row=0, column=0, sticky=tk.NW+tk.E)
#         self.interior.columnconfigure(0, weight=1)
#         self.interior.rowconfigure(0, weight=1)
#
