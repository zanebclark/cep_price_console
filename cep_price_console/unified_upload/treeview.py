import tkinter as tk
import tkinter.ttk as ttk
import datetime
from ttkwidgets import CheckboxTreeview
from cep_price_console.utils.log_utils import CustomAdapter, debug
import logging
# from cep_price_console.cntr_upload.CntrUploadTab import BusyManager


class TreeviewConstructor(ttk.Frame):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        self.col_obj_dict = {}
        self.column_lst = []
        self.col_disp_lst = []
        self.item_obj_dict = {}
        self.master = master

        # noinspection PyArgumentList
        super().__init__(self.master, *args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.treeview = CheckboxTreeview(self)
        TreeviewConstructor.logger.log(logging.DEBUG, "10")
        self.treeview.grid(row=0, column=0, sticky=tk.NSEW)
        TreeviewConstructor.logger.log(logging.DEBUG, "11")

        self.ysb = ttk.Scrollbar(self)
        TreeviewConstructor.logger.log(logging.DEBUG, "12")
        self.ysb.grid(row=0, column=1, sticky=tk.NS)
        TreeviewConstructor.logger.log(logging.DEBUG, "13")
        self.ysb.config(orient=tk.VERTICAL, command=self.treeview.yview)
        TreeviewConstructor.logger.log(logging.DEBUG, "14")

        self.xsb = ttk.Scrollbar(self)
        TreeviewConstructor.logger.log(logging.DEBUG, "15")
        self.xsb.grid(row=1, column=0, sticky=tk.EW)
        TreeviewConstructor.logger.log(logging.DEBUG, "16")
        self.xsb.config(orient=tk.HORIZONTAL, command=self.treeview.xview)
        TreeviewConstructor.logger.log(logging.DEBUG, "17")

        self.treeview['yscroll'] = self.ysb.set
        TreeviewConstructor.logger.log(logging.DEBUG, "18")
        self.treeview['xscroll'] = self.xsb.set
        TreeviewConstructor.logger.log(logging.DEBUG, "19")
        # self.manager = BusyManager(self.frame)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_cols(self, checkwidth):
        col_obj = TreeColumn(order=0,
                             col_id='#0',
                             hdr_txt="",
                             anchor=tk.W,
                             stretch=tk.NO,
                             minwidth=0,
                             width=checkwidth,
                             display=False)
        TreeviewConstructor.logger.log(logging.DEBUG, "Column ID: {col_id} Header Text: {hdr_txt}".
                                       format(col_id=col_obj.col_id, hdr_txt=col_obj.hdr_txt))
        self.col_obj_dict[col_obj.col_id] = col_obj

        for col_key, column in sorted(self.col_obj_dict.items(), key=lambda x: x[1].order):
            self.column_lst.append(column.col_id)
            if column.display:
                self.col_disp_lst.append(column.col_id)

        self.treeview.config(columns=self.column_lst, displaycolumns=self.col_disp_lst)
        self.treeview.tag_configure('red', foreground='red4', background='IndianRed1')
        self.treeview.tag_configure('parent_evenrow', background='gray85')
        self.treeview.tag_configure('child_evenrow', background="honeydew3")
        self.treeview.tag_configure('parent_oddrow', background='white')
        self.treeview.tag_configure('child_oddrow', background="honeydew2")

        for col in self.col_obj_dict.values():
            TreeviewConstructor.logger.log(
                logging.DEBUG,
                "Column ID: {col_id} Header Text: {hdr_txt} Anchor: {anchor}".format(
                    col_id=col.col_id, hdr_txt=col.hdr_txt, anchor=col.anchor))
            if col.hdr_txt in (None, ""):
                header = col.col_id
            else:
                header = col.hdr_txt
            if col.col_id == '#0':
                self.treeview.heading(column=col.col_id,
                                      text="",
                                      anchor=col.anchor,
                                      command=lambda _col=col.col_id: self.treeview_sort_column(_col, False))
            else:
                self.treeview.heading(column=col.col_id,
                                      text=header,
                                      anchor=col.anchor,
                                      command=lambda _col=col.col_id: self.treeview_sort_column(_col, False))

            self.treeview.column(col.col_id, minwidth=col.minwidth, width=col.width, stretch=col.stretch)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_items(self):
        for item in self.item_obj_dict.values():
            TreeviewConstructor.logger.log(logging.NOTSET, "Item Info: {0}".format(item.iid))
            self.treeview.insert(item.parent, item.index, iid=item.iid, values=item.values_list)
            for tag in item.tags_list:
                self.treeview.tag_add(item.iid, tag)

    @debug(lvl=logging.DEBUG, prefix='')
    def stripe_rows(self):
        for item in self.item_obj_dict.values():
            self.treeview.tag_del(item.iid, 'parent_evenrow')
            self.treeview.tag_del(item.iid, 'child_evenrow')
            self.treeview.tag_del(item.iid, 'parent_oddrow')
            self.treeview.tag_del(item.iid, 'child_oddrow')
            row_num = self.treeview.index(item.iid)
            if row_num % 2 == 0:
                if item.parent == "":
                    self.treeview.tag_add(item.iid, 'child_evenrow')
                else:
                    self.treeview.tag_add(item.iid, 'parent_evenrow')
            elif row_num % 2 != 0:
                if item.parent == "":
                    self.treeview.tag_add(item.iid, 'child_oddrow')
                else:
                    self.treeview.tag_add(item.iid, 'parent_oddrow')

    @debug(lvl=logging.DEBUG, prefix='')
    def treeview_sort_column(self, col, reverse):
        # self.manager.busy()
        item_list = [(self.treeview.set(k, col), k) for k in self.treeview.get_children('')]
        item_list.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(item_list):
            self.treeview.move(k, '', index)
        self.stripe_rows()
        # reverse sort next time
        self.treeview.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))
        # self.manager.not_busy()

    @debug(lvl=logging.DEBUG, prefix='')
    def tv_refresh(self):
        # self.manager.busy()
        item_list = list(self.treeview.get_children(''))
        item_list.sort(key=lambda x: int(x))
        for item_iid, item_obj in sorted(self.item_obj_dict.items()):
            TreeviewConstructor.logger.log(logging.DEBUG, "Item ID: {0}".format(item_iid))
            # l = self.treeview.get_children('')
            for index, k in enumerate(item_list):
                TreeviewConstructor.logger.log(logging.DEBUG, "k: {0}".format(k))
                if str(item_iid) == str(k):
                    self.treeview.delete(k)
                    item_obj.index = index
                    self.treeview.insert(item_obj.parent, item_obj.index, iid=item_obj.iid, values=item_obj.values_list)
                    item_list.remove(k)
                    break
        self.stripe_rows()
        # self.manager.not_busy()

    @debug(lvl=logging.DEBUG, prefix='')
    def add_column(self,
                   order=None,
                   col_id=None,
                   hdr_txt="",
                   anchor=tk.W,
                   stretch=tk.YES,
                   minwidth=0,
                   width=50,
                   display=True,
                   desc=None):
        col_obj = TreeColumn(order=order,
                             col_id=col_id,
                             hdr_txt=hdr_txt,
                             anchor=anchor,
                             stretch=stretch,
                             minwidth=minwidth,
                             width=width,
                             display=display,
                             desc=desc)
        self.col_obj_dict[col_obj.col_id] = col_obj

    @debug(lvl=logging.NOTSET, prefix='')
    def add_item(self,
                 iid,
                 parent="",
                 index=tk.END,
                 values_dict=None):
        item_obj = TreeRow(treeview_const=self,
                           iid=iid,
                           parent=parent,
                           index=index,
                           values_dict=values_dict)
        self.item_obj_dict[item_obj.iid] = item_obj

    @debug(lvl=logging.DEBUG, prefix='')
    def columns_from_query(self, query, hide_list=None, pref_order=None):
        if pref_order is None:
            pref_order = []
        if hide_list is None:
            hide_list = []

        col_order = 1
        col_order += len(pref_order)
        TreeviewConstructor.logger.log(logging.DEBUG, "Column Order Starting Value: {0}".format(str(col_order)))

        for desc in query.column_descriptions:
            name = desc.get('name').replace("'", "").replace('"', "")
            TreeviewConstructor.logger.log(logging.DEBUG, "Column Name: {0}".format(name))
            disp = True
            if name in hide_list:
                disp = False
            cust_order = col_order
            if name in pref_order:
                cust_order = pref_order.index(name) + 1
            self.add_column(
                order=cust_order,
                col_id=name.replace(" ", "_"),
                hdr_txt=name,
                display=disp,
                desc=desc
            )
            if name not in pref_order:
                col_order += 1

    @debug(lvl=logging.DEBUG, prefix='')
    def rows_from_query(self, query, id_col="line_number", limit=None, parent_col=None):
        counter = 1
        for row in query.all():
            temp_dict = {}
            for col_obj in self.col_obj_dict.values():
                # noinspection PyProtectedMember
                value = row._asdict().get(col_obj.hdr_txt)
                if isinstance(value, str):
                    value.replace("{", "").replace("}", "")
                temp_dict[str(col_obj.order)] = value
            counter += 1
            if counter == limit:
                break
            parent = ""
            if parent_col is not None:
                # noinspection PyProtectedMember
                if str(row._asdict().get(id_col)) != str(row._asdict().get(parent_col)):
                    # noinspection PyProtectedMember
                    parent = str(row._asdict().get(parent_col))
            # noinspection PyProtectedMember
            self.add_item(iid=str(row._asdict().get(id_col)), values_dict=temp_dict, parent=parent)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_query(self,
                       query,
                       hide_list=None,
                       pref_order=None,
                       id_col="line_number",
                       limit=None,
                       checkwidth=0,
                       parent_col=None):
        the_query = query
        self.columns_from_query(the_query, hide_list, pref_order)
        self.populate_cols(checkwidth=checkwidth)
        self.rows_from_query(the_query, id_col, limit, parent_col)
        self.populate_items()
        self.stripe_rows()


class TreeColumn(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 order=None,
                 col_id=None,
                 hdr_txt="",
                 anchor=tk.W,
                 stretch=tk.YES,
                 minwidth=0,
                 width=50,
                 display=True,
                 desc=None):
        self.order = order
        self.col_id = col_id
        self.hdr_txt = hdr_txt
        self.__format = None
        self.anchor = anchor
        self.stretch = stretch
        self.minwidth = minwidth
        self.width = width
        self.display = display
        self.desc = desc


class TreeRow(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 treeview_const,
                 iid,
                 parent="",
                 index=tk.END,
                 values_dict=None):
        self.treeview_const = treeview_const
        self.parent = parent
        self.index = index
        self.iid = iid
        self.tags_list = []
        self.values_dict = values_dict
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
            TreeRow.logger.log(logging.DEBUG, "Temp Col Keys: {0}".format(temp_col_keys))
            temp_xl_keys = list(self.xl_cells.keys())
            temp_xl_keys.sort(key=lambda x: int(x))
            TreeRow.logger.log(logging.DEBUG, "Temp XL Keys: {0}".format(temp_xl_keys))
            # for col_id, col_obj in sorted(temp_col_dict.items(), key=lambda x: x[1].order):
            for col_id in reversed(temp_col_keys):
                match = False
                TreeRow.logger.log(logging.DEBUG, "Col ID: {0}, Order: {1}"
                                   .format(col_id, str(self.treeview_const.col_obj_dict[col_id].order)))
                for col_order in reversed(temp_xl_keys):
                    TreeRow.logger.log(logging.DEBUG, "Col Order: {0}".format(str(col_order)))
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
                        TreeRow.logger.log(logging.DEBUG, "Column ID Match! Col_Order: {0}, Formatted Value: {1}"
                                           .format(str(col_order), cell_obj.formatted_value))
                        TreeRow.logger.log(logging.DEBUG, "Removing values from list: {0}, {1}"
                                           .format(col_id, col_order))
                        temp_col_keys.remove(col_id)
                        temp_xl_keys.remove(col_order)
                        break
                if not match:
                    TreeRow.logger.log(logging.DEBUG, "No Match. Appending empty value")
                    temp_dict[str(self.treeview_const.col_obj_dict[col_id].order)] = ""
            for order in sorted(temp_dict.keys(), key=lambda x: int(x)):
                value = temp_dict[order]
                TreeRow.logger.log(logging.DEBUG, "temp dict key and value: {0}, {1}".format(order, value))
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
