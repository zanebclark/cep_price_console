from cep_price_console.db_management.server_utils import mysql_login_required
from cep_price_console.utils.gui_utils import VerticalScrolledFrame, odd_background, OrderableListFrame
from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.variance_report.variance_date_options import DateOptionsFrame
from tkinter import filedialog, messagebox
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk
from itertools import combinations


class SalesVarianceView(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    @mysql_login_required
    def __init__(self, master, testing=False, **kwargs):
        from cep_price_console.variance_report.variance_model import SalesVarianceModel
        from cep_price_console.utils.unified_selection_view import UniversalSelectionFrame
        self.master = master
        self.testing = testing
        super().__init__(self.master, **kwargs)
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.model = SalesVarianceModel(self)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.nb = ttk.Notebook(self)

        self.selection_criteria = UniversalSelectionFrame(
            self.nb,
            show_contract=True,
            show_customer=True,
            show_cust_shipto=True,
            show_cust_category=True,
            show_product=True,
            show_product_line=True,
            show_price_group=True,
            show_primary_vendor=True,
            show_secondary_vendor=True,
            show_major_group=True,
        )
        self.nb.add(self.selection_criteria, text="Selection Criteria")

        self.report_options_frame = ReportOptions(self, self.nb)
        self.nb.add(self.report_options_frame, text="Reporting Options")

        self.formatting_options = FormattingOptions(self, self.nb)
        self.nb.add(self.formatting_options, text="Formatting Options")

        self.nb.grid(row=0, column=0, sticky=tk.NSEW)

        self.btn = ttk.Button(self,
                              text="Run",
                              command=self.run)
        self.btn.grid(row=1, column=0, sticky=tk.NSEW)
        self.selection_criteria.show()
        self.nb.bind('<<NotebookTabChanged>>', self.fuck_this)

    @debug(lvl=logging.DEBUG, prefix='')
    def fuck_this(self, event):
        self.report_options_frame.date_option_frame.on_resize(None)

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        try:
            self.master.menu_bar.delete("--Close--")
        except:
            pass
        self.selection_criteria.session.close()
        self.model.close()
        self.destroy()

    @debug(lvl=logging.DEBUG, prefix='')
    def pre_run(self):
        error_msg = []

        if not self.prod_list:
            error_msg.append("{:>22}: {}".format('Selection Criteria', "Product selection doesn't yield any results. "
                                                                       "Try a more broad selection"))
        if not self.cust_list:
            error_msg.append(
                "{:>22}: {}".format('Selection Criteria', "Customer selection doesn't yield any results. "
                                                          "Try a more broad selection"))
        if len(self.cust_list) > 40:
            error_msg.append(
                "{:>22}: {}".format('Selection Criteria', "Customer selection returns more than 40 customers. "
                                                          "Try a more narrow selection"))
        if self.date_item_combo is None:
            error_msg.append("{:>22}: {}".format('Reporting Options', 'Select date parameters.'))
        if self.model.fullpath is None:
            error_msg.append("{:>22}: {}".format('Formatting Options', 'Choose file destination.'))
        if len(self.model.col_list_metric) == 0:
            error_msg.append("{:>22}: {}".format(
                'Select Metric',
                'At least one of the following "metric" columns must be selected:\n{}'.format(
                    "\n".join([col.header for col in self.model.available_col_dict.values() if col.metric]))))
        if not self.model.include_summary and not self.model.include_individual:
            error_msg.append("{:>22}: {}".format(
                'Reporting Options',
                'You must select: \n'
                '1) Include months/quarters?\n'
                '2) Include yearly aggregate?\n'
                '3) Both of the above.'))

        if error_msg:
            if self.testing:
                self.__class__.logger.log(logging.DEBUG, "Run Failed. Error Message: {}".format(error_msg))
                self.close()
            else:
                messagebox.askokcancel(
                    "Additional Information Required",
                    "\n".join(error_msg),
                    parent=self
                )
                return None
        else:
            return None

    @debug(lvl=logging.DEBUG, prefix='')
    def run(self):
        if self.pre_run() is None:
            self.model.create_wb(self.prod_list, self.cust_shipto_list, self.cust_list)
            if not self.testing:
                messagebox.askokcancel(
                    "Success!",
                    "The workbook has been created!",
                    parent=self
                )
            self.close()
            # if self.testing:
            #     return self.model.get_master_df(prod_list=self.prod_list,
            #                                     cust_shipto_list=self.cust_shipto_list,
            #                                     cust_list=self.cust_list)
            # else:
            #     self.model.create_wb(self.prod_list, self.cust_shipto_list, self.cust_list)
            #     if not self.testing:
            #         messagebox.askokcancel(
            #             "Success!",
            #             "The workbook has been created!",
            #             parent=self
            #         )
            #     self.close()
        else:
            return None

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def prod_list(self):
        return self.selection_criteria.entity_prod.get_unified_sel()

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def cust_shipto_list(self):
        return self.selection_criteria.entity_cust.get_unified_sel()

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def cust_list(self):
        return self.selection_criteria.entity_cust.factor_dict["Cust_Num"].atomic_to_unit_list(
            self.cust_shipto_list
        )

    # region Date Item Combo ###########################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def date_item_combo(self):
        return self.model.date_item_combo

    @date_item_combo.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def date_item_combo(self, value):
        if value is not None:
            value.get_comparison_range_list()
        self.model.date_item_combo = value
    # endregion ########################################################################################################


class ReportOptions(VerticalScrolledFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, view, parent):
        self.view = view
        self.parent = parent
        super().__init__(self.parent,
                         relief=tk.RAISED,
                         padding=5,
                         style="odd.group.TFrame",
                         canvas_background=odd_background)
        self.interior.rowconfigure(0, weight=1)
        self.interior.columnconfigure(0, weight=1)
        self.interior.config(style="odd.group.TFrame")
        self.paned_interior = tk.PanedWindow(self.interior,
                                             orient=tk.VERTICAL,
                                             sashrelief=tk.FLAT,
                                             sashwidth=7,
                                             opaqueresize=False,
                                             bg=odd_background)
        self.paned_interior.grid(row=0, column=0, sticky=tk.NSEW)

        self.paned_top_interior = tk.PanedWindow(self.paned_interior,
                                                 orient=tk.HORIZONTAL,
                                                 sashrelief=tk.FLAT,
                                                 sashwidth=7,
                                                 opaqueresize=False,
                                                 bg=odd_background)
        self.paned_interior.add(self.paned_top_interior,
                                height=390,
                                stretch="never")

        self.paned_bottom_interior = tk.PanedWindow(self.paned_interior,
                                                    orient=tk.HORIZONTAL,
                                                    sashrelief=tk.FLAT,
                                                    sashwidth=7,
                                                    opaqueresize=False,
                                                    bg=odd_background)
        self.paned_interior.add(self.paned_bottom_interior,
                                height=150,
                                stretch="always")

        self.date_option_frame = DateOptionsFrame(self, self.paned_top_interior)
        self.paned_top_interior.add(self.date_option_frame,
                                    width=320,
                                    stretch="never")
        self.paned_top_interior.bind("<Configure>", lambda event: self.date_option_frame.on_resize(event), "+")

        self.comparison_frame = OrderableListFrame(
                    self.paned_top_interior,
                    title="Comparison Selection",
                    value_dict=self.view.model.available_comparisons,
                    allow_reorder=False,
                    allow_delete=False
                )
        self.paned_top_interior.add(self.comparison_frame,
                                    # height=200,
                                    stretch="always")
        self.column_available = AvailableColListFrame(
            parent=self.paned_bottom_interior,
            title="Available Columns",
            sel_col_frame=None,
            value_dict=self.view.model.available_col_dict,
            allow_reorder=False,
            allow_delete=True,
            allow_reset=False
        )
        self.paned_bottom_interior.add(self.column_available,
                                       width=300,
                                       stretch="never")

        self.column_selection = SelectedColListFrame(
            parent=self.paned_bottom_interior,
            title="Column Selection",
            value_dict=self.view.model.selected_col_dict,
            avail_col_frame=self.column_available
        )
        self.column_available.selected_col_frame = self.column_selection
        self.paned_bottom_interior.add(self.column_selection,
                                       stretch="always")
        self.column_available.update_idletasks()
        self.column_selection.update_idletasks()
        self.date_option_frame.on_resize(None)

    @debug(lvl=logging.DEBUG, prefix='')
    def run_test(self, comp_list=None, column_list=None, check_list=None):
        if comp_list is not None:
            for comparison in list(self.comparison_frame.item_dict.values()):
                if comparison.header in comp_list:
                    comparison.sel_check_btn.state(['selected'])
                else:
                    comparison.sel_check_btn.state(['!selected'])
        if column_list is not None:
            for column in list(self.column_available.item_dict.values()):
                if column.label in column_list:
                    self.column_available.delete_item(column)
            for column in list(self.column_selection.item_dict.values()):
                if column.label not in column_list:
                    self.column_selection.delete_item(column)
                if column.label in check_list:
                    column.sel_check_btn.state(['selected'])

        # grouping_list = [
        #     {"title": "Contract",
        #      "return_value": "Contract"},
        #
        #     {"title": "Customer",
        #      "return_value": "Customer"},
        #
        #     {"title": "Customer Ship To",
        #      "return_value": "Customer Ship To"},
        #
        #     {"title": "Customer Category",
        #      "return_value": "Customer Category"},
        #
        #     {"title": "Product",
        #      "return_value": "Product"},
        #
        #     {"title": "Product Line",
        #      "return_value": "Product Line"},
        #
        #     {"title": "Price Group",
        #      "return_value": "Price Group"},
        #
        #     {"title": "Primary Vendor",
        #      "return_value": "Primary Vendor"},
        #
        #     {"title": "Secondary Vendor",
        #      "return_value": "Secondary Vendor"},
        #
        #     {"title": "Major Group",
        #      "return_value": "Major Group"},
        # ]
        #
        # self.grouping_gui = OrderableListFrame(
        #     self.interior,
        #     title="Factor Grouping",
        #     value_list=grouping_list
        # )
        # self.grouping_gui.grid(row=3, column=0, sticky=tk.NSEW)


class FormattingOptions(VerticalScrolledFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, parent):
        self.view = view
        self.parent = parent
        super().__init__(self.parent,
                         relief=tk.RAISED,
                         padding=5,
                         style="odd.group.TFrame",
                         canvas_background=odd_background)
        self.interior.config(style="odd.group.TFrame")
        # self.interior.rowconfigure(0, weight=1)
        self.interior.columnconfigure(0, weight=1)
        self.header = ttk.Label(
            self.interior,
            text="Formatting Options: ",
            wraplength=20,
            style="odd.heading1.TLabel",
        )
        self.header.grid(row=0, column=0, sticky=tk.NW)

        self.filename_frame = ttk.Frame(self.interior, style="odd.group.TFrame")
        self.filename_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.filename_frame.columnconfigure(0, weight=1)

        self.filename_lbl = ttk.Label(
            self.filename_frame,
            text="Filepath ",
            style="odd.dflt.TLabel")
        self.filename_lbl.grid(row=0, column=0, columnspan=2, sticky=tk.EW)

        self.fullpath_var = tk.StringVar()

        fullpath_validation = (self.filename_frame.register(self.validate_fullpath),
                               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.filename_entry = ttk.Entry(
            self.filename_frame,
            textvariable=self.fullpath_var,
            validate='focusout',
            validatecommand=fullpath_validation
        )
        self.filename_entry.grid(row=1, column=0, sticky=tk.EW)

        self.filename_btn = ttk.Button(
            self.filename_frame,
            text="Browse",
            command=self.file_dialog
        )
        self.filename_btn.grid(row=1, column=1, sticky=tk.E)
        self.bind("<Configure>", self.on_resize, "+")
        self.filename_focus = False

    @debug(lvl=logging.DEBUG, prefix='')
    def run_test(self, filename):
        from cep_price_console.utils import config
        self.fullpath_var.set(config.MEDIA_PATH / "{}.xlsx".format(filename))
        self.filename_entry.validate()

    @debug(lvl=logging.DEBUG, prefix='')
    def file_dialog(self):
        filename_options = dict(
            title='Save Worksheet As',
            initialdir=os.path.expanduser('~'),
            initialfile=None,
            parent=self.view,
            filetypes=[('Excel Files', ['.xlsx']),
                       ("all files", "*.*")]
        )
        self.fullpath_var.set(tk.filedialog.asksaveasfilename(**filename_options))
        self.filename_entry.validate()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.NOTSET, prefix='')
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
            var_boolean = self.view.model.set_fullpath(value_if_allowed)
            if var_boolean:
                self.fullpath_var.set(self.view.model.fullpath)
                return True
            elif not var_boolean:
                self.fullpath_var.set("")
                return False
        else:
            return True

    # noinspection PyUnusedLocal
    def on_resize(self, event):
        # print(self.view.model.available_col_dict.keys())
        self._configure_canvas(None)
        self.header.configure(wraplength=self.interior.winfo_width())


class AvailableColListFrame(OrderableListFrame):
    def __init__(self,
                 parent,
                 title,
                 sel_col_frame,
                 value_dict=None,
                 allow_reorder=True,
                 allow_delete=True,
                 allow_reset=True):
        super().__init__(parent=parent, title=title, value_dict=value_dict, allow_reorder=allow_reorder,
                         allow_delete=allow_delete, allow_reset=allow_reset)
        self.selected_col_frame = sel_col_frame

    def add_item(self, key, item):
        super().add_item(key, item)
        item.inner_frame.grid_remove()
        item.delete_item.config(text="Add")

    def delete_item(self, list_item):
        list_item.grid_forget()
        item = self.item_dict.pop(list_item.key)
        self.selected_col_frame.add_item(key=item.key, item=item)
        self.selected_col_frame.grid_all()
        self.grid_all()


class SelectedColListFrame(OrderableListFrame):
    def __init__(self,
                 parent,
                 title,
                 avail_col_frame,
                 value_dict=None,
                 allow_reorder=True,
                 allow_delete=True,
                 allow_reset=True):
        super().__init__(parent=parent, title=title, value_dict=value_dict, allow_reorder=allow_reorder,
                         allow_delete=allow_delete, allow_reset=allow_reset)
        self.available_col_frame = avail_col_frame
        self.reset_btn.config(command=lambda: self.reset_both(value_dict=value_dict))

    @debug(lvl=logging.NOTSET, prefix='')
    def reset_both(self, value_dict):
        self.populate(value_dict=value_dict)
        self.available_col_frame.populate(self.available_col_frame.default_dict)

    @debug(lvl=logging.NOTSET, prefix='')
    def add_item(self, key, item):
        super().add_item(key=key, item=item)
        item.inner_frame.grid()
        item.delete_item.config(text="X")

    @debug(lvl=logging.DEBUG, prefix='')
    def delete_item(self, list_item):
        list_item.grid_forget()
        item = self.item_dict.pop(list_item.key)
        self.available_col_frame.add_item(key=item.key, item=item)
        self.available_col_frame.grid_all()
        self.grid_all()


logger = CustomAdapter(logging.getLogger(str(__name__)), None)


@debug(lvl=logging.DEBUG, prefix='')
def multiple_tester(
        master,
        filename,
        comparison_value,
        date_style_value,
        start_month_value,
        start_year_value,
        end_month_value,
        end_year_value,
        column_list,
        check_list=None,
        comp_list=None,
        include_summary=None,
        compare_summary=None,
        include_individual=None,
        compare_individual=None,
        vl_cntr_num=None,
        vl_cust_cat=None,
        vl_cust_num=None,
        vl_cust_num_shipto=None,
        vl_prod_num=None,
        vl_prod_line=None,
        vl_price_group_code=None,
        vl_primary_vend_num=None,
        vl_vend_num=None,
        vl_major_group=None):

    def recursive(combo_dict, return_list):
        try:
            key, value_list = combo_dict.popitem()
        except KeyError:
            count = 0
            for seed in return_list:
                count += 1
                logger.log(logging.DEBUG, "Dictionary Object ------------------------------")
                for k, v in seed.items():
                    logger.log(logging.DEBUG, "Key: {}  Value: {}".format(k, v))
                logger.log(logging.DEBUG, "Count: {}".format(count))
            return return_list
        else:
            new_return_list = []
            for seed_dict in return_list:
                # noinspection PyDictCreation
                for value in value_list:
                    spawned_dict = {**seed_dict}
                    spawned_dict[key] = value
                    new_return_list.append(spawned_dict)
            return recursive(combo_dict, new_return_list)

    param_dict = dict(**locals())

    for k, v in param_dict.items():
        logger.log(logging.NOTSET, "Key: {}  Value: {}".format(k, v))

    combination_dict = {}

    if include_summary is None:
        combination_dict["include_summary"] = [True, False]

    if compare_summary is None:
        combination_dict["compare_summary"] = [True, False]

    if include_individual is None:
        combination_dict["include_individual"] = [True, False]

    if compare_individual is None:
        combination_dict["compare_individual"] = [True, False]

    if check_list is None:
        check_list_avail = [
            "Price_Group_Code",
            "Primary_Vend",
            "Prod_Line"
        ]
        check_list_combinations = []
        for combo in [combinations(check_list_avail, count) for count in range(0, len(check_list_avail) + 1)]:
            for sub_combo in combo:
                check_list_combinations.append(list(sub_combo))
        combination_dict["check_list"] = check_list_combinations

    if comp_list is None:
        comp_list_avail = [
            "Variance",
            "Percentage Variance"
        ]
        comp_list_combinations = []
        for combo in [combinations(comp_list_avail, count) for count in range(0, len(comp_list_avail) + 1)]:
            for sub_combo in combo:
                comp_list_combinations.append(list(sub_combo))
        combination_dict["comp_list"] = comp_list_combinations

    # noinspection PyDictCreation
    # full_seed_dict = {**param_dict}
    # full_seed_dict["include_summary"] = True
    # full_seed_dict["compare_summary"] = True
    # full_seed_dict["include_individual"] = True
    # full_seed_dict["compare_individual"] = True
    # full_seed_dict["check_list"] = ["Price_Group_Code", "Primary_Vend", "Prod_Line"]
    # full_seed_dict["comp_list"] = ["Variance", "Percentage Variance"]
    # dict_list = [full_seed_dict]
    dict_list = []
    dict_list.extend(recursive(combo_dict=combination_dict, return_list=[param_dict]))

    seed_df = None
    for dict_obj in dict_list:
        view = SalesVarianceView(master, testing=True)

        view.selection_criteria.run_test(
            vl_cntr_num=dict_obj.get("vl_cntr_num"),
            vl_cust_cat=dict_obj.get("vl_cust_cat"),
            vl_cust_num=dict_obj.get("vl_cust_num"),
            vl_cust_num_shipto=dict_obj.get("vl_cust_num_shipto"),
            vl_prod_num=dict_obj.get("vl_prod_num"),
            vl_prod_line=dict_obj.get("vl_prod_line"),
            vl_price_group_code=dict_obj.get("vl_price_group_code"),
            vl_primary_vend_num=dict_obj.get("vl_primary_vend_num"),
            vl_vend_num=dict_obj.get("vl_vend_num"),
            vl_major_group=dict_obj.get("vl_major_group")
        )

        view.report_options_frame.date_option_frame.run_test(
            comparison_value=dict_obj.get("comparison_value"),
            date_style_value=dict_obj.get("date_style_value"),
            start_month_value=dict_obj.get("start_month_value"),
            start_year_value=dict_obj.get("start_year_value"),
            end_month_value=dict_obj.get("end_month_value"),
            end_year_value=dict_obj.get("end_year_value"),
            include_summary=dict_obj.get("include_summary"),
            compare_summary=dict_obj.get("compare_summary"),
            include_individual=dict_obj.get("include_individual"),
            compare_individual=dict_obj.get("compare_individual")
        )

        view.report_options_frame.run_test(
            comp_list=dict_obj.get("comp_list"),
            column_list=dict_obj.get("column_list"),
            check_list=dict_obj.get("check_list")
        )

        view.formatting_options.run_test(filename=dict_obj.get("filename"))

        df = view.run()
        if df is not None:
            if seed_df is None:
                seed_df = df
            logger.log(logging.DEBUG, df.to_string())
            # logger.log(logging.DEBUG, seed_df.eq(df, level="Prod. Num", axis=0).to_string())
            # logger.log(logging.DEBUG, seed_df.eq(df, level="Prod. Num", axis=1).to_string())
