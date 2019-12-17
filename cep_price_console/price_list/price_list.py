from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
from cep_price_console.utils.gui_utils import center_window, VerticalScrolledFrame
import tkinter as tk
import tkinter.ttk as ttk
import logging
from tkinter import messagebox
from tkcalendar import DateEntry


class PriceList(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    count = 0

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        # DateSelection.reset()
        PriceList.count += 1
        self.master = master
        self.root = self.master.root
        self.name = str(PriceList.__name__).lower() + str(PriceList.count)
        super().__init__(self.root, name=self.name, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("Price List Generator")
        self.iconbitmap(config.FAVICON)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.date_options_label_frame = ttk.LabelFrame(self,
                                                       borderwidth=2,
                                                       labelanchor=tk.NW,
                                                       padding=2,
                                                       relief=tk.SUNKEN,
                                                       text="Date Options")
        self.date_options_label_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.date_options_label_frame.rowconfigure(1, weight=1)
        self.date_options_label_frame.columnconfigure(0, weight=1)
        self.date_options_label_frame.columnconfigure(1, weight=1)

        self.date_style_var = tk.IntVar()
        self.date_style_radio_1 = ttk.Radiobutton(self.date_options_label_frame,
                                                  text="Calendar Date",
                                                  variable=self.date_style_var,
                                                  value=0,
                                                  command=self.calendar_date_switch)
        self.date_style_radio_1.grid(row=0, column=0)

        self.date_style_radio_2 = ttk.Radiobutton(self.date_options_label_frame,
                                                  text="Accounting Period",
                                                  variable=self.date_style_var,
                                                  value=1,
                                                  command=self.accounting_period_switch)
        self.date_style_radio_2.grid(row=0, column=1)

        self.calendar_date_frame = DateFrame(self.date_options_label_frame,
                                             style="even.group.TFrame",
                                             padding=5)
        self.calendar_date_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        self.acct_period = AcctFrame(self.date_options_label_frame,
                                     style="even.group.TFrame",
                                     padding=5)
        self.acct_period.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.acct_period.grid_remove()

        self.bind('<Configure>', self.top_level_config)

        self.report_options_label_frame = ttk.LabelFrame(self,
                                                         borderwidth=2,
                                                         labelanchor=tk.NW,
                                                         padding=2,
                                                         relief=tk.SUNKEN,
                                                         text="Date Options")
        self.report_options_label_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.report_options_label_frame.rowconfigure(0, weight=1)
        self.report_options_label_frame.columnconfigure(0, weight=1)

        self.sales_history_date_cutoff = None
        self.sales_history_date_checkbutton = None
        self.cust_selection_btn = None
        self.prod_selection_btn = None
        self.max_levels_chk_btn = None
        self.qty_break_chk_btn = None
        self.expired_chk_btn = None
        self.current_chk_btn = None
        self.future_chk_btn = None

        center_window(win_obj=self)

    @debug(lvl=logging.DEBUG, prefix='')
    def calendar_date_switch(self):
        self.switch_date_style("calendar")

    @debug(lvl=logging.DEBUG, prefix='')
    def accounting_period_switch(self):
        self.switch_date_style("accounting")

    @debug(lvl=logging.DEBUG, prefix='')
    def switch_date_style(self, style):
        if style == 'calendar':
            self.calendar_date_frame.grid()
            self.acct_period.grid_remove()
        elif style == 'accounting':
            self.calendar_date_frame.ungrid()
            self.acct_period.grid()
        else:
            raise ValueError

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        msgbox = messagebox.askokcancel("Quit", "Do you want to quit?", parent=self)
        if msgbox:
            self.destroy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def top_level_config(self, *args):
        if self.acct_period is not None:
            # noinspection PyProtectedMember
            self.acct_period.scroll_frame._configure_window(None)


class DateSelection(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    # date_selection_dict = {}

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, parent, row, column, label_text, style=None, *args, **kwargs):
        self.parent = parent
        self.label_text = label_text
        self.row = row
        self.column = column
        self.style = style
        self.label = ttk.Label(self.parent,
                               text=self.label_text,
                               style=self.style)
        self.label.grid(row=self.row, column=self.column, sticky=tk.NW)
        self.value = None
        self.entry = DateEntry(self.parent,
                               firstweekday="sunday",
                               showweeknumbers=False)  # TODO: Apply some style to this date dropdown
        self.entry.grid(row=self.row, column=self.column + 1, sticky=tk.NE)
        self.entry.bind("<<DateEntrySelected>>", self.new_date)
        # DateSelection.date_selection_dict[label_text] = self

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def new_date(self, *args):
        DateSelection.logger.log(logging.DEBUG, "{} Selection: {}".format(self.label_text, self.entry.get_date()))
        self.value = self.entry.get_date()

    # @debug(lvl=logging.DEBUG, prefix='')
    # def ungrid(self):
    #     self.value = None
    #     self.label.grid_remove()
    #     self.entry.grid_remove()
    #     self.entry.set_date(None)

    # @debug(lvl=logging.DEBUG, prefix='')
    # def regrid(self):
    #     self.label.grid()
    #     self.entry.grid()

    # @classmethod
    # @debug(lvl=logging.DEBUG, prefix='')
    # def reset(cls):
    #     cls.date_selection_dict = {}


class DateFrame(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        # noinspection PyArgumentList
        super().__init__(self.parent, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.date_start = DateSelection(self,
                                        style="even.dflt.TLabel",
                                        row=1,
                                        column=0,
                                        label_text="Start Date: ")

        self.date_end = DateSelection(self,
                                      style="even.dflt.TLabel",
                                      row=2,
                                      column=0,
                                      label_text="End Date: ")

    # @debug(lvl=logging.DEBUG, prefix='')
    # def regrid(self):
    #     for date_selection in DateSelection.date_selection_dict.values():
    #         date_selection.regrid()
    #
    @debug(lvl=logging.DEBUG, prefix='')
    def ungrid(self):
        self.date_start.value = None
        self.date_start.entry.set_date(None)
        self.date_end.value = None
        self.date_end.entry.set_date(None)
        self.grid_remove()
        # for date_selection in DateSelection.date_selection_dict.values():
        #     date_selection.ungrid()


class AcctFrame(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        # noinspection PyArgumentList
        super().__init__(self.parent, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.parent_scroll_frame = ttk.Frame(self,
                                             style="odd.group.TFrame",
                                             padding=5)
        self.parent_scroll_frame.rowconfigure(0, weight=1)
        self.parent_scroll_frame.columnconfigure(0, weight=1)
        self.parent_scroll_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.scroll_frame = VerticalScrolledFrame(self.parent_scroll_frame)

        self.paned_window = tk.PanedWindow(self.scroll_frame,
                                           orient=tk.VERTICAL,
                                           name="acct_period")
        self.paned_window.rowconfigure(0, weight=1)
        self.paned_window.columnconfigure(0, weight=1)
        self.paned_window.grid(row=0, column=0, sticky=tk.NSEW)

        self.add_option_btn = ttk.Button(self,
                                         text="Add Period",
                                         command=self.add_option)
        self.add_option_btn.grid(row=1, column=0)
        self.acct_period_selection = []

    @debug(lvl=logging.DEBUG, prefix='')
    def add_option(self):
        something = AcctPeriod(acct_frame=self, acct_paned_window=self.paned_window)
        self.acct_period_selection.append(something)
        self.paned_window.add(something,
                              sticky=tk.NSEW,
                              stretch="never")
        self.scroll_frame.event_generate("<Configure>")

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_selection(self,
                           action,
                           index,
                           value_if_allowed,
                           prior_value,
                           text,
                           validation_type,
                           trigger_type,
                           widget_name):
        # if value_if_allowed != "":
        return True


class AcctPeriod(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, acct_frame, acct_paned_window, *args, **kwargs):
        self.acct_frame = acct_frame
        self.acct_paned_window = acct_paned_window
        # noinspection PyArgumentList
        super().__init__(acct_paned_window, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        entry_validation = (self.register(self.validate_selection),
                            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self,
                               textvariable=self.entry_var,
                               validate='focusout',
                               validatecommand=entry_validation)
        self.entry.grid(row=0, column=0, sticky=tk.NW + tk.E)

        self.close_btn = ttk.Button(self,
                                    text="x",
                                    command=self.remove,
                                    width=1)
        self.close_btn.grid(row=0, column=1, sticky=tk.NE)

    @debug(lvl=logging.DEBUG, prefix='')
    def remove(self):
        self.acct_frame.remove_sel(self)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def validate_selection(self,
                           action,
                           index,
                           value_if_allowed,
                           prior_value,
                           text,
                           validation_type,
                           trigger_type,
                           widget_name):
        # if value_if_allowed != "":
        return True

