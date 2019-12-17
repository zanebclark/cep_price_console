from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
from cep_price_console.utils.gui_utils import center_window
from cep_price_console.unified_upload.view_1_file_selection import FileSelection
from cep_price_console.unified_upload.view_2_worksheet_selection import WorksheetSelection
from cep_price_console.unified_upload.view_3_column_mapping import ColumnSelection
from cep_price_console.unified_upload.model import Model
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import logging

"""
Make a list of a available steps. In the model? Maybe. Initially, this list will be the input file, 
but there might be branching logic that would append a different step for contract uploads or 
essendant cost updates. 
1) start with file selection
2) when the filepath is valid, enable the proceed button
3) if the step id isn't the smallest id, grid the previous button
4) if the step id isn't the highest, grid the next button

"""
"""
All of the steps need to be initialisable without data. The application needs to be stateless. Moving the view from 
one state to another should require some logic, but the views should exist and be populated with the appropriate data
upon transition

Steps: 
1) File selection
    Encoding dropdown
    Which formats do I accommodate?
3) Header row hinting / Column Hinting/ Ignore empty columns
    Some tools have some logic built in to detect this. Feed it in and ask the user to verify it
4) Which vendor is this? Is it a customer? 
    Use the paned frame approach from the price list along with the tkintertable selection method
5) Column Datatype Definition/Function Mapping
    This is the hardest part. Do I upload the data into SQL and then re-upload it with the new data definition when the 
        user changes it? 
    Or, do I keep the data in memory and upload post data type selection? 
    
    
Need: 
Universal button status function that calls the current step's get button status method that checks to see if we're 
    ready to move on
"""


class View(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master, *args, **kwargs):
        self.master = master
        super().__init__(*args, **kwargs)
        self.title("Contract Upload Procedure: Step 1")
        self.iconbitmap(config.FAVICON)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.model = Model(self)
        self.col_mapper = None
        self.match_review = None
        self.vpn_rev = None
        self.pop_frames = False
        self.checked_dict = None

        self.column_mapping_dataframe = None

        self.current_step_index = 0

        # Force the notebook to fill the window
        self.protocol("WM_DELETE_WINDOW", self.close)

        # something = FileSelection(self)

        # self.frame_main = ttk.Frame(self,
        #                             style="odd.group.TFrame")
        # self.frame_main.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame_cmd = ttk.Frame(self,
                                   style="even.group.TFrame")
        self.frame_cmd.grid(row=1, column=0, sticky=tk.E + tk.SW)
        self.frame_cmd.columnconfigure(0, weight=1)

        self.btn_next = ttk.Button(self.frame_cmd,
                                   text="Proceed",
                                   command=self.next)

        self.btn_next.grid(row=0, column=1, sticky=tk.SE)

        self.btn_prev = ttk.Button(self.frame_cmd,
                                   text="Previous",
                                   command=self.prev)
        self.btn_prev.grid(row=0, column=0, sticky=tk.SW)
        self.btn_prev.grid_remove()

        self.all_steps = {
            "file_selection": FileSelection(self),
            "sheet_selection": WorksheetSelection(self),
            "column_selection": ColumnSelection(self)
        }
        self.avail_step_list = []
        self.testing()
        self.avail_step_list.append(self.all_steps["file_selection"])

        self.current_step_index = 0
        self.avail_step_list[self.current_step_index].open()

        # Center window on screen
        center_window(win_obj=self, width=1000, height=800)
        self.update_next_status()

    @debug(lvl=logging.DEBUG, prefix='')
    def reset_downstream(self):
        close_list = self.avail_step_list[self.current_step_index+1:]
        print("Close List: ")
        for step in close_list:
            print(str(step.__class__))
            step.close()
        self.avail_step_list = [step for step in self.avail_step_list if step not in close_list]

    @debug(lvl=logging.DEBUG, prefix='')
    def testing(self):
        self.wb_filename = config.MEDIA_PATH / "LAGB_02-25-2019_test3.xlsx"
        self.ws_name_selection = "ESSENDANT FEBRUARY"
        self.header_row = 1
        self.btn_prev.grid()

    # region wb_filename ###############################################################################################
    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def wb_filename(self):
        return self.model.wb_filename

    @wb_filename.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def wb_filename(self, value):
        if value != self.model.wb_filename:
            self.reset_downstream()
            self.model.wb_filename = value
            self.column_mapping_dataframe = None
            if self.all_steps["sheet_selection"] not in self.avail_step_list:
                self.avail_step_list.append(self.all_steps["sheet_selection"])
                self.update_next_status()
            else:
                raise ValueError
    # endregion ########################################################################################################

    # region ws_sheet_names ############################################################################################
    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def ws_sheet_names(self):
        return self.model.ws_sheet_names
    # endregion ########################################################################################################

    # region ws_name_selection #########################################################################################
    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def ws_name_selection(self):
        return self.model.ws_name_selection

    @ws_name_selection.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def ws_name_selection(self, value):
        if value != self.model.ws_name_selection:
            self.reset_downstream()
            self.model.ws_name_selection = value
            self.column_mapping_dataframe = None
            if self.all_steps["column_selection"] not in self.avail_step_list:
                self.avail_step_list.append(self.all_steps["column_selection"])
                self.update_next_status()
    # endregion ########################################################################################################

    # region header_row #########################################################################################
    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def header_row(self):
        return self.model.header_row

    @header_row.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def header_row(self, value):
        if value != self.model.ws_name_selection:
            self.reset_downstream()
            self.model.header_row = value
            self.column_mapping_dataframe = None
            if self.all_steps["column_selection"] not in self.avail_step_list:
                self.avail_step_list.append(self.all_steps["column_selection"])
                self.update_next_status()
    # endregion ########################################################################################################

    # region Directory Section  ########################################################################################
    @debug(lvl=logging.DEBUG, prefix='')
    def flow_manager(self, add=False, subtract=False):
        self.avail_step_list[self.current_step_index].close()
        if add:
            self.current_step_index += 1
        elif subtract:
            self.current_step_index -= 1
        current_step_obj = self.avail_step_list[self.current_step_index]
        current_step_obj.open()
        if current_step_obj.initial:
            self.btn_prev.grid_remove()
        else:
            self.btn_prev.grid()

        if current_step_obj.terminal:
            self.btn_next.grid_remove()
        else:
            self.btn_next.grid()
        self.update_next_status()

    @debug(lvl=logging.DEBUG, prefix='')
    def update_next_status(self):
        print("Next Button Disable Logic:")
        print(self.current_step_index)
        print(len(self.avail_step_list)-1)
        if self.current_step_index == len(self.avail_step_list) - 1:
            self.btn_next.state(['disabled'])
        else:
            self.btn_next.state(['!disabled'])

    @debug(lvl=logging.DEBUG, prefix='')
    def close(self):
        msgbox = messagebox.askokcancel("Quit", "Do you want to quit?", parent=self)
        if msgbox:
            self.destroy()

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def next(self, *args):
        self.flow_manager(add=True)

    # noinspection PyUnusedLocal
    @debug(lvl=logging.DEBUG, prefix='')
    def prev(self, *args):
        self.flow_manager(subtract=True)

#
#     # TODO: Create some unified function that would accept a step "id" and init/destroy without having separate fns
#     # TODO: Each step's next/prev button should run this unified function instead of a step-specific one.
#     @debug(lvl=logging.DEBUG, prefix='')
#     def flow_manager(self):
#         if self.file_selection is None:
#             self.file_selection = FileSelection(view=self)
#             center_window(win_obj=self)
#         elif Step.step_dict.get("FileSelection").complete:
#             if self.col_mapper is None:
#                 self.file_selection.close()
#                 self.model.sql_import()
#                 self.col_mapper = ColumnMapping(view=self)
#                 self.col_mapper.populate_frame()
#                 center_window(win_obj=self)
#             elif Step.step_dict.get("ColumnMapping").complete:
#                 if self.match_review is None:
#                     self.col_mapper.close()
#                     self.match_review = MatchReview(view=self)
#                     self.match_review.populate_frame()
#                     center_window(win_obj=self)
#                 elif Step.step_dict.get("MatchReview").complete:
#                     self.model.check_upload_table(self.checked_dict)
#                     output_query = self.model.get_output_query()
#
#                     filename_options = dict(
#                         title='Save Output',
#                         initialdir=str(os.path.expanduser('~')).replace('\\', '/'),
#                         initialfile=None,
#                         parent=self.root,
#                         filetypes=[('Workbook', '.xlsx')])
#
#                     fullpath_var = str(filedialog.asksaveasfilename(**filename_options)).replace("/", "\\")
#                     filename, _ = os.path.splitext(fullpath_var)
#                     workbook = xlsxwriter.Workbook('{}.xlsx'.format(filename))
#                     worksheet = workbook.add_worksheet()
#                     col_number = 0
#                     row_number = 0
#                     col_list = []
#                     for desc in output_query.column_descriptions:
#                         name = desc.get('name').replace("'", "").replace('"', "")
#                         col_list.append(name)
#                         worksheet.write(row_number, col_number, name)
#
#                         col_number += 1
#
#                     row_number += 1
#                     for row in output_query.all():
#                         col_number = 0
#                         for col_name in col_list:
#                             # noinspection PyProtectedMember
#                             value = row._asdict().get(col_name)
#                             if isinstance(value, str):
#                                 value.replace("{", "").replace("}", "")
#                             worksheet.write(row_number, col_number, value)
#                             col_number += 1
#                         row_number += 1
#                     workbook.close()
#                     self.close()
#                     # if self.vpn_rev is None and \
#                     #         self.model.func_dict.get("Vendor Part Number Revision").upload_col is not None:
#                     #     self.match_review.close()
#                     #     self.model.check_upload_table(self.checked_dict)
#                     #     self.vpn_rev = PartNumRevision(view=self)
#                     #     self.vpn_rev.populate_frame()
#                     #     center_window(win_obj=self)
#
#                     # if not self.pop_frames:
#                     #     self.process_definition()
#                     # for next_step in sorted(Step.step_dict.values(), key=lambda x: int(x.order)):
#                     #     if not next_step.complete:
#                     #         print("Here's where you would do something")
#                     #         break
#
#     def process_definition(self):
#         pass
#         # if self.model.func_dict.get("Action Indicator").upload_col is not None:
#         #     self.action_ind = ActionIndicator(view=self)
#         # if self.model.func_dict.get("Primary UOM").upload_col is not None:
#         #     self.uom = UnitOfMeasure(view=self)
#
#
# class PartNumRevision(Step):
#     logger = CustomAdapter(logging.getLogger(str(__name__)), None)
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def __init__(self, view, *args, **kwargs):
#         super().__init__(namely=str(PartNumRevision.__name__), order=4, view=view, *args, **kwargs)
#         self.part_num_rev_hdr = ttk.Label(self.frame_main)
#         self.part_num_rev_hdr.config(text="Vendor Part Number Revision", style="heading1.TLabel")
#         self.part_num_rev_hdr.grid(row=0, column=0, sticky=tk.NW)
#
#         self.part_num_rev_instr_lbl = ttk.Label(self.frame_main)
#         self.part_num_rev_instr_lbl.config(text="These are the instructions on how to do this thing. \n"
#                                                 "1) You need to do something. \n"
#                                                 "2) You need to do something else. \n"
#                                                 "3) Finally, you need to do something else. \n"
#                                                 "Then you are done!")
#         self.part_num_rev_instr_lbl.grid(row=1, column=0)
#
#         self.treeview = TreeviewConstructor(self.frame_main)
#         self.treeview.grid(row=2,
#                            column=0,
#                            sticky=tk.NSEW)
#
#         self.btn_next.state(['!disabled'])
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def populate_frame(self):
#         pass
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def next(self, *args):
#         self.complete = True
#         self.view.flow_manager()
#
#
# class ActionIndicator(Step):
#     logger = CustomAdapter(logging.getLogger(str(__name__)), None)
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def __init__(self, view, *args, **kwargs):
#         super().__init__(namely=str(ActionIndicator.__name__), order=5, view=view, *args, **kwargs)
#
#
# class UnitOfMeasure(Step):
#     logger = CustomAdapter(logging.getLogger(str(__name__)), None)
#
#     @debug(lvl=logging.DEBUG, prefix='')
#     def __init__(self, view, *args, **kwargs):
#         super().__init__(namely=str(ColumnMapping.__name__), order=5, view=view, *args, **kwargs)
#


