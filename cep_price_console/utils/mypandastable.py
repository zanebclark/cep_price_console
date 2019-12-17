import tkinter as tk
from tkinter import BooleanVar
from pandastable.headers import createSubMenu, QueryDialog
from pandastable.dialogs import applyStyle, MultipleValDialog, addButton
from pandastable import Table, ColumnHeader, RowHeader, AutoScrollbar, IndexHeader, ToolBar, statusBar, images, util
import logging

class MyQueryDialog(QueryDialog):
    applyqueryvar: BooleanVar

    def setup(self):
        qf = self
        sfont = "Helvetica 10 bold"
        self.queryvar = tk.StringVar()
        self.fbar = tk.Frame(qf)
        self.fbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=2, pady=2)
        f = tk.Frame(qf)
        f.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=2)
        addButton(f, 'find', self.query, images.filtering(), 'apply filters', side=tk.LEFT)
        addButton(f, 'add manual filter', self.addFilter, images.add(),
                  'add manual filter', side=tk.LEFT)
        addButton(f, 'close', self.close, images.cross(), 'close', side=tk.LEFT)
        self.applyqueryvar = tk.BooleanVar()
        self.applyqueryvar.set(True)
        c = tk.Checkbutton(f, text='show filtered only', variable=self.applyqueryvar, command=self.query)
        c.pack(side=tk.LEFT, padx=2)
        addButton(f, 'color rows', self.colorResult, images.color_swatch(), 'color filtered rows', side=tk.LEFT)

        self.queryresultvar = tk.StringVar()
        l = tk.Label(f,textvariable=self.queryresultvar, font=sfont)
        l.pack(side=tk.RIGHT)
        return

class MyRowHeader(RowHeader):
    def popupMenu(self, event, rows=None, cols=None, outside=None):

        """Add left and right click behaviour for canvas, should not have to override
            this function, it will take its values from defined dicts in constructor"""

        defaultactions = {"Select All": self.table.selectAll,
                          "Add Row(s)": lambda: self.table.addRows(),
                          "Delete Row(s)": lambda: self.table.deleteRow(),
                          "Duplicate Row(s)": lambda: self.table.duplicateRows()}
        main = ["Add Row(s)", "Delete Row(s)", "Duplicate Row(s)"]

        popupmenu = tk.Menu(self, tearoff=0)

        def popupFocusOut(event):
            popupmenu.unpost()

        for action in main:
            popupmenu.add_command(label=action, command=defaultactions[action])

        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        applyStyle(popupmenu)
        return popupmenu


class MyColumnHeader(ColumnHeader):
    def popupMenu(self, event):
        """Add left and right click behaviour for column header"""

        df = self.table.model.df
        if len(df.columns) == 0:
            return
        ismulti = util.check_multiindex(df.columns)
        colname = str(df.columns[self.table.currentcol])
        currcol = self.table.currentcol
        multicols = self.table.multiplecollist
        colnames = list(df.columns[multicols])[:4]
        colnames = [str(i)[:20] for i in colnames]
        if len(colnames) > 2:
            colnames = ','.join(colnames[:2]) + '+%s others' % str(len(colnames) - 2)
        else:
            colnames = ','.join(colnames)
        popupmenu = tk.Menu(self, tearoff=0)

        def popupFocusOut(event):
            popupmenu.unpost()

        columncommands = {"Rename": self.renameColumn,
                          "Add": self.table.addColumn,
                          "Delete": self.table.deleteColumn,
                          "Copy": self.table.copyColumn,
                          "Move to Start": self.table.moveColumns,
                          "Move to End": lambda: self.table.moveColumns(pos='end'),
                          "Set Data Type": self.table.setColumnType
                          }
        formatcommands = {'Set Color': self.table.setColumnColors,
                          'Alignment': self.table.setAlignment,
                          'Wrap Header': self.table.setWrap
                          }
        popupmenu.add_command(label="Sort by " + colnames + ' \u2193',
                              command=lambda: self.table.sortTable(ascending=[1 for i in multicols]))
        popupmenu.add_command(label="Sort by " + colnames + ' \u2191',
                              command=lambda: self.table.sortTable(ascending=[0 for i in multicols]))
        popupmenu.add_command(label="Delete Column(s)", command=self.table.deleteColumn)
        createSubMenu(popupmenu, 'Column', columncommands)
        createSubMenu(popupmenu, 'Format', formatcommands)
        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        applyStyle(popupmenu)
        return popupmenu


class MyTable(Table):
    def __init__(self, parent=None, model=None, dataframe=None, width=None, height=None, rows=20, cols=5,
                 showtoolbar=False, showstatusbar=False, allow_edits=True, **kwargs):
        super().__init__(parent, model, dataframe, width, height, rows, cols, showtoolbar, showstatusbar, **kwargs)
        if not allow_edits:
            self.editable = False

    def show(self, callback=None):
        """Adds column header and scrollbars and combines them with
           the current table adding all to the master frame provided in constructor.
           Table is then redrawn."""

        # Add the table and header to the frame
        self.rowheader = MyRowHeader(self.parentframe, self)
        self.tablecolheader = MyColumnHeader(self.parentframe, self)
        self.rowindexheader = IndexHeader(self.parentframe, self)
        self.Yscrollbar = AutoScrollbar(self.parentframe, orient=tk.VERTICAL, command=self.set_yviews)
        self.Yscrollbar.grid(row=1, column=2, rowspan=1, sticky='news', pady=0, ipady=0)
        self.Xscrollbar = AutoScrollbar(self.parentframe, orient=tk.HORIZONTAL, command=self.set_xviews)
        self.Xscrollbar.grid(row=2, column=1, columnspan=1, sticky='news')
        self['xscrollcommand'] = self.Xscrollbar.set
        self['yscrollcommand'] = self.Yscrollbar.set
        self.tablecolheader['xscrollcommand'] = self.Xscrollbar.set
        self.rowheader['yscrollcommand'] = self.Yscrollbar.set
        self.parentframe.rowconfigure(1, weight=1)
        self.parentframe.columnconfigure(1, weight=1)

        self.rowindexheader.grid(row=0, column=0, rowspan=1, sticky='news')
        self.tablecolheader.grid(row=0, column=1, rowspan=1, sticky='news')
        self.rowheader.grid(row=1, column=0, rowspan=1, sticky='news')
        self.grid(row=1, column=1, rowspan=1, sticky='news', pady=0, ipady=0)

        self.adjustColumnWidths()
        # bind redraw to resize, may trigger redraws when widgets added
        self.parentframe.bind("<Configure>", self.resized)  # self.redrawVisible)
        self.tablecolheader.xview("moveto", 0)
        self.xview("moveto", 0)
        if self.showtoolbar:
            self.toolbar = ToolBar(self.parentframe, self)
            self.toolbar.grid(row=0, column=3, rowspan=2, sticky='news')
        if self.showstatusbar:
            self.statusbar = statusBar(self.parentframe, self)
            self.statusbar.grid(row=3, column=0, columnspan=2, sticky='ew')
        # self.redraw(callback=callback)
        self.currwidth = self.parentframe.winfo_width()
        self.currheight = self.parentframe.winfo_height()
        if hasattr(self, 'pf'):
            self.pf.updateData()
        return

    # --- Some cell specific actions here ---

    def popupMenu(self, event, rows=None, cols=None, outside=None):
        """Add left and right click behaviour for canvas, should not have to override
            this function, it will take its values from defined dicts in constructor"""

        defaultactions = {
            "Copy": lambda: self.copy(rows, cols),
            "Undo": lambda: self.undo(),
            "Add Row(s)": lambda: self.addRows(),
            "Add Column(s)": lambda: self.addColumn(),
            "Delete Column(s)": lambda: self.deleteColumn(),
            "Clear Data": lambda: self.deleteCells(rows, cols),
            "Select All": self.selectAll,
            "Set Color": self.setRowColors,
            "Filter Rows": self.queryBar,
            "Preferences": self.showPreferences,
            "Clean Data": self.cleanData,
            "Clear Formatting": self.clearFormatting,
            "Undo Last Change": self.undo,
            "Copy Table": self.copyTable,
            "Find/Replace": self.findText}

        main = ["Copy", "Undo", "Clear Data", "Set Color"]
        general = ["Select All", "Filter Rows", 'Clear Formatting', "Preferences"]

        def add_commands(fieldtype):
            """Add commands to popup menu for column type and specific cell"""
            functions = self.columnactions[fieldtype]
            for f in list(functions.keys()):
                func = getattr(self, functions[f])
                popupmenu.add_command(label=f, command=lambda: func(row, col))
            return

        popupmenu = tk.Menu(self, tearoff=0)

        # noinspection PyUnusedLocal
        def popupFocusOut(event):
            popupmenu.unpost()

        if outside is None:
            # if outside table, just show general items
            row = self.get_row_clicked(event)
            col = self.get_col_clicked(event)
            coltype = self.model.getColumnType(col)

            def add_defaultcommands():
                """now add general actions for all cells"""
                for action in main:
                    popupmenu.add_command(label=action, command=defaultactions[action])
                return

            if coltype in self.columnactions:
                add_commands(coltype)
            add_defaultcommands()

        for action in general:
            popupmenu.add_command(label=action, command=defaultactions[action])

        # popupmenu.add_separator()
        # createSubMenu(popupmenu, 'File', filecommands)
        # createSubMenu(popupmenu, 'Edit', editcommands)
        # createSubMenu(popupmenu, 'Plot', plotcommands)
        # createSubMenu(popupmenu, 'Table', tablecommands)
        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        applyStyle(popupmenu)
        return popupmenu

    def queryBar(self, evt=None):
        """Query/filtering dialog"""

        if hasattr(self, 'qframe') and self.qframe is not None:
            return
        self.qframe = MyQueryDialog(self)
        self.qframe.grid(row=self.queryrow,column=0,columnspan=3,sticky='news')
        return

    def setColumnType(self):
        """Change the column dtype"""

        df = self.model.df
        col = df.columns[self.currentcol]
        # coltypes = {'object': 'Object',
        #             'str': 'Text',
        #             'int': 'Integer',
        #             'float64': 'Decimal',
        #             'category': 'Category',
        #             'datetime64': 'Date Time'}
        coltypes = {'Object': 'object',
                    'Text': 'str',
                    'Integer': 'int',
                    'Decimal': 'float64',
                    'Category': 'category',
                    'Date': 'datetime64',
                    'Time': 'datetime64',
                    'Date Time': 'datetime64'}
        curr = df[col].dtype
        d = MultipleValDialog(title='current type is %s' %curr,
                              initialvalues=[list(coltypes.keys())],
                              labels=['Type:'],
                              types=['combobox'],
                              parent = self.parentframe)
        if d.result is None:
            return
        t = d.results[0]
        try:
            location = df.columns.get_loc(col) + 1
            column_name = "{}_{}".format(col, t)
            if t == "Integer":
                self.model.df.insert(
                    loc=location,
                    column=column_name,
                    value=df[col].astype(coltypes[t])
                )
            self.redraw()
        except:
            logging.error("Exception occurred", exc_info=True)
            print('failed')
        return

    def handle_mouse_drag(self, event):
        print("colover", self.get_col_clicked(event))
        print(self.cols)
        print(self.startcol)
        super().handle_mouse_drag(event)

    # class statusBar(tk.Frame):
    #     """Status bar class"""
    #
    #     def __init__(self, parent=None, parentapp=None):
    #         tk.Frame.__init__(self, parent)
    #         self.parentframe = parent
    #         self.parentapp = parentapp
    #         df = self.parentapp.model.df
    #         sfont = ("Helvetica bold", 10)
    #         clr = '#A10000'
    #         self.rowsvar = tk.StringVar()
    #         self.rowsvar.set(len(df))
    #         l = tk.Label(self, textvariable=self.rowsvar, font=sfont, foreground=clr)
    #         l.pack(fill=tk.X, side=tk.LEFT)
    #         tk.Label(self, text='rows x', font=sfont, foreground=clr).pack(side=tk.LEFT)
    #         self.colsvar = tk.StringVar()
    #         self.colsvar.set(len(df.columns))
    #         l = tk.Label(self, textvariable=self.colsvar, font=sfont, foreground=clr)
    #         l.pack(fill=tk.X, side=tk.LEFT)
    #         tk.Label(self, text='columns', font=sfont, foreground=clr).pack(side=tk.LEFT)
    #         self.filenamevar = tk.StringVar()
    #         l = tk.Label(self, textvariable=self.filenamevar, font=sfont)
    #         l.pack(fill=tk.X, side=tk.RIGHT)
    #         fr = tk.Frame(self)
    #         fr.pack(fill=tk.Y, side=tk.RIGHT)
    #
    #         img = images.contract_col()
    #         addButton(fr, 'Contract Cols', self.parentapp.contractColumns, img, 'contract columns', side=tk.LEFT,
    #                   padding=1)
    #         img = images.expand_col()
    #         addButton(fr, 'Expand Cols', self.parentapp.expandColumns, img, 'expand columns', side=tk.LEFT, padding=1)
    #         img = images.zoom_out()
    #         addButton(fr, 'Zoom Out', self.parentapp.zoomOut, img, 'zoom out', side=tk.LEFT, padding=1)
    #         img = images.zoom_in()
    #         addButton(fr, 'Zoom In', self.parentapp.zoomIn, img, 'zoom in', side=tk.LEFT, padding=1)
    #         return