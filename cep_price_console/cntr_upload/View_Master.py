from cep_price_console.cntr_upload.View_1 import *
from cep_price_console.cntr_upload.View_2 import *
from cep_price_console.cntr_upload.View_3 import *
from cep_price_console.cntr_upload.View_4 import *
from cep_price_console.cntr_upload.View_5 import *
from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils import config
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import logging


class CntrUploadView(tk.Toplevel):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, vc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vc = vc
        self.window_dims = (1200, 800)
        self.center_coords = []
        self.nb = Notebook(self)
        self.current_tab_id = -1
        self.step_1 = Step1FileSelection(self, 'Step 1: File Selection', 'normal')
        self.step_2 = Step2ColumnMapping(self, 'Step 2: Column Mapping', 'disabled')
        self.step_3 = Step3ContractMatching(self, 'Step 3: Contract Matching', 'disabled')
        self.step_4 = Step4ProductNumberMatches(self, 'Step 4: Product Selection', 'disabled')
        self.step_5 = Step5ReviewUpload(self, 'Step 5: Review Upload', 'disabled')
        self.step_6 = Step5ReviewUpload(self, 'Step 6', 'disabled')
        self.tab_list = [
            self.step_1,
            self.step_2,
            self.step_3,
            self.step_4,
            self.step_5,
            self.step_6
        ]
        self.max_tab_id = len(self.tab_list) - 1
        self.load_window()

    @debug(lvl=logging.NOTSET, prefix='')
    def tab_id_assignment(self):
        value = self.current_tab_id
        self.current_tab_id = value + 1
        CntrUploadView.logger.log(logging.NOTSET, "Tab ID: {0}".format(str(self.current_tab_id)))
        return self.current_tab_id

    @debug(lvl=logging.NOTSET, prefix='')
    def load_window(self):
        # Force the window to sit on top of the Price Console Dashboard
        self.attributes("-topmost", "true")
        self.title("Contract Upload Procedure: Step 1")
        self.iconbitmap(config.ICON_FILE)

        # region Center Popup on screen
        screen = (self.winfo_screenwidth(), self.winfo_screenheight())
        for i in range(0, 2):
            i = int(round((screen[i]/2)-(self.window_dims[i]/2)))
            self.center_coords.append(i)
        self.geometry("{0}x{1}+{2}+{3}".format(self.window_dims[0],
                                               self.window_dims[1],
                                               self.center_coords[0],
                                               self.center_coords[1]))
        # endregion

        # Force the notebook to fill the window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # region Append frames to notebook and assign id values
        self.step_1.nbook_add()
        self.step_2.nbook_add()
        self.step_3.nbook_add()
        self.step_4.nbook_add()
        self.step_5.nbook_add()
        self.step_6.nbook_add()
        # endregion

        # Grid the notebook on the window and force it to fill
        self.nb.grid(row=0, column=0, sticky=NSEW)

        self.protocol("WM_DELETE_WINDOW", self.on_closing_view)

    @debug(lvl=logging.DEBUG, prefix='')
    def on_closing_view(self):
        msgbox = messagebox.askokcancel("Quit", "Do you want to quit?", parent=self)
        if msgbox:
            self.destroy()
            self.vc.on_closing_cont()

    @debug(lvl=logging.NOTSET, prefix='')
    def tab_switcher(self, target_step_id):
        self.nb.select(target_step_id)
        for tb in self.tab_list:
            if tb.tab_id == target_step_id:
                tb.toggle_tab("normal")
                self.nb.select(target_step_id)
            else:
                tb.toggle_tab("disabled")
