import tkinter as tk
import tkinter.ttk as ttk
import datetime
from ttkwidgets import CheckboxTreeview
from cep_price_console.utils.log_utils import CustomAdapter, debug
import logging
from cep_price_console.cntr_upload.CntrUploadTab import BusyManager


class TreeviewConstructor(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, master, frame_main, checkwidth=0):
        self.master = master  # Done
        self.frame = frame_main  # Done
        self.col_obj_dict = {}  # Done
        self.column_lst = []  # Done
        self.col_disp_lst = []  # Done
        self.item_obj_dict = {}
        self.treeview = CheckboxTreeview(self.frame)  # Done
        self.ysb = ttk.Scrollbar(self.frame)  # Done
        self.xsb = ttk.Scrollbar(self.frame)  # Done
        self.checkwidth = checkwidth
        self.manager = BusyManager(self.frame)
        self.populate_frame()  # Done

    @debug(lvl=logging.NOTSET, prefix='')
    def populate_frame(self):
        self.frame.columnconfigure(0, weight=1)  # Done
        self.frame.rowconfigure(0, weight=1)  # Done
        self.treeview.grid(row=0, column=0, sticky=tk.NSEW)  # Done
        self.ysb.config(orient=tk.VERTICAL, command=self.treeview.yview)  # Done
        self.xsb.config(orient=tk.HORIZONTAL, command=self.treeview.xview)  # Done
        self.treeview['yscroll'] = self.ysb.set  # Done
        self.treeview['xscroll'] = self.xsb.set  # Done
        self.ysb.grid(row=0, column=1, sticky=tk.NS)  # Done
        self.xsb.grid(row=1, column=0, sticky=tk.EW)  # Done

    @debug(lvl=logging.NOTSET, prefix='')
    def populate_cols(self):
        col_obj = TreeColumn(order=0,
                             col_id='#0',
                             hdr_txt="",
                             anchor=tk.W,
                             stretch=tk.NO,
                             minwidth=0,
                             width=self.checkwidth,
                             display=False)
        TreeviewConstructor.logger.log(logging.NOTSET, "Column ID: {col_id} Header Text: {hdr_txt}".
                                       format(col_id=col_obj.col_id, hdr_txt=col_obj.hdr_txt))
        self.col_obj_dict[col_obj.col_id] = col_obj

        for col_key, column in sorted(self.col_obj_dict.items(), key=lambda x: x[1].order):
            self.column_lst.append(column.col_id)
            if column.display:
                self.col_disp_lst.append(column.col_id)

        self.treeview.config(columns=self.column_lst, displaycolumns=self.col_disp_lst)
        self.treeview.tag_configure('red', foreground='red2')
        self.treeview.tag_configure('evenrow', background='gray85')
        self.treeview.tag_configure('oddrow', background='white')

        for col in self.col_obj_dict.values():
            TreeviewConstructor.logger.log(
                logging.NOTSET,
                "Column ID: {col_id} Header Text: {hdr_txt} Anchor: {anchor}".format(
                    col_id=col.col_id, hdr_txt=col.hdr_txt, anchor=col.anchor))
            if col.hdr_txt in (None, ""):
                header = col.col_id
            else:
                header = col.hdr_txt
            self.treeview.heading(column=col.col_id,
                                  text=header,
                                  anchor=col.anchor,
                                  command=lambda _col=col.col_id: self.treeview_sort_column(_col, False))
            self.treeview.column(col.col_id, minwidth=col.minwidth, width=col.width, stretch=col.stretch)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_items(self):
        for item in self.item_obj_dict.values():
            TreeRow.logger.log(logging.NOTSET, "Item Info: {0}".format(item.iid))
            self.treeview.insert(item.parent, item.index, iid=item.iid, values=item.values_list)
            for tag in item.tags_list:
                self.treeview.tag_add(item.iid, tag)

    @debug(lvl=logging.DEBUG, prefix='')
    def stripe_rows(self):
        for item in self.item_obj_dict.values():
            self.treeview.tag_del(item.iid, 'evenrow')
            self.treeview.tag_del(item.iid, 'oddrow')
            row_num = self.treeview.index(item.iid)
            if row_num % 2 == 0:
                self.treeview.tag_add(item.iid, 'evenrow')
            elif row_num % 2 != 0:
                self.treeview.tag_add(item.iid, 'oddrow')

    @debug(lvl=logging.DEBUG, prefix='')
    def treeview_sort_column(self, col, reverse):
        self.manager.busy()
        item_list = [(self.treeview.set(k, col), k) for k in self.treeview.get_children('')]
        item_list.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(item_list):
            self.treeview.move(k, '', index)
        self.stripe_rows()
        # reverse sort next time
        self.treeview.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))
        self.manager.not_busy()

    @debug(lvl=logging.DEBUG, prefix='')
    def tv_refresh(self):
        # self.manager.busy()
        item_list = list(self.treeview.get_children(''))
        item_list.sort(key=lambda x: int(x))
        for item_iid, item_obj in sorted(self.item_obj_dict.items()):
            TreeRow.logger.log(logging.NOTSET, "Item ID: {0}".format(item_iid))
            # l = self.treeview.get_children('')
            for index, k in enumerate(item_list):
                TreeRow.logger.log(logging.NOTSET, "k: {0}".format(k))
                if str(item_iid) == str(k):
                    self.treeview.delete(k)
                    item_obj.index = index
                    self.treeview.insert(item_obj.parent, item_obj.index, iid=item_obj.iid, values=item_obj.values_list)
                    item_list.remove(k)
                    break
        self.stripe_rows()
        # self.manager.not_busy()


class TreeColumn(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 order=None,  # Done
                 col_id=None,  # Done
                 hdr_txt="",  # Done
                 anchor=tk.W,
                 stretch=tk.YES,
                 minwidth=0,
                 width=50,
                 display=True):
        self.order = order
        self.col_id = col_id
        self.hdr_txt = hdr_txt
        self.__format = None
        self.anchor = anchor
        self.stretch = stretch
        self.minwidth = minwidth
        self.width = width
        self.display = display


class TreeRow(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 treeview_const,
                 iid,
                 parent="",
                 index=tk.END):
        self.treeview_const = treeview_const
        self.parent = parent
        self.index = index
        self.iid = iid
        self.tags_list = []
        self.values_dict = {}
        self.__values_list = []
        self.tv_cells = {}
        self.xl_cells = {}

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def values_list(self):
        temp_list = []
        temp_dict = {}
        if bool(self.xl_cells):
            temp_col_keys = []
            for col_id, column in sorted(self.treeview_const.col_obj_dict.items(), key=lambda x: x[1].order):
                temp_col_keys.append(col_id)
            TreeRow.logger.log(logging.NOTSET, "Temp Col Keys: {0}".format(temp_col_keys))
            temp_xl_keys = list(self.xl_cells.keys())
            temp_xl_keys.sort(key=lambda x: int(x))
            TreeRow.logger.log(logging.NOTSET, "Temp XL Keys: {0}".format(temp_xl_keys))
            # for col_id, col_obj in sorted(temp_col_dict.items(), key=lambda x: x[1].order):
            for col_id in reversed(temp_col_keys):
                match = False
                TreeRow.logger.log(logging.NOTSET, "Col ID: {0}, Order: {1}"
                                   .format(col_id, str(self.treeview_const.col_obj_dict[col_id].order)))
                for col_order in reversed(temp_xl_keys):
                    TreeRow.logger.log(logging.NOTSET, "Col Order: {0}".format(str(col_order)))
                    if str(self.treeview_const.col_obj_dict[col_id].order) == str(col_order):
                        match = True
                        cell_obj = self.xl_cells[col_order]
                        if cell_obj.formatted_value is not None:
                            if cell_obj.fmt_selection == 'date':
                                if isinstance(cell_obj.formatted_value, datetime.datetime):
                                    value = cell_obj.formatted_value.strftime('%m/%d/%Y')
                                elif isinstance(cell_obj.formatted_value, datetime.date):
                                    value = cell_obj.formatted_value.strftime('%m/%d/%Y')
                                else:
                                    value = cell_obj.formatted_value
                            else:
                                value = cell_obj.formatted_value
                        else:
                            value = ""
                        temp_dict[str(self.treeview_const.col_obj_dict[col_id].order)] = value
                        TreeRow.logger.log(logging.NOTSET, "Column ID Match! Col_Order: {0}, Formatted Value: {1}"
                                           .format(str(col_order), cell_obj.formatted_value))
                        TreeRow.logger.log(logging.NOTSET, "Removing values from list: {0}, {1}"
                                           .format(col_id, col_order))
                        temp_col_keys.remove(col_id)
                        temp_xl_keys.remove(col_order)
                        break
                if not match:
                    TreeRow.logger.log(logging.NOTSET, "No Match. Appending empty value")
                    temp_dict[str(self.treeview_const.col_obj_dict[col_id].order)] = ""
            for order in sorted(temp_dict.keys(), key=lambda x: int(x)):
                value = temp_dict[order]
                TreeRow.logger.log(logging.NOTSET, "temp dict key and value: {0}, {1}".format(order, value))
                temp_list.append(value)
            return temp_list
        else:
            TreeRow.logger.log(logging.NOTSET, "Value List based on Value Dict")
            col_orders = []

            for col_obj in self.treeview_const.col_obj_dict.values():
                col_orders.append(col_obj.order)
            col_orders.sort(key=lambda x: int(x))
            TreeRow.logger.log(logging.NOTSET, "Column orders list: {0}".format(col_orders))
            for order in col_orders:
                value = self.values_dict.get(str(order), "")
                formatted_value = "~empty~"
                if not isinstance(value, (datetime.date, datetime.datetime)):
                    formatted_value = value
                else:
                    if isinstance(value, datetime.date):
                        formatted_value = value.strftime('%m/%d/%Y')
                    elif isinstance(value, datetime.datetime):
                        formatted_value = value.strftime('%m/%d/%Y')

                temp_list.append(formatted_value)
                TreeRow.logger.log(logging.NOTSET, "Column order: {0}, Value to append: {1}"
                                   .format(order, self.values_dict.get(str(order), "")))
            return temp_list


# class TreeCell(object):
#     logger = CustomAdapter(logging.getLogger(str(__name__)), None)
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def __init__(self,
#                  ws_obj=None,
#                  row_obj=None,
#                  col_obj=None):
#         self.ws_obj = ws_obj
#         self.row_obj = row_obj
#         self.col_obj = col_obj
#         self.__raw_val = None
#         self.formatting = None
#         self.__formatted_value = None
#         self.init_cell()
#
#     @property
#     @debug(lvl=logging.NOTSET, prefix='')
#     def formatted_value(self):
#         return self.formatting
#
#     @property
#     @debug(lvl=logging.NOTSET, prefix='')
#     def raw_val(self):
#         return self.ws_obj.fetch_value(self.row_obj.iid, self.col_obj.ws_order)[2]
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def format_suggestion(self):
#         self.formatting = self.ws_obj.fetch_value(self.row_obj.iid, self.col_obj.ws_order)[1]
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def init_cell(self):
#         self.row_obj.row_cells[self.col_obj.order] = self
