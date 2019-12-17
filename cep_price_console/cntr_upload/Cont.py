from cep_price_console.cntr_upload.Model import *
from cep_price_console.cntr_upload.View_Master import *
from cep_price_console.utils.log_utils import CustomAdapter, debug
import logging


class CntrUploadCont(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, master):
        self.master = master
        self.model = CntrUploadModel(self)
        self.view = CntrUploadView(self)
        self.view.load_window()

    @debug(lvl=logging.NOTSET, prefix='')
    def on_closing_cont(self):
        del self.model

    # region Step_1  ###################################################################################################
    @debug(lvl=logging.DEBUG, prefix='')
    def set_ws_fullpath(self, fullpath):
        try:
            self.model.workbook_fullpath_pretty = fullpath
        except Exception as e:
            raise e

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_ws_list(self):
        return self.model.wb.ws_lst

    @debug(lvl=logging.NOTSET, prefix='')
    def set_ws_sel(self, value):
        self.model.wb.ws_sel = value

    @debug(lvl=logging.NOTSET, prefix='')
    def set_header_row(self, value):
        self.model.wb.header_row = value
        return self.model.wb.row_count, self.model.wb.col_count

    @debug(lvl=logging.NOTSET, prefix='')
    def set_last_row(self, value):
        try:
            self.model.last_row = value
        except Exception as ex:
            template = "A last_row_set exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            CntrUploadCont.logger.error(message)

    @debug(lvl=logging.NOTSET, prefix='')
    def set_last_col(self, value):
        try:
            self.model.last_col = value
        except Exception as ex:
            template = "A last_col_set exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            CntrUploadCont.logger.error(message)
    # endregion ########################################################################################################

    # region last_col  #################################################################################################
    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_workbook(self):
        return self.model.get_wb()

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_upload_map_dict(self):
        return self.model.upload_map_dict

    @debug(lvl=logging.NOTSET, prefix='')
    def upload_contract(self):
        self.model.upload_contract()

    @debug(lvl=logging.NOTSET, prefix='')
    def reset_contract(self):
        self.model.reset_contract()

    @debug(lvl=logging.NOTSET, prefix='')
    def ecolab_rule(self):
        self.model.ecolab_rule()

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_distinct_cntr(self):
        return self.model.fetch_distinct_cntr()

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_cntr_details(self, vend_cntr):
        return self.model.fetch_cntr_details(vend_cntr)

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_prod_sel_tbl(self):
        return self.model.fetch_prod_sel_tbl()

    @debug(lvl=logging.NOTSET, prefix='')
    def delete_unchecked_prod_matches(self, prod_sel_lst):
        self.model.delete_unchecked_prod_matches(prod_sel_lst)

    @debug(lvl=logging.NOTSET, prefix='')
    def populate_upload_matched_tbl(self):
        self.model.populate_upload_matched_tbl()

    @debug(lvl=logging.NOTSET, prefix='')
    def fetch_upload_matched_tbl(self):
        return self.model.fetch_upload_matched_tbl()

    @debug(lvl=logging.NOTSET, prefix='')
    def __del__(self):
        pass

    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_csv_results(self):
        return self.model.fetch_csv_results()

    @debug(lvl=logging.DEBUG, prefix='')
    def supply_cntr_match(self, cep_cntr_match):
        self.model.supply_cntr_match(cep_cntr_match)

    @debug(lvl=logging.DEBUG, prefix='')
    def prepare_repository_and_filename(self):
        self.model.prepare_repository_and_filename()

    @debug(lvl=logging.DEBUG, prefix='')
    def move_contract_wb(self):
        self.model.move_contract_wb()

    @debug(lvl=logging.DEBUG, prefix='')
    def save_csv_export(self):
        self.model.save_csv_export()

    @debug(lvl=logging.DEBUG, prefix='')
    def remove_cep_cntr_info(self):
        self.model.remove_cep_cntr_info()
