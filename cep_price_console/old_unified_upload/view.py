from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
from cep_price_console.utils.gui_utils import center_window
from cep_price_console.old_unified_upload.step import Step
from cep_price_console.old_unified_upload.input_param import FileSelection
from cep_price_console.old_unified_upload.match_review import MatchReview
from cep_price_console.old_unified_upload.col_map import ColumnMapping
from cep_price_console.old_unified_upload.model import Model
from cep_price_console.old_unified_upload.treeview import TreeviewConstructor
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import logging
import os
import xlsxwriter


class View(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.root = self.master.root
        super().__init__(self.root, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.model = Model(self)
        self.file_selection = None
        self.col_mapper = None
        self.match_review = None
        self.vpn_rev = None
        self.pop_frames = False
        self.checked_dict = None

        # Force the window to sit on top of the Price Console Dashboard
        # self.attributes("-topmost", "true")
        self.title("Contract Upload Procedure: Step 1")
        self.iconbitmap(config.ICON_FILE)
        # Center window on screen
        center_window(win_obj=self)
        # Force the notebook to fill the window
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.flow_manager()

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        msgbox = messagebox.askokcancel("Quit", "Do you want to quit?", parent=self)
        if msgbox:
            self.destroy()

    # TODO: Create some unified function that would accept a step "id" and init/destroy without having separate fns
    # TODO: Each step's next/prev button should run this unified function instead of a step-specific one.
    @debug(lvl=logging.DEBUG, prefix='')
    def flow_manager(self):
        if self.file_selection is None:
            self.file_selection = FileSelection(view=self)
            center_window(win_obj=self)
        elif Step.step_dict.get("FileSelection").complete:
            if self.col_mapper is None:
                self.file_selection.close()
                self.model.sql_import()
                self.col_mapper = ColumnMapping(view=self)
                self.col_mapper.populate_frame()
                center_window(win_obj=self)
            elif Step.step_dict.get("ColumnMapping").complete:
                if self.match_review is None:
                    self.col_mapper.close()
                    self.match_review = MatchReview(view=self)
                    self.match_review.populate_frame()
                    center_window(win_obj=self)
                elif Step.step_dict.get("MatchReview").complete:
                    self.model.check_upload_table(self.checked_dict)
                    output_query = self.model.get_output_query()

                    filename_options = dict(
                        title='Save Output',
                        initialdir=str(os.path.expanduser('~')).replace('\\', '/'),
                        initialfile=None,
                        parent=self.root,
                        filetypes=[('Workbook', '.xlsx')])

                    fullpath_var = str(filedialog.asksaveasfilename(**filename_options)).replace("/", "\\")
                    filename, _ = os.path.splitext(fullpath_var)
                    workbook = xlsxwriter.Workbook('{}.xlsx'.format(filename))
                    worksheet = workbook.add_worksheet()
                    col_number = 0
                    row_number = 0
                    col_list = []
                    for desc in output_query.column_descriptions:
                        name = desc.get('name').replace("'", "").replace('"', "")
                        col_list.append(name)
                        worksheet.write(row_number, col_number, name)

                        col_number += 1

                    row_number += 1
                    for row in output_query.all():
                        col_number = 0
                        for col_name in col_list:
                            # noinspection PyProtectedMember
                            value = row._asdict().get(col_name)
                            if isinstance(value, str):
                                value.replace("{", "").replace("}", "")
                            worksheet.write(row_number, col_number, value)
                            col_number += 1
                        row_number += 1
                    workbook.close()
                    self.close()
                    # if self.vpn_rev is None and \
                    #         self.model.func_dict.get("Vendor Part Number Revision").upload_col is not None:
                    #     self.match_review.close()
                    #     self.model.check_upload_table(self.checked_dict)
                    #     self.vpn_rev = PartNumRevision(view=self)
                    #     self.vpn_rev.populate_frame()
                    #     center_window(win_obj=self)

                    # if not self.pop_frames:
                    #     self.process_definition()
                    # for next_step in sorted(Step.step_dict.values(), key=lambda x: int(x.order)):
                    #     if not next_step.complete:
                    #         print("Here's where you would do something")
                    #         break

    def process_definition(self):
        pass
        # if self.model.func_dict.get("Action Indicator").upload_col is not None:
        #     self.action_ind = ActionIndicator(view=self)
        # if self.model.func_dict.get("Primary UOM").upload_col is not None:
        #     self.uom = UnitOfMeasure(view=self)


class PartNumRevision(Step):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        super().__init__(namely=str(PartNumRevision.__name__), order=4, view=view, *args, **kwargs)
        self.part_num_rev_hdr = ttk.Label(self.frame_main)
        self.part_num_rev_hdr.config(text="Vendor Part Number Revision", style="heading1.TLabel")
        self.part_num_rev_hdr.grid(row=0, column=0, sticky=tk.NW)

        self.part_num_rev_instr_lbl = ttk.Label(self.frame_main)
        self.part_num_rev_instr_lbl.config(text="These are the instructions on how to do this thing. \n"
                                                "1) You need to do something. \n"
                                                "2) You need to do something else. \n"
                                                "3) Finally, you need to do something else. \n"
                                                "Then you are done!")
        self.part_num_rev_instr_lbl.grid(row=1, column=0)

        self.treeview = TreeviewConstructor(self.frame_main)
        self.treeview.grid(row=2,
                           column=0,
                           sticky=tk.NSEW)

        self.btn_next.state(['!disabled'])

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_frame(self):
        pass

    @debug(lvl=logging.DEBUG, prefix='')
    def next(self, *args):
        self.complete = True
        self.view.flow_manager()


class ActionIndicator(Step):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        super().__init__(namely=str(ActionIndicator.__name__), order=5, view=view, *args, **kwargs)


class UnitOfMeasure(Step):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view, *args, **kwargs):
        super().__init__(namely=str(ColumnMapping.__name__), order=5, view=view, *args, **kwargs)

