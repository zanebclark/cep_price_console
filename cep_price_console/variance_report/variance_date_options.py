import logging
import tkinter as tk
import tkinter.ttk as ttk
import datetime
import math
import calendar
from dateutil.relativedelta import relativedelta
from cep_price_console.utils.gui_utils import VerticalScrolledFrame, odd_background
from cep_price_console.utils.log_utils import CustomAdapter, debug
from tkinter import messagebox


class DateOptionsFrame(VerticalScrolledFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent):
        self.report_options = report_options
        self.parent = parent
        super().__init__(self.parent,
                         relief=tk.RAISED,
                         padding=5,
                         style="odd.group.TFrame",
                         canvas_background=odd_background)
        self.interior.config(style="odd.group.TFrame")
        self.interior.rowconfigure(16, weight=1)
        self.interior.columnconfigure(0, weight=1)

        self.header = ttk.Label(
            self.interior,
            text="Date Options: ",
            wraplength=20,
            style="odd.heading2.TLabel",
        )
        self.header.grid(row=0, column=0, sticky=tk.NW)

        sep = ttk.Separator(self.interior)
        sep.grid(row=1, column=0, sticky=tk.EW)

        self.comparison_style_label = ttk.Label(
            self.interior,
            text="Comparison Style: ",
            wraplength=20,
            style="odd.heading3.TLabel",
        )
        self.comparison_style_label.grid(row=2, column=0, sticky=tk.NW)

        self.comparison_style_var = tk.IntVar()
        self.comparison_style_radio_1 = ttk.Radiobutton(
            self.interior,
            text="Month/Quarter over Month/Quarter",
            variable=self.comparison_style_var,
            value=0,
            style="odd.dflt.TRadiobutton",
            command=lambda: self.switch_date_style()
        )
        self.comparison_style_radio_1.grid(row=3, column=0, sticky=tk.NW)

        self.comparison_style_radio_2 = ttk.Radiobutton(
            self.interior,
            text="Year over Year",
            variable=self.comparison_style_var,
            value=1,
            style="odd.dflt.TRadiobutton",
            command=lambda: self.switch_date_style()
        )
        self.comparison_style_radio_2.grid(row=4, column=0, sticky=tk.NW)

        sep = ttk.Separator(self.interior)
        sep.grid(row=5, column=0, sticky=tk.EW)

        self.date_style_label = ttk.Label(
            self.interior,
            text="Selection:",
            wraplength=20,
            style="odd.heading3.TLabel",
        )
        self.date_style_label.grid(row=6, column=0, sticky=tk.NW)

        self.date_style_var = tk.IntVar()
        self.date_style_var.set(1)

        self.date_style_radio_2 = ttk.Radiobutton(
            self.interior,
            text="Month",
            variable=self.date_style_var,
            value=1,
            style="odd.dflt.TRadiobutton",
            command=lambda: self.switch_date_style()
        )
        self.date_style_radio_2.grid(row=7, column=0, sticky=tk.NW)

        self.date_style_radio_3 = ttk.Radiobutton(
            self.interior,
            text="Quarter",
            variable=self.date_style_var,
            value=2,
            style="odd.dflt.TRadiobutton",
            command=lambda: self.switch_date_style()
        )
        self.date_style_radio_3.grid(row=8, column=0, sticky=tk.NW)

        self.date_style_radio_4 = ttk.Radiobutton(
            self.interior,
            text="Year",
            variable=self.date_style_var,
            value=3,
            style="odd.dflt.TRadiobutton",
            command=lambda: self.switch_date_style()
        )
        self.date_style_radio_4.grid(row=9, column=0, sticky=tk.NW)

        sep = ttk.Separator(self.interior)
        sep.grid(row=10, column=0, sticky=tk.EW)

        self.include_summary_check_btn = ttk.Checkbutton(
            self.interior,
            padding=5,
            text="Include yearly aggregate? ",
            command=self.checkbox_logic,
            style="odd.dflt.TCheckbutton"
        )
        self.include_summary_check_btn.state(['!alternate', 'selected'])
        self.include_summary_check_btn.grid(row=11, column=0, sticky=tk.NW)

        self.compare_summary_check_btn = ttk.Checkbutton(
            self.interior,
            padding=5,
            text="Compare yearly aggregate? ",
            command=self.checkbox_logic,
            style="odd.dflt.TCheckbutton"
        )
        self.compare_summary_check_btn.state(['!alternate', 'selected'])
        self.compare_summary_check_btn.grid(row=12, column=0, sticky=tk.NW)

        self.include_individual_check_btn = ttk.Checkbutton(
            self.interior,
            padding=5,
            text="Include months/quarters?",
            command=self.checkbox_logic,
            style="odd.dflt.TCheckbutton"
        )
        self.include_individual_check_btn.state(['!alternate', 'selected'])
        self.include_individual_check_btn.grid(row=13, column=0, sticky=tk.NW)

        self.compare_individual_check_btn = ttk.Checkbutton(
            self.interior,
            padding=5,
            text="Compare months/quarters?",
            command=self.checkbox_logic,
            style="odd.dflt.TCheckbutton"
        )
        self.compare_individual_check_btn.state(['!alternate', '!selected'])
        self.compare_individual_check_btn.grid(row=14, column=0, sticky=tk.NW)

        sep = ttk.Separator(self.interior)
        sep.grid(row=15, column=0, sticky=tk.EW)

        self.month_frame = AcctRangeFrameMonth(self, self.interior)
        self.month_frame.grid(row=16, column=0, columnspan=2, sticky=tk.NW)

        self.month_double_frame = AcctDoubleRangeFrameMonth(self, self.interior)
        self.month_double_frame.grid(row=16, column=0, columnspan=2, sticky=tk.NW)

        self.quarter_frame = AcctRangeFrameQuarter(self, self.interior)
        self.quarter_frame.grid(row=16, column=0, columnspan=2, sticky=tk.NW)

        self.quarter_double_frame = AcctDoubleRangeFrameQuarter(self, self.interior)
        self.quarter_double_frame.grid(row=16, column=0, columnspan=2, sticky=tk.NW)

        self.year_frame = AcctRangeFrameYear(self, self.interior)
        self.year_frame.grid(row=16, column=0, columnspan=2, sticky=tk.NW)

        self.switch_date_style()

        self.bind("<Configure>", self.on_resize, "+")

    @debug(lvl=logging.NOTSET, prefix='')
    def checkbox_logic(self):
        if 'selected' in self.include_summary_check_btn.state():
            self.compare_summary_check_btn.state(['!disabled'])
            self.report_options.view.model.include_summary = True
        elif 'selected' not in self.include_summary_check_btn.state():
            self.compare_summary_check_btn.state(['disabled', '!selected'])
            self.report_options.view.model.include_summary = False

        if 'selected' in self.compare_summary_check_btn.state():
            self.report_options.view.model.compare_summary = True
        elif 'selected' not in self.compare_summary_check_btn.state():
            self.report_options.view.model.compare_summary = False

        if 'selected' in self.include_individual_check_btn.state():
            self.compare_individual_check_btn.state(['!disabled'])
            self.report_options.view.model.include_individual = True
        elif 'selected' not in self.include_individual_check_btn.state():
            self.compare_individual_check_btn.state(['disabled', '!selected'])
            self.report_options.view.model.include_individual = False

        if 'selected' in self.compare_individual_check_btn.state():
            self.report_options.view.model.compare_individual = True
        elif 'selected' not in self.compare_individual_check_btn.state():
            self.report_options.view.model.compare_individual = False

    @debug(lvl=logging.NOTSET, prefix='')
    def run_test(self,
                 comparison_value,
                 date_style_value,
                 start_month_value,
                 end_month_value,
                 include_summary,
                 compare_summary,
                 include_individual,
                 compare_individual,
                 start_year_value=None,
                 end_year_value=None):
        if comparison_value not in [0, 1]:  # comparison_var_list
            messagebox.askokcancel(
                "Critical Error",
                "Unknown comparison_value: {}. Please restart the application.".format(comparison_value)
            )
            raise ValueError
        self.comparison_style_var.set(comparison_value)

        if date_style_value not in [1, 2, 3]:  # date_style_list
            messagebox.askokcancel(
                "Critical Error",
                "Unknown date_style_value: {}. Please restart the application.".format(date_style_value)
            )
            raise ValueError
        self.date_style_var.set(date_style_value)

        self.switch_date_style()

        start_month_var = None
        start_year_var = None
        end_month_var = None
        end_year_var = None

        if comparison_value == 0:  # "Month/Quarter over Month/Quarter
            if date_style_value == 1:  # "Month (Acct. Period)"
                start_month_var = self.month_frame.start_month_value
                end_month_var = self.month_frame.end_month_value
            elif date_style_value == 2:  # "Quarter (Acct. Period)"
                start_month_var = self.quarter_frame.start_month_value
                end_month_var = self.quarter_frame.end_month_value
            elif date_style_value == 3:  # "Year (Acct. Period)"
                start_month_var = self.year_frame.start_month_value
                end_month_var = self.year_frame.end_month_value
        elif comparison_value == 1:  # "Year over Year"
            if date_style_value == 1:  # "Month (Acct. Period)"
                start_month_var = self.month_double_frame.start_month_value
                start_year_var = self.month_double_frame.start_year_value
                end_month_var = self.month_double_frame.end_month_value
                end_year_var = self.month_double_frame.end_year_value
            elif date_style_value == 2:  # "Quarter (Acct. Period)"
                start_month_var = self.quarter_double_frame.start_month_value
                start_year_var = self.quarter_double_frame.start_year_value
                end_month_var = self.quarter_double_frame.end_month_value
                end_year_var = self.quarter_double_frame.end_year_value
            elif date_style_value == 3:  # "Year (Acct. Period)"
                messagebox.askokcancel(
                    "Critical Error",
                    "Year over Year not allowed with Year. Please restart the application."
                )
                raise ValueError

        if start_month_var is not None:
            start_month_var.set(start_month_value)
        if end_month_var is not None:
            end_month_var.set(end_month_value)
        if start_year_var is not None:
            start_year_var.set(start_year_value)
        if end_year_var is not None:
            end_year_var.set(end_year_value)

        if include_summary:
            self.include_summary_check_btn.state(['!alternate', 'selected'])
        else:
            self.include_summary_check_btn.state(['!alternate', '!selected'])

        if compare_summary:
            self.compare_summary_check_btn.state(['!alternate', 'selected'])
        else:
            self.compare_summary_check_btn.state(['!alternate', '!selected'])

        if include_individual:
            self.include_individual_check_btn.state(['!alternate', 'selected'])
        else:
            self.include_individual_check_btn.state(['!alternate', '!selected'])

        if compare_individual:
            self.compare_individual_check_btn.state(['!alternate', 'selected'])
        else:
            self.compare_individual_check_btn.state(['!alternate', '!selected'])
        self.checkbox_logic()

    @debug(lvl=logging.NOTSET, prefix='')
    def switch_date_style(self):
        if self.comparison_style_var.get() == 0:  # "Month/Quarter over Month/Quarter
            self.date_style_radio_4.state(["!disabled"])
            self.month_double_frame.ungrid()
            self.quarter_double_frame.ungrid()
            if self.date_style_var.get() == 1:  # "Month (Acct. Period)"
                self.month_frame.regrid()
                self.quarter_frame.ungrid()
                self.year_frame.ungrid()
            elif self.date_style_var.get() == 2:  # "Quarter (Acct. Period)"
                self.month_frame.ungrid()
                self.quarter_frame.regrid()
                self.year_frame.ungrid()
            elif self.date_style_var.get() == 3:  # "Year (Acct. Period)"
                self.month_frame.ungrid()
                self.quarter_frame.ungrid()
                self.year_frame.regrid()
            else:
                messagebox.askokcancel(
                    "Critical Error",
                    "Unknown date_style_var: {}. Please restart the application.".format(self.date_style_var.get())
                )
                raise ValueError
        elif self.comparison_style_var.get() == 1:  # "Year over Year"
            self.date_style_radio_4.state(["disabled"])
            self.month_frame.ungrid()
            self.quarter_frame.ungrid()
            self.year_frame.ungrid()
            if self.date_style_var.get() == 1:  # "Month (Acct. Period)"
                self.month_double_frame.regrid()
                self.quarter_double_frame.ungrid()
            elif self.date_style_var.get() == 2:  # "Quarter (Acct. Period)"
                self.month_double_frame.ungrid()
                self.quarter_double_frame.regrid()
            elif self.date_style_var.get() == 3:  # "Year (Acct. Period)"
                messagebox.askokcancel(
                    "Critical Error",
                    "Year over Year not allowed with Year. Please restart the application."
                )
                raise ValueError
            else:
                messagebox.askokcancel(
                    "Critical Error",
                    "Unknown date_style_var: {}. Please restart the application.".format(self.date_style_var.get()),
                )
                raise ValueError
        else:
            messagebox.askokcancel(
                "Critical Error",
                "Unknown comparison_style_var: {}. Please restart the application.".format(
                    self.comparison_style_var.get()
                ),
            )
            raise ValueError
        self._configure_canvas(None)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def on_resize(self, event):
        self.__class__.logger.log(logging.DEBUG, "width: {}".format(self.interior.winfo_width()))
        self.header.configure(wraplength=self.interior.winfo_width())
        self.comparison_style_label.configure(wraplength=self.interior.winfo_width())
        self.date_style_label.configure(wraplength=self.interior.winfo_width())


class AcctRangeFrame(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        self.report_options = report_options
        self.view = self.report_options.report_options.view
        self.parent = parent
        super().__init__(self.parent,
                         relief=tk.RAISED,
                         style="even.group.TFrame",
                         padding=5,
                         **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.start_month_value = tk.StringVar()
        self.start_month_value.trace_add("write", self.update_values)

        self.start_month_label = ttk.Label(
            self,
            style="even.dflt.TLabel",
            wraplength=2
        )
        self.start_month_label.grid(row=0, column=0, sticky=tk.EW)

        self.start_month_combobox = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.start_month_value
        )
        self.start_month_combobox.grid(row=1, column=0, sticky=tk.EW)

        self.end_month_value = tk.StringVar()
        self.end_month_value.trace_add("write", self.update_values)

        self.end_month_label = ttk.Label(
            self,
            style="even.dflt.TLabel",
            wraplength=2
        )
        self.end_month_label.grid(row=0, column=1, sticky=tk.EW)

        self.end_month_combobox = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.end_month_value
        )
        self.end_month_combobox.grid(row=1, column=1, sticky=tk.EW)

        self.bind("<Configure>", self.on_resize, "+")

        self.month_value_dict = None

    @debug(lvl=logging.NOTSET, prefix='')
    def init_value_dict(self):
        raise NotImplementedError

    @debug(lvl=logging.NOTSET, prefix='')
    def update_values(self, var_name=None, _=None, mode=None):
        start_month_item = self.month_value_dict[self.start_month_value.get()]
        end_month_item = self.month_value_dict[self.end_month_value.get()]

        if start_month_item is None and end_month_item is None:
            self.end_month_combobox.config(values=list(self.month_value_dict.keys()))
            self.start_month_combobox.config(values=list(self.month_value_dict.keys()))
        elif end_month_item is None:
            end_month_value_list = [""]
            for dateitem in self.month_value_dict.values():
                if dateitem is not None:
                    if dateitem.start_date > start_month_item.end_date:
                        end_month_value_list.append(str(dateitem))
            self.end_month_combobox.config(values=end_month_value_list)

            self.start_month_combobox.config(values=list(self.month_value_dict.keys()))
        elif start_month_item is None:
            self.end_month_combobox.config(values=list(self.month_value_dict.keys()))

            start_month_value_list = [""]
            for dateitem in self.month_value_dict.values():
                if dateitem is not None:
                    if dateitem.end_date < end_month_item.start_date:
                        start_month_value_list.append(str(dateitem))
            self.start_month_combobox.config(values=start_month_value_list)
        elif start_month_item is not None and end_month_item is not None:
            self.end_month_combobox.config(values=list(self.month_value_dict.keys()))
            self.start_month_combobox.config(values=list(self.month_value_dict.keys()))

    @debug(lvl=logging.NOTSET, prefix='')
    def regrid(self):
        self.view.date_item_combo = None

        self.grid()
        self.start_month_value.set('')
        self.end_month_value.set('')

    @debug(lvl=logging.NOTSET, prefix='')
    def ungrid(self):
        self.grid_remove()
        self.start_month_value.set('')
        self.end_month_value.set('')

    # noinspection PyUnusedLocal
    def on_resize(self, event):
        self.start_month_label.configure(wraplength=self.start_month_combobox.winfo_width() - 10)
        self.end_month_label.configure(wraplength=self.end_month_combobox.winfo_width() - 10)


class AcctSingleRangeFrame(AcctRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.init_value_dict()
        self.update_values()

    @debug(lvl=logging.NOTSET, prefix='')
    def update_values(self, var_name=None, _=None, mode=None):
        super().update_values(var_name, _, mode)
        start_month_item = self.month_value_dict[self.start_month_value.get()]
        end_month_item = self.month_value_dict[self.end_month_value.get()]
        if start_month_item is not None and end_month_item is not None:
            self.view.date_item_combo = MonthOverMonthCombo(
                start_item=start_month_item,
                end_item=end_month_item
            )


class AcctDoubleRangeFrame(AcctRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.start_year_value = tk.StringVar()
        self.start_year_value.trace_add("write", self.update_values)

        self.start_year_label = ttk.Label(
            self,
            style="even.dflt.TLabel",
            wraplength=2
        )
        self.start_year_label.grid(row=0, column=2, sticky=tk.EW)

        self.start_year_combobox = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.start_year_value
        )
        self.start_year_combobox.grid(row=1, column=2, sticky=tk.EW)

        self.end_year_value = tk.StringVar()
        self.end_year_value.trace_add("write", self.update_values)

        self.end_year_label = ttk.Label(
            self,
            style="even.dflt.TLabel",
            wraplength=2
        )
        self.end_year_label.grid(row=0, column=3, sticky=tk.EW)

        self.end_year_combobox = ttk.Combobox(
            self,
            state="readonly",
            textvariable=self.end_year_value
        )
        self.end_year_combobox.grid(row=1, column=3, sticky=tk.EW)
        self.year_value_dict = None
        self.init_value_dict()
        self.update_values()

    @debug(lvl=logging.NOTSET, prefix='')
    def update_values(self, var_name=None, _=None, mode=None):
        super().update_values(var_name, _, mode)
        start_year_item = self.year_value_dict[self.start_year_value.get()]
        end_year_item = self.year_value_dict[self.end_year_value.get()]

        if start_year_item is None and end_year_item is None:
            self.end_year_combobox.config(values=list(self.year_value_dict.keys()))
            self.start_year_combobox.config(values=list(self.year_value_dict.keys()))
        elif end_year_item is None:
            end_year_value_list = [""]
            for dateitem in self.year_value_dict.values():
                if dateitem is not None:
                    if dateitem.start_date > start_year_item.end_date:
                        end_year_value_list.append(str(dateitem))
            self.end_year_combobox.config(values=end_year_value_list)

            self.start_year_combobox.config(values=list(self.year_value_dict.keys()))
        elif start_year_item is None:
            self.end_year_combobox.config(values=list(self.year_value_dict.keys()))

            start_year_value_list = [""]
            for dateitem in self.year_value_dict.values():
                if dateitem is not None:
                    if dateitem.end_date < end_year_item.start_date:
                        start_year_value_list.append(str(dateitem))
            self.start_year_combobox.config(values=start_year_value_list)
        elif start_year_item is not None and end_year_item is not None:
            self.end_month_combobox.config(values=list(self.month_value_dict.keys()))
            self.start_month_combobox.config(values=list(self.month_value_dict.keys()))

        start_month_item = self.month_value_dict[self.start_month_value.get()]
        end_month_item = self.month_value_dict[self.end_month_value.get()]
        if (
                start_month_item is not None and
                end_month_item is not None and
                start_year_item is not None and
                end_year_item is not None
        ):
            self.view.date_item_combo = YearOverYearCombo(
                start_month_item=start_month_item,
                end_month_item=end_month_item,
                start_year_item=start_year_item,
                end_year_item=end_year_item
            )

    # noinspection PyUnusedLocal
    def on_resize(self, event):
        super().on_resize(event)
        self.start_year_label.configure(wraplength=self.start_year_combobox.winfo_width() - 10)
        self.end_year_label.configure(wraplength=self.end_year_combobox.winfo_width() - 10)

    @debug(lvl=logging.NOTSET, prefix='')
    def regrid(self):
        super().regrid()
        self.start_year_value.set('')
        self.end_year_value.set('')


class AcctRangeFrameMonth(AcctSingleRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.start_month_label.config(text="Start Month/Year")
        self.end_month_label.config(text="End Month/Year")

    @debug(lvl=logging.DEBUG, prefix='')
    def init_value_dict(self):
        self.month_value_dict = {"": None}
        for year in range(2016, datetime.datetime.now().year + 1):
            for month in range(1, 13):
                dateitem = MonthItem(month=month, year=year)
                if dateitem.start_date < datetime.datetime.now():
                    self.month_value_dict[str(dateitem)] = dateitem


class AcctDoubleRangeFrameMonth(AcctDoubleRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.start_month_label.config(text="Start Month")
        self.end_month_label.config(text="End Month")
        self.start_year_label.config(text="Start Year")
        self.end_year_label.config(text="End Year")

    @debug(lvl=logging.NOTSET, prefix='')
    def init_value_dict(self):
        self.month_value_dict = {"": None}
        self.year_value_dict = {"": None}
        for year in range(2016, datetime.datetime.now().year + 1):
            dateitem = YearItem(year=year)
            self.year_value_dict[str(dateitem)] = dateitem
        for month in range(1, 13):
            dateitem = MonthAloneItem(month=month)
            self.month_value_dict[str(dateitem)] = dateitem


class AcctDoubleRangeFrameQuarter(AcctDoubleRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.start_month_label.config(text="Start Quarter")
        self.end_month_label.config(text="End Quarter")
        self.start_year_label.config(text="Start Year")
        self.end_year_label.config(text="End Year")

    @debug(lvl=logging.NOTSET, prefix='')
    def init_value_dict(self):
        self.month_value_dict = {"": None}
        self.year_value_dict = {"": None}
        for year in range(2016, datetime.datetime.now().year + 1):
            dateitem = YearItem(year=year)
            self.year_value_dict[str(dateitem)] = dateitem
        for quarter in range(1, 5):
            dateitem = QuarterAloneItem(quarter=quarter)
            self.month_value_dict[str(dateitem)] = dateitem


class AcctRangeFrameQuarter(AcctSingleRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.start_month_label.config(text="Start Qtr./Year")
        self.end_month_label.config(text="End Qtr./Year")

    @debug(lvl=logging.NOTSET, prefix='')
    def init_value_dict(self):
        self.month_value_dict = {"": None}
        for year in range(2016, datetime.datetime.now().year + 1):
            for quarter in range(1, 5):
                dateitem = QuarterItem(quarter=quarter, year=year)
                if dateitem.start_date < datetime.datetime.now():
                    self.month_value_dict[str(dateitem)] = dateitem


class AcctRangeFrameYear(AcctSingleRangeFrame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, report_options, parent, *args, **kwargs):
        super().__init__(report_options, parent, *args, **kwargs)
        self.start_month_label.config(text="Start Year")
        self.end_month_label.config(text="End Year")

    @debug(lvl=logging.NOTSET, prefix='')
    def init_value_dict(self):
        self.month_value_dict = {"": None}
        for year in range(2016, datetime.datetime.now().year + 1):
            dateitem = YearItem(year=year)
            if dateitem.start_date < datetime.datetime.now():
                self.month_value_dict[str(dateitem)] = dateitem


class DateItem(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # when do my values start? Check MSSQL db for earliest date, today = latest date
    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, day=None, month=None, quarter=None, year=None):
        self.__day = None
        self.__month = None
        self.__quarter = None
        self.__year = None
        self.day = day
        self.month = month
        self.quarter = quarter
        self.year = year
        self.date_type = None

    # region Value #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def day(self):
        return self.__day

    @day.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def day(self, value):
        if value is not None:
            self.__day = value
            self.__month = value.month
            self.__quarter = math.ceil(value.month / 3)
            self.__year = value.year

    # endregion ########################################################################################################

    # region Value #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def month(self):
        return self.__month

    @month.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def month(self, value):
        if value is not None:
            if value in range(1, 13):
                self.__month = value
                self.__quarter = math.ceil(value / 3)
            else:
                messagebox.askokcancel(
                    "Critical Error",
                    "Unknown Date Item Value: {}. Please restart the application.".format(value),
                )
                raise ValueError

    # endregion ########################################################################################################

    # region Value #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def quarter(self):
        return self.__quarter

    @quarter.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def quarter(self, value):
        if value is not None:
            if value in range(1, 5):
                self.__month = value * 3
                self.__quarter = value
            else:
                messagebox.askokcancel(
                    "Critical Error",
                    "Quarter Value Not Allowed: {}. Please restart the application.".format(value),
                )
                raise ValueError

    # endregion ########################################################################################################

    # region Value #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def year(self):
        return self.__year

    @year.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def year(self, value):
        if value is not None:
            if value in range(2016, datetime.datetime.now().year + 1):
                self.__year = value
            else:
                messagebox.askokcancel(
                    "Critical Error",
                    "Year Value Not Allowed: {}. Please restart the application.".format(value),
                )
                raise ValueError

    # endregion ########################################################################################################

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_date(self):
        raise NotImplementedError

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_date(self):
        raise NotImplementedError

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_acct_period(self):
        raise NotImplementedError

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_acct_period(self):
        raise NotImplementedError

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        raise NotImplementedError


# class DayItem(DateItem):
#     logger = CustomAdapter(logging.getLogger(str(__name__)), None)
#
#     # when do my values start? Check MSSQL db for earliest date, today = latest date
#     @debug(lvl=logging.NOTSET, prefix='')
#     def __init__(self, day):
#         super().__init__(day=day)
#         self.date_type = "day"
#
#     @property
#     @debug(lvl=logging.NOTSET, prefix="")
#     def start_date(self):
#         return self.day
#
#     @property
#     @debug(lvl=logging.NOTSET, prefix="")
#     def end_date(self):
#         if self.month == 12:
#             return datetime.datetime(month=self.month % 12 + 1, year=self.year + 1,
#                                      day=1) - datetime.timedelta(days=1)
#         else:
#             return datetime.datetime(month=self.month % 12 + 1, year=self.year, day=1) - datetime.timedelta(
#                 days=1)
#
#     @property
#     @debug(lvl=logging.NOTSET, prefix="")
#     def start_acct_period(self):
#         return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))
#
#     @property
#     @debug(lvl=logging.NOTSET, prefix="")
#     def end_acct_period(self):
#         return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))
#
#     @debug(lvl=logging.NOTSET, prefix="")
#     def __str__(self):
#         return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))
#

class MonthItem(DateItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # when do my values start? Check MSSQL db for earliest date, today = latest date
    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, month, year):
        super().__init__(month=month, year=year)
        self.date_type = "month"

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_date(self):
        return datetime.datetime(month=self.month, year=self.year, day=1)

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_date(self):
        if self.month == 12:
            return datetime.datetime(month=self.month % 12 + 1, year=self.year + 1,
                                     day=1) - datetime.timedelta(days=1)
        else:
            return datetime.datetime(month=self.month % 12 + 1, year=self.year, day=1) - datetime.timedelta(
                days=1)

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_acct_period(self):
        return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_acct_period(self):
        return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))


class MonthSummaryItem(DateItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, start_month, end_month):
        print(type(start_month))
        print(type(end_month))
        self.start_month = start_month
        self.end_month = end_month
        super().__init__(month=self.start_month.month, year=self.start_month.year)
        self.date_type = "month_summary"

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_date(self):
        return self.start_month.start_date

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_date(self):
        return self.end_month.end_date

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_acct_period(self):
        return self.start_month.start_acct_period

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_acct_period(self):
        return self.end_month.end_acct_period

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        # if self.start_month.date_type == "month":
        #     pass
        # if self.start_month.date_type == "month_alone":
        #     pass

        return "{}-{} {}".format(str(self.start_month)[:2], str(self.end_month)[:2], str(self.start_month.year))


class MonthAloneItem(MonthItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # when do my values start? Check MSSQL db for earliest date, today = latest date
    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, month):
        super().__init__(month=month, year=datetime.datetime.now().year)
        self.date_type = "month_alone"

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        return calendar.month_abbr[self.month]


class QuarterItem(DateItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, quarter, year):
        super().__init__(quarter=quarter, year=year)
        self.date_type = "quarter"

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_date(self):
        return datetime.datetime(month=self.month - 2, year=self.year, day=1)

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_date(self):
        return datetime.datetime(month=self.month % 12 + 1, year=self.year, day=1) - datetime.timedelta(days=1)

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_acct_period(self):
        return "{:02d}{:02d}".format(self.month - 2, int(str(self.year)[-2:]))

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_acct_period(self):
        return "{:02d}{:02d}".format(self.month, int(str(self.year)[-2:]))

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        if self.quarter == 1:
            quarter_str = "1st"
        elif self.quarter == 2:
            quarter_str = "2nd"
        elif self.quarter == 3:
            quarter_str = "3rd"
        elif self.quarter == 4:
            quarter_str = "4th"
        else:
            messagebox.askokcancel(
                "Critical Error",
                "Unknown Quarter Value: {}. Please restart the application.".format(self.quarter),
            )
            raise ValueError
        return "{} {}".format(quarter_str, self.year)


class QuarterSummaryItem(DateItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, start_quarter, end_quarter):
        self.start_quarter = start_quarter
        self.end_quarter = end_quarter
        super().__init__(quarter=self.start_quarter.quarter, year=self.start_quarter.year)
        self.date_type = "quarter_summary"

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_date(self):
        return self.start_quarter.start_date

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_date(self):
        return self.end_quarter.end_date

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_acct_period(self):
        return self.start_quarter.start_acct_period

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_acct_period(self):
        return self.end_quarter.end_acct_period

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        return "{}-{} {}".format(str(self.start_quarter)[:3], str(self.end_quarter)[:3], str(self.start_quarter.year))


class QuarterAloneItem(QuarterItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, quarter):
        super().__init__(quarter=quarter, year=datetime.datetime.now().year)
        self.date_type = "quarter_alone"

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        if self.quarter == 1:
            quarter_str = "1st"
        elif self.quarter == 2:
            quarter_str = "2nd"
        elif self.quarter == 3:
            quarter_str = "3rd"
        elif self.quarter == 4:
            quarter_str = "4th"
        else:
            messagebox.askokcancel(
                "Critical Error",
                "Unknown Quarter Value: {}. Please restart the application.".format(self.quarter),
            )
            raise ValueError
        return quarter_str


class YearItem(DateItem):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    # when do my values start? Check MSSQL db for earliest date, today = latest date
    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, year):
        super().__init__(year=year)
        self.date_type = "year"

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_date(self):
        return datetime.datetime(month=1, year=self.year, day=1)

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_date(self):
        return datetime.datetime(month=1, year=self.year + 1, day=1) - datetime.timedelta(days=1)

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def start_acct_period(self):
        return "{:02d}{:02d}".format(1, int(str(self.year)[-2:]))

    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def end_acct_period(self):
        return "{:02d}{:02d}".format(12, int(str(self.year)[-2:]))

    @debug(lvl=logging.NOTSET, prefix="")
    def __str__(self):
        return str(self.year)


class DateItemCombo(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 start_item=None,
                 end_item=None,
                 start_month_item=None,
                 end_month_item=None,
                 start_year_item=None,
                 end_year_item=None):
        self.start_item = start_item
        self.end_item = end_item
        self.start_month_item = start_month_item
        self.end_month_item = end_month_item
        self.start_year_item = start_year_item
        self.end_year_item = end_year_item
        self.item_type = None
        self.month_date_type = None


class MonthOverMonthCombo(DateItemCombo):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, start_item, end_item):
        super().__init__(start_item=start_item, end_item=end_item)
        assert self.start_item.date_type == self.end_item.date_type
        self.item_type = self.start_item.date_type

    @debug(lvl=logging.NOTSET, prefix='')
    def get_date_range_list(self):
        year_dict = {}
        seed_date = self.start_item.start_date
        while seed_date < self.end_item.end_date:
            if self.item_type == "month":
                start_date = MonthItem(month=seed_date.month, year=seed_date.year)
                seed_date = seed_date + relativedelta(months=+1)
                # end_date = MonthItem(month=seed_date.month, year=seed_date.year)
            elif self.item_type == "quarter":
                start_date = QuarterItem(quarter=math.ceil(seed_date.month / 3), year=seed_date.year)
                seed_date = seed_date + relativedelta(months=+3)
                # end_date = QuarterItem(quarter=math.ceil(seed_date.month / 3), year=seed_date.year)
            elif self.item_type == "year":
                start_date = YearItem(year=seed_date.year)
                seed_date = seed_date + relativedelta(years=+1)
                # end_date = YearItem(year=seed_date.year)
            else:
                messagebox.askokcancel(
                    "Critical Error",
                    "Unknown Item Type: {}. Please restart the application.".format(self.item_type),
                )
                raise ValueError

            if year_dict.get(str(start_date.year)) is None:
                year_dict[str(start_date.year)] = [start_date]
            else:
                year_dict[str(start_date.year)].append(start_date)
        return year_dict

    @debug(lvl=logging.DEBUG, prefix='')
    def get_comparison_range_list(
            self,
            include_summary=True,
            compare_summary=True,
            include_individual=True,
            compare_individual=True):
        date_range_dict = self.get_date_range_list()
        return_list = []
        if include_individual:
            for year in sorted(date_range_dict.keys()):
                if compare_individual:
                    return_list.extend(list(zip(date_range_dict[year][:-1], date_range_dict[year][1:])))
                else:
                    return_list.append(date_range_dict[year])
        if include_summary:
            summary_list = []
            for year in sorted(date_range_dict.keys()):
                if self.item_type == "month":
                    date_item = MonthSummaryItem(
                        start_month=date_range_dict[year][0],
                        end_month=date_range_dict[year][-1]
                    )
                elif self.item_type == "quarter":
                    date_item = QuarterSummaryItem(
                        start_quarter=date_range_dict[year][0],
                        end_quarter=date_range_dict[year][-1]
                    )
                else:
                    messagebox.askokcancel(
                        "Critical Error",
                        "Unknown Month Date Type: {}. Please restart the application.".format(self.month_date_type),
                    )
                    raise ValueError
                summary_list.append(date_item)
            for date_item in summary_list:
                self.__class__.logger.log(logging.NOTSET, "Summary: {}".format(date_item))
            if compare_summary:
                return_list.extend(list(zip(summary_list[:-1], summary_list[1:])))
            else:
                return_list.append(summary_list)
        for cnt, date_list in enumerate(return_list, 1):
            str_list = [date_obj.start_date.strftime('%m/%d/%Y') for date_obj in date_list]
            self.__class__.logger.log(logging.DEBUG, "Date Item: {} | From {}".format(
                cnt,
                " to ".join(str_list)))
        # for cnt, [date_1, date_2] in enumerate(return_list, 1):
        #     self.__class__.logger.log(logging.DEBUG, "Date Item: {} from {} to {}".format(
        #         cnt,
        #         date_1.start_date.strftime('%m/%d/%Y'),
        #         date_2.start_date.strftime('%m/%d/%Y')))
        return return_list


class YearOverYearCombo(DateItemCombo):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, start_month_item, end_month_item, start_year_item, end_year_item):
        super().__init__(start_month_item=start_month_item, end_month_item=end_month_item,
                         start_year_item=start_year_item, end_year_item=end_year_item)
        assert self.start_month_item.date_type == self.end_month_item.date_type
        assert self.start_year_item.date_type == self.end_year_item.date_type
        self.month_date_type = self.start_month_item.date_type

    @debug(lvl=logging.DEBUG, prefix='')
    def get_comparison_range_list(
            self,
            include_summary=True,
            compare_summary=True,
            include_individual=True,
            compare_individual=True):
        year_dict = {}
        range_combo_list = []
        month_int = self.start_month_item.start_date.month
        self.__class__.logger.log(logging.NOTSET, "Initial month_int: {0}".format(month_int))
        while month_int <= self.end_month_item.end_date.month:
            year_int = self.start_year_item.start_date.year
            self.__class__.logger.log(logging.NOTSET, "year_int: {0}".format(year_int))
            yearly_comparison_range_list = []
            while year_int <= self.end_year_item.end_date.year:
                if self.month_date_type == "month_alone":
                    date_item = MonthItem(month=month_int, year=year_int)
                elif self.month_date_type == "quarter_alone":
                    date_item = QuarterItem(quarter=math.ceil(month_int / 3), year=year_int)
                else:
                    messagebox.askokcancel(
                        "Critical Error",
                        "Unknown Month Date Type: {}. Please restart the application.".format(self.month_date_type),
                    )
                    raise ValueError

                if year_dict.get(year_int) is None:
                    year_dict[year_int] = []
                year_dict[year_int].append(date_item)
                yearly_comparison_range_list.append(date_item)
                year_int += 1
            self.__class__.logger.log(logging.NOTSET, "year_int: {0}".format(month_int))
            for date_item in yearly_comparison_range_list:
                self.__class__.logger.log(
                    logging.NOTSET,
                    "Yearly Item: {} to {}".format(
                        date_item.start_date,
                        date_item.end_date))
            if include_individual:
                if compare_individual:
                    range_combo_list.extend(list(zip(yearly_comparison_range_list[:-1],
                                                     yearly_comparison_range_list[1:])))
                else:
                    range_combo_list.append(yearly_comparison_range_list)
            if self.month_date_type == "month_alone":
                month_int += 1
            elif self.month_date_type == "quarter_alone":
                month_int += 3

        self.__class__.logger.log(logging.DEBUG, "Year Dictionary:")
        for year, dates in year_dict.items():
            self.__class__.logger.log(logging.DEBUG, "{}: {}".format(year, dates))
        if include_summary:
            summary_list = []
            for item_list in year_dict.values():
                if self.month_date_type == "month_alone":
                    date_item = MonthSummaryItem(start_month=item_list[0], end_month=item_list[-1])
                elif self.month_date_type == "quarter_alone":
                    date_item = QuarterSummaryItem(start_quarter=item_list[0], end_quarter=item_list[-1])
                else:
                    messagebox.askokcancel(
                        "Critical Error",
                        "Unknown Month Date Type: {}. Please restart the application.".format(self.month_date_type),
                    )
                    raise ValueError
                summary_list.append(date_item)
            for date_item in summary_list:
                self.__class__.logger.log(logging.DEBUG, "Summary: {}".format(date_item))
            if compare_summary:
                range_combo_list.extend(list(zip(summary_list[:-1], summary_list[1:])))
            else:
                range_combo_list.append(summary_list)
        for cnt, date_list in enumerate(range_combo_list, 1):
            str_list = [date_obj.start_date.strftime('%m/%d/%Y') for date_obj in date_list]
            self.__class__.logger.log(logging.DEBUG, "Date Item: {} | From {}".format(
                cnt,
                " to ".join(str_list)))
        return range_combo_list


"""
    for each date-span tuple, append comparisons
    Feed the result of this into the index generator

    The variance and pcnt variance columns can just be pandas data manipulations
    Each metric can be it's own dataframe. append dataframes to one-another 

    use a join to knit the dataframes together

    https://stackoverflow.com/questions/46755146/combine-dataframes-with-different-indexes-in-pandas



"""