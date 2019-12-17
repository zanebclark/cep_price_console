from tkinter import *
from tkinter.ttk import *
import logging
from cep_price_console.cntr_upload.CntrUploadTab import CntrUploadTab
from cep_price_console.cntr_upload.Treeview import TreeviewConstructor, TreeColumn, TreeRow
from cep_price_console.utils.log_utils import CustomAdapter, debug


class Step4ProductNumberMatches(CntrUploadTab):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, master, tab_text, tab_state='normal'):
        CntrUploadTab.__init__(self,
                               master,
                               tab_text,
                               tab_state)
        self.prod_sel_tbl = None
        self.prod_match_header = Label(self.frame_main)
        self.prod_match_instr = Label(self.frame_main)
        self.prod_match_frame = Frame(self.frame_main)
        self.prod_match_treeview = None

    # noinspection PyProtectedMember
    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        self.frame_main.columnconfigure(0, weight=1)
        self.prod_sel_tbl = self.cont.fetch_prod_sel_tbl()
        self.prod_match_header.config(text="Product Matching", font=('Verdana Bold', '20'))
        self.prod_match_header.grid(row=0, column=0, sticky=NW)
        self.prod_match_instr.config(text="These are instructions...")
        self.prod_match_instr.grid(row=1, column=0)
        self.prod_match_frame.grid(row=2, column=0, sticky=NSEW)
        self.frame_main.rowconfigure(2, weight=1)
        self.prod_match_treeview = TreeviewConstructor(self, self.prod_match_frame, checkwidth=35)
        self.btn_next.state(['!disabled'])
        self.btn_next.bind("<ButtonRelease-1>", self.proceeding)
        self.btn_prev.bind("<ButtonRelease-1>", self.reversing)

        col_order = 1
        for item in self.prod_sel_tbl.all():
            for col_name in item.keys():
                obj = TreeColumn(order=col_order,
                                 col_id=col_name,
                                 hdr_txt=col_name.replace("_", " "))
                if col_name == "Prod_Match_ID":
                    obj.display = False
                self.prod_match_treeview.col_obj_dict[col_name] = obj
                col_order += 1
            break

        self.prod_match_treeview.populate_cols()

        for query_row in self.prod_sel_tbl.all():
            item = TreeRow(
                treeview_const=self.prod_match_treeview,
                iid=query_row.Prod_Match_ID
            )
            for col_obj in self.prod_match_treeview.col_obj_dict.values():
                item.values_dict[str(col_obj.order)] = query_row._asdict().get(col_obj.col_id)
            if query_row.Count != 1:
                item.tags_list.append('red')
            if query_row.Customer_Part_Number is not None and query_row.CEP_Part_Number is None:
                item.tags_list.append('red')
            self.prod_match_treeview.item_obj_dict[str(item.iid)] = item
        self.prod_match_treeview.populate_items()
        self.prod_match_treeview.stripe_rows()

        for item_iid, item_obj in self.prod_match_treeview.item_obj_dict.items():
            count_order = str(self.prod_match_treeview.col_obj_dict["Count"].order)
            cep_pn_order = str(self.prod_match_treeview.col_obj_dict["CEP_Part_Number"].order)
            if item_obj.values_dict[count_order] == 1:
                if item_obj.values_dict[cep_pn_order] is not None:
                    self.prod_match_treeview.treeview.change_state(item_iid, 'checked')
                elif item_obj.values_dict[cep_pn_order] is None:
                    self.prod_match_treeview.treeview.change_state(item_iid, 'unchecked')

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def proceeding(self, events):
        self.manager.busy()
        prod_sel_lst = self.prod_match_treeview.treeview.get_checked()
        self.cont.delete_unchecked_prod_matches(prod_sel_lst)
        self.cont.populate_upload_matched_tbl()
        self.master.step_5.populate_frame()
        self.master.tab_switcher(4)
        self.manager.not_busy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def reversing(self, events):
        self.cont.remove_cep_cntr_info()
