from cep_price_console.utils.log_utils import debug, CustomAdapter
import cep_price_console.utils.config as config_mod
from cep_price_console.utils.gui_utils import center_window
import logging
from collections import OrderedDict
import tkinter as tk
import tkinter.ttk as ttk


class ConfigGUI(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    inst = None

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, *args, **kwargs):
        self.name = "config_gui"
        super().__init__(*args, **kwargs)
        self.title("Filtering Criteria")
        self.iconbitmap(config_mod.FAVICON)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.header = ttk.Label(self, text="Configuration Parameters", style="heading2.TLabel")
        self.header.grid(row=0, column=0)

        self.reset_btn = ttk.Button(self, text="Reset Defaults", command=self.restore_defaults)
        self.reset_btn.grid(row=0, column=1)

        self.paned_sections = tk.PanedWindow(self,
                                             orient=tk.VERTICAL,
                                             name="paned_factor_criteria",
                                             sashrelief=tk.RAISED,
                                             sashwidth=7)
        self.paned_sections.grid(row=1, column=0, sticky=tk.NSEW, columnspan=2)

        self.section_dict = OrderedDict()
        self.dashboard = None
        self.withdraw()
        self.row_counter = 0

    @debug(lvl=logging.NOTSET, prefix='')
    def restore_defaults(self):
        config_mod.write_default_config()
        self.update_values()

    @debug(lvl=logging.NOTSET, prefix='')
    def update_values(self):
        for section in self.section_dict.values():
            for key in section.key_dict.values():
                key.value_sync(None, None, "read")
        self.update_idletasks()

    @debug(lvl=logging.DEBUG, prefix="")
    def populate(self):
        for section in self.section_dict.values():
            section.add_pane()
            section.frame.update_idletasks()
            self.paned_sections.add(section.frame,
                                    minsize=section.frame.winfo_reqheight(),
                                    pady=5,
                                    padx=5,
                                    stretch="always")
        self.paned_sections.update()
        center_window(self,
                      height=self.paned_sections.winfo_reqheight() + 40,
                      width=self.paned_sections.winfo_reqwidth()
                      )

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        if self.dashboard is not None:
            self.dashboard.menu_bar.delete("--Close--")
        self.withdraw()

    @debug(lvl=logging.DEBUG, prefix='')
    def show(self, dashboard=None):
        self.dashboard = dashboard
        self.deiconify()
        self.update_values()
        return self


class IniSection(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    section_dict = {}

    @debug(lvl=logging.DEBUG, prefix="")
    def __init__(self, section, gui_obj, *args, **kw):
        self.frame = None
        self.lbl = None
        self.section = section
        self.gui_obj = gui_obj
        self.gui_obj.section_dict[str(self)] = self
        self.missing = True
        self.row_counter = 1
        self.key_dict = {}
        self.style_prefix = None
        IniSection.section_dict[str(self)] = self

    @debug(lvl=logging.DEBUG, prefix="")
    def add_pane(self):
        self.frame = ttk.Frame(self.gui_obj.paned_sections)
        self.frame.columnconfigure(1, weight=1)
        self.frame.config(padding=5)

        self.lbl = ttk.Label(self.frame, text=str(self))
        self.lbl.grid(row=0, column=0, columnspan=2)

        if len(self.gui_obj.paned_sections.panes()) % 2 == 0:
            self.style_prefix = "even"
        else:
            self.style_prefix = "odd"
        self.frame.configure(style="{}.group.TFrame".format(self.style_prefix))
        self.lbl.configure(style="{}.heading3.TLabel".format(self.style_prefix))
        self.populate()

    @debug(lvl=logging.DEBUG, prefix="")
    def populate(self):
        for key in self.key_dict.values():
            key.grid(self.row_counter)
            self.row_counter += 1

    @classmethod
    @debug(lvl=logging.DEBUG, prefix="")
    def reset_dict(cls):
        cls.section_dict = {}

    def __str__(self):
        return self.section


class IniDBSection(IniSection):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    section_dict = {}
    creds = []

    @debug(lvl=logging.DEBUG, prefix="")
    def __init__(self, section, gui_obj):
        super().__init__(section, gui_obj)
        self.submit_btn = None
        self.creds = self.__class__.creds

    @debug(lvl=logging.DEBUG, prefix="")
    def add_pane(self):
        super().add_pane()
        self.submit_btn = ttk.Button(self.frame, text="Test Credentials", command=self.test_creds)
        self.submit_btn.grid(row=self.row_counter, column=0, pady=5)
        self.row_counter += 1

    @debug(lvl=logging.DEBUG, prefix="")
    def test_creds(self):
        raise NotImplementedError

    @debug(lvl=logging.DEBUG, prefix="")
    def toggle_creds(self, good_creds):
        for credential in self.creds:
            self.key_dict.get(credential).bad = not good_creds


class MySQLSection(IniDBSection):
    creds = ["mysql_username", "mysql_password", "mysql_user_database"]

    @debug(lvl=logging.DEBUG, prefix="")
    def test_creds(self):
        from cep_price_console.db_management.server_utils import mysql_test_creds
        if mysql_test_creds():
            self.toggle_creds(good_creds=True)
            self.gui_obj.withdraw()
        else:
            self.toggle_creds(good_creds=False)


class MSSQLSection(IniDBSection):
    creds = ["mssql_username", "mssql_password"]

    @debug(lvl=logging.DEBUG, prefix="")
    def test_creds(self):
        from cep_price_console.db_management.server_utils import mssql_test_creds
        if mssql_test_creds():
            self.toggle_creds(good_creds=True)
            self.gui_obj.withdraw()
        else:
            self.toggle_creds(good_creds=False)


class IniKey(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    key_dict = {}

    def __init__(self,
                 section,
                 key,
                 default,
                 read_only=False):
        # print("key")
        self.__bad = False
        self.key = key
        self.section = section
        self.section.key_dict[str(self)] = self
        self.default = default
        self.__read_only = read_only
        self.value = None
        self.missing = True
        self.lbl = None
        self.entry = None
        IniKey.key_dict[self.key] = self

    @debug(lvl=logging.DEBUG, prefix="")
    def grid(self, row):
        self.value = tk.StringVar(name="{}_value".format(str(self)))
        self.value.trace_add('read', self.value_sync)
        self.value.trace_add('write', self.value_sync)
        self.value.trace_add('unset', self.value_sync)
        self.value_sync(None, None, "read")

        self.lbl = ttk.Label(self.section.frame, text=self.key,
                             style="{}.dflt.TLabel".format(self.section.style_prefix))
        self.lbl.grid(row=row, column=0, sticky=tk.E)
        self.entry = ttk.Entry(self.section.frame,
                               style="TEntry",
                               textvariable=self.value)
        self.entry.grid(row=row, column=1, sticky=tk.EW)
        self.read_only = self.__read_only
        self.bad = False

    # region Value #####################################################################################################
    @property
    @debug(lvl=logging.DEBUG, prefix="")
    def bad(self):
        return self.__bad

    @bad.setter
    @debug(lvl=logging.DEBUG, prefix="")
    def bad(self, value):
        if value:
            self.entry.config(font=('Verdana', 10, 'normal'), style="bad.TEntry")
            if self.value.get() == "":
                self.value.set("Provide a value")
        else:
            self.entry.config(font=('Verdana', 10, 'normal'), style="TEntry")
        self.__bad = value
    # endregion ########################################################################################################

    # region Value #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix="")
    def read_only(self):
        return self.__read_only

    @read_only.setter
    @debug(lvl=logging.DEBUG, prefix="")
    def read_only(self, value):
        if value:
            self.entry.state(['disabled'])
        else:
            self.entry.state(['!disabled'])
        self.__read_only = value
    # endregion ########################################################################################################

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix="")
    def value_sync(self, var_name, _, mode):
        if config_mod.config is not None:
            if mode == "write":
                config_mod.config[str(self.section)][str(self.key)] = self.value.get()
                config_mod.write_config()
            elif mode == "read":
                self.value.set(config_mod.config[str(self.section)][str(self)])
            elif mode == "unset":
                raise ValueError
            else:
                raise ValueError

    @classmethod
    @debug(lvl=logging.DEBUG, prefix="")
    def reset_dict(cls):
        cls.key_dict = {}

    def __str__(self):
        return self.key
