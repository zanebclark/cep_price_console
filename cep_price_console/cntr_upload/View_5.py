from tkinter import *
from tkinter.ttk import *
from cep_price_console.cntr_upload.CntrUploadTab import CntrUploadTab
from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.cntr_upload.Treeview import TreeviewConstructor, TreeColumn, TreeRow
import logging


class Step5ReviewUpload(CntrUploadTab):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, master, tab_text, tab_state='normal'):
        CntrUploadTab.__init__(self,
                               master,
                               tab_text,
                               tab_state)

        # Instructions Frame
        self.instr_frame = Frame(self.frame_main)
        self.instr_lbl = Label(self.instr_frame)

        # Review upload values
        self.review_frame = Frame(self.frame_main)
        self.review_treeview = None
        self.upload_matched_tbl = None
        self.csv_results = None
        self.column_lst = []

    # noinspection PyProtectedMember
    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        # Main Frame
        self.btn_prev.grid_remove()
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.rowconfigure(1, weight=1)
        self.upload_matched_tbl = self.cont.fetch_upload_matched_tbl()

        self.instr_frame.grid(row=0, column=0)
        self.instr_lbl.config(text="This is the header", font=('Verdana Bold', '20'))
        self.instr_lbl.grid(row=0, column=0)

        self.review_frame.grid(row=1, column=0, sticky=NSEW)
        self.review_frame.columnconfigure(0, weight=1)
        self.review_frame.rowconfigure(0, weight=1)
        self.review_treeview = TreeviewConstructor(self, self.review_frame, False)
        self.btn_next.state(['!disabled'])
        self.btn_next.bind("<ButtonRelease-1>", self.proceeding)

        for _ in self.upload_matched_tbl.column_descriptions:
            name = _.get('name').replace(" ", "_").replace("'", "").replace('"', "")
            Step5ReviewUpload.logger.log(logging.DEBUG, "Name: {0}".format(name))
            self.column_lst.append(name)

        col_order = 1
        for col in self.column_lst:
            Step5ReviewUpload.logger.log(logging.DEBUG, "Column ID: {0}".format(col))
            obj = TreeColumn(order=col_order,
                             col_id=col,
                             hdr_txt=col.replace("_", " "))
            if col in ("UploadMatched_ID", "UploadMono_ID", "UploadMulti_ID"):
                Step5ReviewUpload.logger.log(logging.DEBUG, "Hiding Column.")
                obj.display = False
            self.review_treeview.col_obj_dict[col] = obj
            col_order += 1

        self.review_treeview.populate_cols()

        for query_row in self.upload_matched_tbl.all():
            Step5ReviewUpload.logger.log(logging.NOTSET, "Row Info: {0}".format(query_row))
            item = TreeRow(
                treeview_const=self.review_treeview,
                iid=query_row.UploadMatched_ID
            )
            for col_obj in self.review_treeview.col_obj_dict.values():
                item.values_dict[str(col_obj.order)] = query_row._asdict().get(col_obj.col_id)
            self.review_treeview.item_obj_dict[str(item.iid)] = item
        self.review_treeview.populate_items()
        self.review_treeview.stripe_rows()

    # noinspection PyUnusedLocal
    def proceeding(self, events):
        self.manager.busy()
        self.cont.prepare_repository_and_filename()
        self.cont.save_csv_export()
        self.cont.move_contract_wb()
        self.manager.not_busy()

