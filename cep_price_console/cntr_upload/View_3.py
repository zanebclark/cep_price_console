from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import logging
from cep_price_console.cntr_upload.CntrUploadTab import CntrUploadTab
from cep_price_console.cntr_upload.Treeview import TreeviewConstructor, TreeColumn, TreeRow
from cep_price_console.utils.log_utils import CustomAdapter, debug


class Step3ContractMatching(CntrUploadTab):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, master, tab_text, tab_state='normal'):
        CntrUploadTab.__init__(self,
                               master,
                               tab_text,
                               tab_state)
        # Header and instructions
        self.cntr_matching_hdr = Label(self.frame_main)
        self.cntr_matching_instr = Label(self.frame_main)
        self.cntr_distinct_values = None
        self.cntr_matches = []
        # Master Matching Frame
        self.matching_frame = Frame(self.frame_main)
        self.matching_dict = {}

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        self.cntr_distinct_values = self.cont.fetch_distinct_cntr()
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.rowconfigure(2, weight=1)
        self.cntr_matching_hdr.config(text="Contract Matching", font=('Verdana Bold', '20'))
        self.cntr_matching_hdr.grid(row=0, column=0)
        self.cntr_matching_instr.config(text="These are the instructions...")
        self.cntr_matching_instr.grid(row=1, column=0)
        self.matching_frame.grid(row=2, column=0, sticky=NSEW)
        self.matching_frame.columnconfigure(0, weight=1)
        self.matching_frame.rowconfigure(0, weight=1)
        self.btn_next.state(['!disabled'])
        self.btn_next.bind("<ButtonRelease-1>", self.proceeding)

        row_to_pass = 0
        Step3ContractMatching.logger.info("I'm about to populate the cntr matching frames!")
        for (vend_cntr,) in self.cntr_distinct_values:
            Step3ContractMatching.logger.info("Distinct Vendor Contract Number: {0}".format(vend_cntr))
            cntr_details = self.cont.fetch_cntr_details(vend_cntr)
            obj = VendCntrMatch(self, vend_cntr, cntr_details, row_to_pass)
            self.matching_dict[vend_cntr] = obj
            self.matching_frame.rowconfigure(row_to_pass, weight=1)
            row_to_pass += 1

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def proceeding(self, *args):
        self.manager.busy()
        error = False
        self.cntr_matches = []
        for obj in self.matching_dict.values():
            if obj.cep_cntr_match is None:
                error = True
                break
            else:
                # self.cntr_matches.append((obj.vend_cntr, obj.cep_cntr_match, obj.exp_date))
                self.cntr_matches.append(obj.cep_cntr_match)
        if error:
            msgbox = messagebox.askokcancel(
                "Missing Contract Selections",
                "Contract selection(s) are missing. Please select a match for all contracts before proceeding.",
                parent=self.master
            )
        else:
            # for (vend_cntr, cep_cntr_match, exp_date) in self.cntr_matches:
            for cep_cntr_match in self.cntr_matches:
                for k, v in cep_cntr_match.items():
                    print("Key: {0}, Value: {1}".format(k, v))
                self.cont.supply_cntr_match(cep_cntr_match)
                # self.cont.append_cep_cntr_val(cep_cntr_match, vend_cntr)
                # self.cont.supply_missing_exp_date(exp_date)
                # print(exp_date)
                # base_filename = cep_cntr_match + "_" + vend_cntr + "_" + exp_date
                # self.cont.supply_base_filename(base_filename)
            self.master.step_4.populate_frame()
            self.master.tab_switcher(3)
        self.manager.not_busy()


class VendCntrMatch(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, vend_cntr, cntr_details, row):
        self.master = master
        self.frame = self.master.matching_frame
        self.master_row = row
        self.vend_cntr = vend_cntr
        self.cep_cntr_match = None
        # self.exp_date = None
        self.vend_cntr_match_frame = Frame(self.frame)

        # Vendor Contract Number
        self.vend_cntr_num_frame = Frame(self.vend_cntr_match_frame)
        self.vend_cntr_num_label = Label(self.vend_cntr_num_frame)
        self.vend_cntr_num_entry = Entry(self.vend_cntr_num_frame)
        self.vend_cntr_num_var = StringVar()

        # Contract Selection
        self.cntr_sel_frame = Frame(self.vend_cntr_match_frame)
        self.column_lst = []
        self.value_dict = {}
        self.parent_dict = {}
        self.treeview = TreeviewConstructor(self, self.cntr_sel_frame, checkwidth=60)
        self.cntr_details = cntr_details
        self.manager = self.master.manager
        self.populate_frame()

    # noinspection PyProtectedMember
    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        for _ in self.cntr_details.column_descriptions:
            name = _.get('name').replace(" ", "_").replace("'", "").replace('"', "")
            VendCntrMatch.logger.log(logging.NOTSET, "Name: {0}".format(name))
            self.column_lst.append(name)

        col_order = 1
        for col in self.column_lst:
            VendCntrMatch.logger.log(logging.NOTSET, "Column ID: {0}".format(col))
            obj = TreeColumn(order=col_order,
                             col_id=col,
                             hdr_txt=col.replace("_", " "))
            if col == "ID":
                VendCntrMatch.logger.log(logging.NOTSET, "Hiding Column.")
                obj.display = False
            self.treeview.col_obj_dict[col] = obj
            col_order += 1

        self.treeview.populate_cols()

        # Populate Parents
        for query_row in self.cntr_details.all():
            VendCntrMatch.logger.log(logging.NOTSET, "Row Info: {0}".format(query_row))
            if query_row.Vendor_Number in ("", None):
                id_val = "N/A"
            else:
                id_val = query_row.Vendor_Number
            VendCntrMatch.logger.log(logging.NOTSET, "ID Val: {0}".format(id_val))
            self.parent_dict[id_val] = None
        VendCntrMatch.logger.log(logging.NOTSET, "Now for the parents:")
        for parent in self.parent_dict.keys():
            VendCntrMatch.logger.log(logging.NOTSET, "Parent ID Val: {parent}".format(parent=parent))
            item = TreeRow(
                treeview_const=self.treeview,
                iid=parent
            )

            for col_obj in self.treeview.col_obj_dict.values():
                if col_obj.col_id == "Vendor_Number":
                    item.values_dict[str(col_obj.order)] = parent
                else:
                    item.values_dict[str(col_obj.order)] = "--------------------------------------------"
            self.treeview.item_obj_dict[str(item.iid)] = item

        # Populate Children
        VendCntrMatch.logger.log(logging.NOTSET, "Now for the children:")
        for query_row in self.cntr_details.all():
            if query_row.Vendor_Number in ("", None):
                parent = "N/A"
            else:
                parent = query_row.Vendor_Number
            VendCntrMatch.logger.log(logging.NOTSET, "Row Info: {0}, Parent: {1}, iid: {2}".
                                     format(query_row, parent, query_row.ID))
            item = TreeRow(
                treeview_const=self.treeview,
                iid=query_row.ID,
                parent=parent
            )

            for col_obj in self.treeview.col_obj_dict.values():
                if col_obj.col_id != "Vendor_Number":
                    item.values_dict[str(col_obj.order)] = query_row._asdict().get(col_obj.col_id)
                    VendCntrMatch.logger.log(logging.NOTSET,
                                             "Column Number: {0}, Value: {1}, Type: {2}".
                                             format(col_obj.order,
                                                    query_row._asdict().get(col_obj.col_id),
                                                    type(query_row._asdict().get(col_obj.col_id))))
                if col_obj.col_id == "Vendor_Number":
                    item.values_dict[str(col_obj.order)] = ""
                    VendCntrMatch.logger.log(logging.NOTSET,
                                             "Column Number: {0}, Value: {1}".
                                             format(col_obj.order, query_row._asdict().get(col_obj.col_id)))
            self.treeview.item_obj_dict[str(item.iid)] = item
        self.treeview.populate_items()
        self.treeview.stripe_rows()

        self.vend_cntr_match_frame.grid(row=self.master_row, column=0, sticky=NSEW)
        self.vend_cntr_match_frame.columnconfigure(0, weight=1)
        self.vend_cntr_match_frame.rowconfigure(1, weight=1)

        # Vendor Contract Number
        self.vend_cntr_num_var.set(self.vend_cntr)
        self.vend_cntr_num_frame.grid(row=0, column=0, sticky=NSEW)
        self.vend_cntr_num_label.config(text="For Vendor Contract Number: ")
        self.vend_cntr_num_label.grid(row=0, column=0, sticky=NW)
        self.vend_cntr_num_entry.config(textvariable=self.vend_cntr_num_var, state='disabled')
        self.vend_cntr_num_entry.grid(row=0, column=1, sticky=NW)

        # Contract Selection
        self.cntr_sel_frame.columnconfigure(0, weight=1)
        self.cntr_sel_frame.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        self.treeview.treeview.bind("<Button-1>", self.clicking, True)

    @debug(lvl=logging.DEBUG, prefix='')
    def clicking(self, event):
        self.manager.busy()
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.treeview.treeview.identify_row(y)
            if self.treeview.treeview.tag_has("checked", item) or self.treeview.treeview.tag_has("tristate", item):
                matching_dict = {}
                item_obj = self.treeview.item_obj_dict.get(str(item))
                col_key_lst = list(self.treeview.col_obj_dict.keys())
                VendCntrMatch.logger.log(logging.DEBUG, "Column Key List: {0}".format(col_key_lst))
                for col_key in col_key_lst:
                    VendCntrMatch.logger.log(logging.DEBUG, "Column Key: {0}".format(col_key))
                    col_obj = self.treeview.col_obj_dict.get(col_key)
                    VendCntrMatch.logger.log(logging.DEBUG, "Column Obj: {0}".format(col_obj))
                    matching_dict[col_obj.col_id] = item_obj.values_dict.get(str(col_obj.order))

                self.cep_cntr_match = matching_dict

                for parent in self.parent_dict.keys():
                    self.treeview.treeview.change_state(parent, "unchecked")
                    children = self.treeview.treeview.get_children(parent)
                    for iid in children:
                        self.treeview.treeview.change_state(iid, "unchecked")
                self.treeview.treeview.change_state(item, "checked")
        self.manager.not_busy()
