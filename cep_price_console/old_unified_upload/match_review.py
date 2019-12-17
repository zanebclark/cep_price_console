from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.old_unified_upload.step import Step
import logging
from cep_price_console.old_unified_upload.treeview import TreeviewConstructor
import tkinter as tk
import tkinter.ttk as ttk


class MatchReview(Step):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        super().__init__(namely=str(MatchReview.__name__), order=3, view=view, *args, **kwargs)
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.rowconfigure(2, weight=1)
        self.match_query = None
        self.match_review_hdr = ttk.Label(self.frame_main)
        self.match_review_hdr.config(text="Match Review", style="heading1.TLabel")
        self.match_review_hdr.grid(row=0, column=0, sticky=tk.NW)

        self.match_review_instr_lbl = ttk.Label(self.frame_main)
        self.match_review_instr_lbl.config(text="These are the instructions on how to do this thing. \n"
                                                "1) You need to do something. \n"
                                                "2) You need to do something else. \n"
                                                "3) Finally, you need to do something else. \n"
                                                "Then you are done!")
        self.match_review_instr_lbl.grid(row=1, column=0)

        self.treeview = TreeviewConstructor(self.frame_main)
        self.treeview.grid(row=2,
                           column=0,
                           sticky=tk.NSEW)
        self.btn_next.state(['!disabled'])

        self.expand_all_btn = ttk.Button(self.frame_cmd)
        self.expand_all_btn.config(text="Expand All", command=self.expand_all)
        self.expand_all_btn.grid(row=0, column=0)

        self.collapse_all_btn = ttk.Button(self.frame_cmd)
        self.collapse_all_btn.config(text="Collapse All", command=self.collapse_all)
        self.collapse_all_btn.grid(row=0, column=1)

        self.check_all_btn = ttk.Button(self.frame_cmd)
        self.expand_all_btn.config(text="Expand All", command=self.expand_all)
        self.expand_all_btn.grid(row=0, column=0)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def expand_all(self, *args):
        self.treeview.treeview.expand_all()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def collapse_all(self, *args):
        self.treeview.treeview.collapse_all()

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        self.match_query = self.view.model.all_match_gui_query()

        self.treeview.populate_query(query=self.match_query,
                                     hide_list=["ID_1", "ID_2"],
                                     pref_order=["Match_Type"],
                                     checkwidth=30,
                                     id_col="ID_2",
                                     limit=None,
                                     parent_col="ID_1")
        for item in self.treeview.item_obj_dict.values():
            self.treeview.treeview.change_state(item.iid, "checked")
            if item.parent == "":
                if item.values_dict.get("5") in (None, ""):
                    self.treeview.treeview.tag_del(item.iid, "parent_evenrow")
                    self.treeview.treeview.tag_del(item.iid, "child_evenrow")
                    self.treeview.treeview.tag_add(item.iid, "red")
                    self.treeview.treeview.change_state(item.iid, "unchecked")
                    # noinspection PyProtectedMember
                    self.treeview.treeview._uncheck_descendant(item.iid)

    @debug(lvl=logging.DEBUG, prefix='')
    def next(self, *args):
        checked_dict = {}
        for checked_box in self.treeview.treeview.get_checked():
            checked_box_obj = self.treeview.item_obj_dict.get(checked_box)
            checked_box_parent_obj = self.treeview.item_obj_dict.get(checked_box_obj.parent)
            checked_dict[checked_box_parent_obj.iid] = self.treeview.item_obj_dict.get(checked_box_parent_obj.iid)
        self.complete = True
        self.view.checked_dict = checked_dict
        self.view.flow_manager()

# TODO: Sort by error
# TODO: Check all
# TODO: Uncheck all
