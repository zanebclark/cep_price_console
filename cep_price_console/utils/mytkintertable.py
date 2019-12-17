from cep_price_console.utils.log_utils import debug
import logging
from tkinter import Menu
from tkintertable.Tables import TableCanvas, ColumnHeader


class MyCanvas(TableCanvas):
    def show(self, callback=None):
        super().show(callback=None)
        self.tablecolheader = MyColumnHeader(self.parentframe, self)
        self.tablecolheader['xscrollcommand'] = self.Xscrollbar.set
        self.tablecolheader.grid(row=0, column=1, rowspan=1, sticky='news', pady=0, ipady=0)
        self.tablecolheader.xview("moveto", 0)

    def do_bindings(self):
        """Bind keys and mouse clicks, this can be overridden"""
        self.bind("<Button-1>", self.handle_left_click)
        self.bind("<Double-Button-1>", self.handle_double_click)
        self.bind("<Control-Button-1>", self.handle_left_ctrl_click)
        self.bind("<Shift-Button-1>", self.handle_left_shift_click)

        self.bind("<ButtonRelease-1>", self.handle_left_release)
        if self.ostyp == 'mac':
            # For mac we bind Shift, left-click to right click
            self.bind("<Button-2>", self.handle_right_click)
            self.bind('<Shift-Button-1>', self.handle_right_click)
        else:
            self.bind("<Button-3>", self.handle_right_click)

        self.bind('<B1-Motion>', self.handle_mouse_drag)
        self.bind('<Motion>', self.handle_motion)

        self.bind_all("<Control-x>", self.deleteRow)
        self.bind_all("<Control-n>", self.addRow)
        self.bind_all("<Delete>", self.clearData)
        self.bind_all("<Control-v>", self.paste)

        # if not hasattr(self,'parentapp'):
        #    self.parentapp = self.parentframe

        self.parentframe.master.bind_all("<Right>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<Left>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<Up>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<Down>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<KP_8>", self.handle_arrow_keys)
        # self.parentframe.master.bind_all("<Return>", self.handle_arrow_keys)
        self.parentframe.master.bind_all("<Tab>", self.handle_arrow_keys)
        # if 'windows' in self.platform:
        self.bind("<MouseWheel>", self.mouse_wheel)
        self.bind('<Button-4>', self.mouse_wheel)
        self.bind('<Button-5>', self.mouse_wheel)
        self.focus_set()
        return

    def popupMenu(self, event, rows=None, cols=None, outside=None):
        """Add left and right click behaviour for canvas, should not have to override
            this function, it will take its values from defined dicts in constructor"""

        defaultactions = {"Set Fill Color": lambda: self.setcellColor(rows, cols, key='bg'),
                          "Set Text Color": lambda: self.setcellColor(rows, cols, key='fg'),
                          "Copy": lambda: self.copyCell(rows, cols),
                          "Paste": lambda: self.pasteCell(rows, cols),
                          "Fill Down": lambda: self.fillDown(rows, cols),
                          "Fill Right": lambda: self.fillAcross(cols, rows),
                          "Add Row(s)": lambda: self.addRows(),
                          "Delete Row(s)": lambda: self.deleteRow(),
                          "View Record": lambda: self.getRecordInfo(row),
                          "Clear Data": lambda: self.deleteCells(rows, cols),
                          "Select": lambda: self.handle_double_click(event),
                          "Select All": self.select_All,
                          "Auto Fit Columns": self.autoResizeColumns,
                          "Filter Records": self.showFilteringBar,
                          "New": self.new,
                          "Load": self.load,
                          "Save": self.save,
                          "Import text": self.importTable,
                          "Export csv": self.exportTable,
                          "Plot Selected": self.plotSelected,
                          "Plot Options": self.plotSetup,
                          "Export Table": self.exportTable,
                          "Preferences": self.showtablePrefs,
                          "Formulae->Value": lambda: self.convertFormulae(rows, cols)}

        main = ["Select", "Set Fill Color", "Set Text Color"]
        general = ["Filter Records"]

        popupmenu = Menu(self, tearoff=0)

        # noinspection PyUnusedLocal,PyShadowingNames
        def popupFocusOut(event):
            popupmenu.unpost()

        if outside is None:
            # if outside table, just show general items
            row = self.get_row_clicked(event)
            col = self.get_col_clicked(event)
            coltype = self.model.getColumnType(col)

            # noinspection PyShadowingNames
            def add_defaultcommands():
                """now add general actions for all cells"""
                for action in main:
                    if action == 'Fill Down' and (rows is None or len(rows) <= 1):
                        continue
                    if action == 'Fill Right' and (cols is None or len(cols) <= 1):
                        continue
                    else:
                        popupmenu.add_command(label=action, command=defaultactions[action])
                return

            add_defaultcommands()

        for action in general:
            popupmenu.add_command(label=action, command=defaultactions[action])

        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu

    def drawCellEntry(self, row, col, text=None):
        pass

    def drawTooltip(self, row, col):
        pass

    @debug(lvl=logging.DEBUG, prefix="")
    def handle_double_click(self, event):
        row = self.get_row_clicked(event)
        self.master.master.selection = self.model.getRecName(row)


class MyColumnHeader(ColumnHeader):
    def popupMenu(self, event):
        colname = self.model.columnNames[self.table.currentcol]
        collabel = self.model.columnlabels[colname]
        currcol = self.table.currentcol
        popupmenu = Menu(self, tearoff=0)

        # noinspection PyUnusedLocal,PyShadowingNames
        def popupFocusOut(event):
            popupmenu.unpost()
        popupmenu.add_command(label="Sort by " + collabel, command=lambda: self.table.sortTable(currcol))
        popupmenu.add_command(label="Sort by " + collabel + ' (descending)',
                              command=lambda: self.table.sortTable(currcol, reverse=1))

        popupmenu.bind("<FocusOut>", popupFocusOut)
        # self.bind("<Button-3>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu
