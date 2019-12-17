from cep_price_console.cntr_upload.Declarative import UploadMulti, UploadMono, ProductMatching, UploadMatched
from cep_price_console.db_management.server_utils import mysql_engine, mysql_session_maker
from cep_price_console.utils.excel_utils import Workbook
from cep_price_console.utils.log_utils import CustomAdapter, debug
from cep_price_console.utils.utils import is_pathname_valid
from cep_price_console.utils.config import config
import logging
from sqlalchemy import update, and_, not_, func, exc, Integer, literal, case, select, or_
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import aliased
import shutil
import csv
import datetime
import os


# noinspection PyComparisonWithNone
class CntrUploadModel(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, vc):
        self.session = mysql_session_maker()
        self.vc = vc
        self.wb = None
        # Workbook information
        self.__workbook_fullpath_pretty = None
        self.__last_row = None
        self.__last_col = None
        self.worksheet_full = {}
        self.worksheet_col_dict = {}
        self.tree_column_dict = {}
        self.tree_row_dict = {}
        self.tree_cell_dict = {}
        self.worksheet_col_names = {}
        self.cnx = None
        self.upload_map_dict = {}
        for col in UploadMulti.__table__.columns:
            mapping_obj = UploadMapping(
                mapping_id=col.name,
                datatype=col.type,
                label=col.doc,
                col_obj=col,
                static_value=None
            )
            self.upload_map_dict[mapping_obj.mapping_id] = mapping_obj
        self.upload_cols_map = []
        self.vend_cntr_num_list = []
        self.vend_cntr_num_map = []
        self.vend_part_num_list = []
        self.vend_part_num_map = []
        self.cep_cntr_match = None
        self.file_repository = config["directory"]["contract_dir"]
        self.contract_repository = None
        self.upload_filename = None
        # Fill in vendor cntr number if not on columns
        # SQL Upload script (new temp table)
        # SQL script Step 1
        # SQL script Step 2
        # Delete bad matches
        # SWL script Step 3

    # region workbook_fullpath_pretty  #################################################################################
    @property
    @debug(lvl=logging.DEBUG, prefix='')
    def workbook_fullpath_pretty(self):
        return self.__workbook_fullpath_pretty

    @workbook_fullpath_pretty.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def workbook_fullpath_pretty(self, value):
        try:
            self.wb = Workbook(value)
        except Exception as e:
            raise e
        else:
            self.__workbook_fullpath_pretty = value
    # endregion ########################################################################################################

    @debug(lvl=logging.DEBUG, prefix='')
    def prepare_repository_and_filename(self):
        self.contract_repository = os.path.normpath(
            os.path.join(self.file_repository, self.cep_cntr_match.get("CEP_Contract_Number")))
        CntrUploadModel.logger.log(logging.DEBUG, "Contract Repository: {0}".format(self.contract_repository))
        if is_pathname_valid(self.contract_repository):
            if not os.path.exists(self.contract_repository):
                CntrUploadModel.logger.log(logging.DEBUG, "Repository doesn't exist. Creating.")
                os.mkdir(self.contract_repository)
            else:
                CntrUploadModel.logger.log(logging.DEBUG, "Repository exist.")
        else:
            CntrUploadModel.logger.log(logging.DEBUG, "Pathname not valid.")

        self.upload_filename = "{repository}\\{date_stamp}_{cep_cntr_numb}_{vend_cntr_num}_Exp{exp_date}".\
            format(date_stamp=datetime.datetime.today().strftime("%m-%d-%Y"),
                   repository=self.contract_repository,
                   cep_cntr_numb=self.cep_cntr_match.get("CEP_Contract_Number"),
                   vend_cntr_num=self.cep_cntr_match.get("Vendor_Contract_Number"),
                   exp_date=datetime.date.strftime(self.cep_cntr_match.get("Expiration_Date"), "%m-%d-%Y"))
        print("Repository: {0}".format(self.upload_filename))

    @debug(lvl=logging.DEBUG, prefix='')
    def move_contract_wb(self):
        src_base = os.path.basename(self.workbook_fullpath_pretty)
        _, src_ext = os.path.splitext(src_base)
        dest_filename = "{filename}_Contract{ext}".format(filename=self.upload_filename, ext=src_ext)
        shutil.copy2(self.workbook_fullpath_pretty, dest_filename)

    # region last_row  #################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def last_row(self):
        return self.__last_row

    @last_row.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def last_row(self, value):
        if value not in (0, ""):
            if isinstance(value, int):
                self.__last_row = value
            else:
                CntrUploadModel.logger.error("last_row Type Error: {0}".format(str(type(value))))
        else:
            CntrUploadModel.logger.info("Setter called with an empty value. No action taken.")

    # endregion ########################################################################################################

    # region last_col  #################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def last_col(self):
        return self.__last_col

    @last_col.setter
    @debug(lvl=logging.NOTSET, prefix='')
    def last_col(self, value):
        if isinstance(value, int):
            if value != "":
                CntrUploadModel.__last_col = value
            else:
                CntrUploadModel.logger.info("Setter called with an empty value. No action taken.")
        else:
            CntrUploadModel.logger.error("last_col Type Error: {0}".format(str(type(value))))

    # endregion ########################################################################################################
    @debug(lvl=logging.DEBUG, prefix='')
    def schema_create_if_not_exists(self, schema_name):
        if not self.schema_exists(schema_name):
            self.schema_create(schema_name)

    @debug(lvl=logging.DEBUG, prefix='')
    def schema_exists(self, schema_name):
        try:
            mysql_engine.execute("SHOW CREATE SCHEMA `{0}`;".format(schema_name)).scalar()
            CntrUploadModel.logger.log(logging.NOTSET, "Schema Exists: {0}".format(schema_name))
            return True
        except exc.DBAPIError:
            CntrUploadModel.logger.log(logging.NOTSET, "Schema Does Not Exist: {0}".format(schema_name))
            return False

    @debug(lvl=logging.DEBUG, prefix='')
    def schema_create(self, schema_name):
        CntrUploadModel.logger.log(logging.NOTSET, "Creating Schema: {0}".format(schema_name))
        mysql_engine.execute(CreateSchema(schema_name))

    @debug(lvl=logging.DEBUG, prefix='')
    def table_create_if_not_exists(self, schema_name, table_name, table_obj_name):
        self.schema_create_if_not_exists(schema_name)
        if not self.table_exists(schema_name, table_name):
            self.table_create(table_obj_name)
        else:
            self.table_drop(table_obj_name)
            self.table_create(table_obj_name)

    @debug(lvl=logging.DEBUG, prefix='')
    def table_exists(self, schema_name, table_name):
        if not mysql_engine.dialect.has_table(mysql_engine, table_name, schema=schema_name):
            CntrUploadModel.logger.log(logging.NOTSET,
                                       "Table does not exist: {0}.{1}".format(schema_name, table_name))
            return False
        else:
            CntrUploadModel.logger.log(logging.NOTSET,
                                       "Table exists: {0}.{1}".format(schema_name, table_name))
            return True

    @debug(lvl=logging.DEBUG, prefix='')
    def table_create(self, table_obj_name):
        statement = "{table_obj_name}.__table__.create({engine_name})" \
            .format(table_obj_name=table_obj_name,
                    engine_name="mysql_engine")
        CntrUploadModel.logger.log(logging.NOTSET, "{table_obj_name} Create Statement: {statement}".
                                   format(table_obj_name=table_obj_name,
                                          statement=statement))
        exec(statement)

    @debug(lvl=logging.DEBUG, prefix='')
    def table_drop(self, table_obj_name):
        CntrUploadModel.logger.log(logging.DEBUG, "{table_obj_name} Drop".
                                   format(table_obj_name=table_obj_name))
        statement = "{table_obj_name}.__table__.drop({engine_name})" \
            .format(table_obj_name=table_obj_name,
                    engine_name="mysql_engine")
        CntrUploadModel.logger.log(logging.DEBUG, "{table_obj_name} Drop Statement: {statement}".
                                   format(table_obj_name=table_obj_name,
                                          statement=statement))
        exec(statement)
        CntrUploadModel.logger.log(logging.DEBUG, "{table_obj_name} Post Drop".
                                   format(table_obj_name=table_obj_name))

    @debug(lvl=logging.DEBUG, prefix='')
    def create_matched_tbl(self):
        if not mysql_engine.dialect.has_table(mysql_engine, 'upload_matched', schema="pythontest"):
            UploadMatched.__table__.create(mysql_engine)
        else:
            UploadMatched.__table__.drop(mysql_engine)
            UploadMatched.__table__.create(mysql_engine)

    @debug(lvl=logging.DEBUG, prefix='')
    def __del__(self):
        pass

    @debug(lvl=logging.NOTSET, prefix='')
    def get_wb(self):
        return self.wb

    @debug(lvl=logging.DEBUG, prefix='')
    def reset_contract(self):
        self.table_create_if_not_exists("pythontest", "upload_multi", "UploadMulti")

    @debug(lvl=logging.DEBUG, prefix='')
    def ecolab_rule(self):
        # noinspection PyPep8
        stmt = UploadMono.__table__.update().\
            where(UploadMono.__table__.c.ContrPrice.isnot(None)).\
            values({'ContrCost': UploadMono.__table__.c.ContrPrice * .9})

        mysql_engine.execute(stmt)

    @debug(lvl=logging.DEBUG, prefix='')
    def upload_contract(self):
        self.table_create_if_not_exists("pythontest", "upload_multi", "UploadMulti")

        dict_of_lists = {}
        dict_of_static = {}
        upload_id_list = list(self.upload_map_dict.keys())
        for upload_id in reversed(upload_id_list):
            upload_obj = self.upload_map_dict[upload_id]
            if upload_obj.ws_col_obj is not None:
                CntrUploadModel.logger.log(logging.DEBUG,
                                           "Upload Mapping with a Worksheet Column: {0}. Appending to list."
                                           .format(str(upload_id)))
                upload_col_cell_list = list(upload_obj.ws_col_obj.col_cells)
                upload_col_cell_list.sort(key=lambda x: int(x.row_num_one_indexed))
                dict_of_lists[upload_id] = upload_col_cell_list
            elif upload_obj.static_value is not None:
                CntrUploadModel.logger.log(logging.DEBUG,
                                           "Upload Mapping with a static value: {0}. Appending to list."
                                           .format(str(upload_id)))
                dict_of_static[upload_id] = upload_obj.static_value
            else:
                CntrUploadModel.logger.log(logging.NOTSET,
                                           "Upload Mapping without a Worksheet Column: {0}. Skipping."
                                           .format(str(upload_id)))

        if bool(dict_of_lists):
            dict_upload_obj = {}
            row_num_list = list(sorted(self.wb.row_dict.keys(), key=lambda x: int(x)))
            for row_num in reversed(row_num_list):
                upload_dict = {}
                for upload_id, upload_col_cell_list in dict_of_lists.items():
                    for cell in reversed(upload_col_cell_list):
                        if str(row_num) == str(cell.row_num_one_indexed):
                            upload_dict[upload_id] = cell.formatted_value
                            CntrUploadModel.logger.log(
                                logging.NOTSET,
                                "Row number: {0}, Cell Row Number: {1}, Upload ID: {2}, Value: {3}. Removing cell"
                                .format(
                                    str(row_num),
                                    str(cell.row_num_one_indexed),
                                    str(upload_id),
                                    str(cell.formatted_value))
                            )
                            upload_col_cell_list.remove(cell)
                            break
                        else:
                            CntrUploadModel.logger.log(
                                logging.NOTSET,
                                "No Match: Row number: {0}, Cell Row Number: {1}, Upload ID: {2}, Value: {3}."
                                .format(
                                    str(row_num),
                                    str(cell.row_num_one_indexed),
                                    str(upload_id),
                                    str(cell.formatted_value))
                            )
                if bool(dict_of_static):
                    for static_upload_id, static_upload_value in dict_of_static.items():
                        upload_dict[static_upload_id] = static_upload_value
                CntrUploadModel.logger.log(logging.DEBUG, "Upload Dictionary: {0}".format(
                    "".join(str(key) + str(value) for key, value in upload_dict.items())))
                upload_obj = UploadMulti(**upload_dict)
                CntrUploadModel.logger.log(logging.NOTSET, "Upload Object: {0}".format(upload_obj))
                # Append this object to the object dictionary
                dict_upload_obj[row_num] = upload_obj

            CntrUploadModel.logger.log(logging.DEBUG, "Create a list of dictionary values")
            list_upload_obj = list(dict_upload_obj.values())

            CntrUploadModel.logger.log(logging.DEBUG, "Add the list of new objects to the session")
            self.session.add_all(list_upload_obj)
            self.session.commit()

            # Delete empty rows from the multi-period landing
            CntrUploadModel.logger.log(logging.DEBUG, "Delete empty rows from the multi-period landing")
            # noinspection PyComparisonWithNone,PyComparisonWithNone,PyComparisonWithNone,PyComparisonWithNone,
            # PyComparisonWithNone,PyComparisonWithNone,PyComparisonWithNone,PyComparisonWithNone,PyComparisonWithNone,
            # PyComparisonWithNone,PyComparisonWithNone,PyComparisonWithNone,PyPep8
            # noinspection PyPep8
            del_stmt = UploadMulti.__table__.delete().where(and_(
                UploadMulti.__table__.c.P1_ContrPrice.is_(None),
                UploadMulti.__table__.c.P1_ContrCost.is_(None),
                UploadMulti.__table__.c.P1_EffDate.is_(None),
                UploadMulti.__table__.c.P1_ExpDate.is_(None),
                UploadMulti.__table__.c.P2_ContrPrice.is_(None),
                UploadMulti.__table__.c.P2_ContrCost.is_(None),
                UploadMulti.__table__.c.P2_EffDate.is_(None),
                UploadMulti.__table__.c.P2_ExpDate.is_(None),
                UploadMulti.__table__.c.P3_ContrPrice.is_(None),
                UploadMulti.__table__.c.P3_ContrCost.is_(None),
                UploadMulti.__table__.c.P3_EffDate.is_(None),
                UploadMulti.__table__.c.P3_ExpDate.is_(None)))

            mysql_engine.execute(del_stmt)

            CntrUploadModel.logger.log(logging.DEBUG,
                                       "GP Contracts often have an 'catch all' expiration date in the "
                                       "final period that should be applied to another period")
            # noinspection PyPep8
            stmt = UploadMulti.__table__.update().where((and_(
                UploadMulti.__table__.c.P1_ContrPrice.is_(None),
                UploadMulti.__table__.c.P1_ContrCost.is_(None),
                UploadMulti.__table__.c.P1_EffDate.is_(None)
            ))).values({'P1_ExpDate': None})

            mysql_engine.execute(stmt)

            CntrUploadModel.logger.log(logging.DEBUG, "Misplaced exp date 1")
            # noinspection PyPep8
            stmt = UploadMulti.__table__.update().where((and_(
                UploadMulti.__table__.c.P1_EffDate.isnot(None),
                UploadMulti.__table__.c.P1_ExpDate.is_(None),
                UploadMulti.__table__.c.P2_EffDate.is_(None),
                UploadMulti.__table__.c.P2_ExpDate.isnot(None),
                UploadMulti.__table__.c.P3_EffDate.is_(None),
                UploadMulti.__table__.c.P3_ExpDate.is_(None)
            ))).values({'P1_ExpDate': UploadMulti.__table__.c.P2_ExpDate,
                        'P2_ExpDate': None
                        })

            mysql_engine.execute(stmt)

            CntrUploadModel.logger.log(logging.DEBUG, "Misplaced exp date 2")
            # noinspection PyPep8
            stmt = UploadMulti.__table__.update().where((and_(
                UploadMulti.__table__.c.P1_EffDate.isnot(None),
                UploadMulti.__table__.c.P1_ExpDate.is_(None),
                UploadMulti.__table__.c.P2_EffDate.is_(None),
                UploadMulti.__table__.c.P2_ExpDate.is_(None),
                UploadMulti.__table__.c.P3_EffDate.is_(None),
                UploadMulti.__table__.c.P3_ExpDate.isnot(None)
            ))).values({'P1_ExpDate': UploadMulti.__table__.c.P3_ExpDate,
                        'P3_ExpDate': None
                        })

            mysql_engine.execute(stmt)

            CntrUploadModel.logger.log(logging.DEBUG, "Misplaced exp date 3")
            # noinspection PyPep8
            stmt = UploadMulti.__table__.update().where((and_(
                UploadMulti.__table__.c.P1_EffDate.is_(None),
                UploadMulti.__table__.c.P1_ExpDate.is_(None),
                UploadMulti.__table__.c.P2_EffDate.isnot(None),
                UploadMulti.__table__.c.P2_ExpDate.is_(None),
                UploadMulti.__table__.c.P3_EffDate.is_(None),
                UploadMulti.__table__.c.P3_ExpDate.isnot(None)
            ))).values({'P2_ExpDate': UploadMulti.__table__.c.P3_ExpDate,
                        'P3_ExpDate': None
                        })

            mysql_engine.execute(stmt)
            self.session.commit()
            mysql_session_maker.close_all()
            self.session = mysql_session_maker()
            self.table_create_if_not_exists("pythontest", "upload_mono", "UploadMono")
            # noinspection PyPep8
            period_1 = self.session.query(
                UploadMulti.__table__.c.ID.label("Upload_ID"),
                UploadMulti.__table__.c.VendCntrNum.label("VendCntrNum"),
                UploadMulti.__table__.c.VendProdNum.label("VendProdNum"),
                UploadMulti.__table__.c.CustProdNum.label("CustProdNum"),
                UploadMulti.__table__.c.QBreak.label("QBreak"),
                UploadMulti.__table__.c.UOM.label("UOM"),
                UploadMulti.__table__.c.P1_ContrPrice.label("ContrPrice"),
                UploadMulti.__table__.c.P1_ContrCost.label("ContrCost"),
                UploadMulti.__table__.c.P1_EffDate.label("EffDate"),
                UploadMulti.__table__.c.P1_ExpDate.label("ExpDate")
            ).filter(not_(and_(UploadMulti.__table__.c.P1_ContrPrice.is_(None),
                               UploadMulti.__table__.c.P1_ContrCost.is_(None),
                               UploadMulti.__table__.c.P1_EffDate.is_(None),
                               UploadMulti.__table__.c.P1_ExpDate.is_(None)
                               )))

            insert_1 = UploadMono.__table__.insert().from_select(
                [UploadMono.__table__.c.UploadMulti_ID,
                 UploadMono.__table__.c.VendCntrNum,
                 UploadMono.__table__.c.VendProdNum,
                 UploadMono.__table__.c.CustProdNum,
                 UploadMono.__table__.c.QBreak,
                 UploadMono.__table__.c.UOM,
                 UploadMono.__table__.c.ContrPrice,
                 UploadMono.__table__.c.ContrCost,
                 UploadMono.__table__.c.EffDate,
                 UploadMono.__table__.c.ExpDate],
                period_1
            )

            mysql_engine.execute(insert_1)

            # noinspection PyPep8
            period_2 = self.session.query(
                UploadMulti.__table__.c.ID.label("Upload_ID"),
                UploadMulti.__table__.c.VendCntrNum.label("VendCntrNum"),
                UploadMulti.__table__.c.VendProdNum.label("VendProdNum"),
                UploadMulti.__table__.c.CustProdNum.label("CustProdNum"),
                UploadMulti.__table__.c.QBreak.label("QBreak"),
                UploadMulti.__table__.c.UOM.label("UOM"),
                UploadMulti.__table__.c.P2_ContrPrice.label("ContrPrice"),
                UploadMulti.__table__.c.P2_ContrCost.label("ContrCost"),
                UploadMulti.__table__.c.P2_EffDate.label("EffDate"),
                UploadMulti.__table__.c.P2_ExpDate.label("ExpDate")
            ).filter(not_(and_(UploadMulti.__table__.c.P2_ContrPrice.is_(None),
                               UploadMulti.__table__.c.P2_ContrCost.is_(None),
                               UploadMulti.__table__.c.P2_EffDate.is_(None),
                               UploadMulti.__table__.c.P2_ExpDate.is_(None)
                               )))

            insert_2 = UploadMono.__table__.insert().from_select(
                [UploadMono.__table__.c.UploadMulti_ID,
                 UploadMono.__table__.c.VendCntrNum,
                 UploadMono.__table__.c.VendProdNum,
                 UploadMono.__table__.c.CustProdNum,
                 UploadMono.__table__.c.QBreak,
                 UploadMono.__table__.c.UOM,
                 UploadMono.__table__.c.ContrPrice,
                 UploadMono.__table__.c.ContrCost,
                 UploadMono.__table__.c.EffDate,
                 UploadMono.__table__.c.ExpDate],
                period_2
            )

            mysql_engine.execute(insert_2)

            # noinspection PyPep8
            period_3 = self.session.query(
                UploadMulti.__table__.c.ID.label("Upload_ID"),
                UploadMulti.__table__.c.VendCntrNum.label("VendCntrNum"),
                UploadMulti.__table__.c.VendProdNum.label("VendProdNum"),
                UploadMulti.__table__.c.CustProdNum.label("CustProdNum"),
                UploadMulti.__table__.c.QBreak.label("QBreak"),
                UploadMulti.__table__.c.UOM.label("UOM"),
                UploadMulti.__table__.c.P3_ContrPrice.label("ContrPrice"),
                UploadMulti.__table__.c.P3_ContrCost.label("ContrCost"),
                UploadMulti.__table__.c.P3_EffDate.label("EffDate"),
                UploadMulti.__table__.c.P3_ExpDate.label("ExpDate")
            ).filter(not_(and_(UploadMulti.__table__.c.P3_ContrPrice.is_(None),
                               UploadMulti.__table__.c.P3_ContrCost.is_(None),
                               UploadMulti.__table__.c.P3_EffDate.is_(None),
                               UploadMulti.__table__.c.P3_ExpDate.is_(None)
                               )))

            insert_3 = UploadMono.__table__.insert().from_select(
                [UploadMono.__table__.c.UploadMulti_ID,
                 UploadMono.__table__.c.VendCntrNum,
                 UploadMono.__table__.c.VendProdNum,
                 UploadMono.__table__.c.CustProdNum,
                 UploadMono.__table__.c.QBreak,
                 UploadMono.__table__.c.UOM,
                 UploadMono.__table__.c.ContrPrice,
                 UploadMono.__table__.c.ContrCost,
                 UploadMono.__table__.c.EffDate,
                 UploadMono.__table__.c.ExpDate],
                period_3
            )

            mysql_engine.execute(insert_3)

            del_stmt = UploadMono.__table__.delete().where(UploadMono.__table__.c.ExpDate < datetime.date.today())

            mysql_engine.execute(del_stmt)
            # noinspection PyPep8
            del_stmt = UploadMono.__table__.delete().where(UploadMono.__table__.c.VendProdNum.is_(None))

            mysql_engine.execute(del_stmt)

            self.session.commit()
            # noinspection PyPep8
            null_period = self.session.query(UploadMono.__table__.c.UploadMono_ID).\
                filter(UploadMono.__table__.c.Period.is_(None))
            period_cnt = 0

            while null_period.count() > 0:
                period_cnt += 1
                print("Len: {0}".format(null_period.count()))
                for _ in null_period.all():
                    print("Row:")
                    for field in _:
                        print(field)
                # noinspection PyPep8
                no_period = \
                    select([UploadMono.__table__.c.VendCntrNum,
                            UploadMono.__table__.c.VendProdNum,
                            UploadMono.__table__.c.QBreak,
                            UploadMono.__table__.c.UOM,
                            func.min(UploadMono.__table__.c.EffDate).label('mindate')])\
                    .group_by(UploadMono.__table__.c.VendCntrNum,
                              UploadMono.__table__.c.VendProdNum,
                              UploadMono.__table__.c.QBreak,
                              UploadMono.__table__.c.UOM)\
                    .where(UploadMono.__table__.c.Period.is_(None))\
                    .alias("no_period")
                for _ in mysql_engine.execute(no_period):
                    print(_)
                # print("Period {0}".format(period_cnt))
                # for _ in no_period:
                #     print(_) cast(UploadMono.__table__.c.EffDate, Date) == cast(no_period.c.mindate, Date)
                # ,
                # UploadMono.__table__.c.VendProdNum == no_period.c.VendProdNum,
                # UploadMono.__table__.c.QBreak == no_period.c.QBreak,
                # UploadMono.__table__.c.UOM == no_period.c.UOM

                # noinspection PyPep8
                append_period = UploadMono.__table__.update().where(and_(
                    or_(
                        and_(
                            UploadMono.__table__.c.VendCntrNum.is_(None),
                            no_period.c.VendCntrNum.is_(None)),
                        UploadMono.__table__.c.VendCntrNum == no_period.c.VendCntrNum),
                    or_(
                        and_(
                            UploadMono.__table__.c.VendProdNum.is_(None),
                            no_period.c.VendProdNum.is_(None)),
                        UploadMono.__table__.c.VendProdNum == no_period.c.VendProdNum),
                    or_(
                        and_(
                            UploadMono.__table__.c.QBreak.is_(None),
                            no_period.c.QBreak.is_(None)),
                        UploadMono.__table__.c.QBreak == no_period.c.QBreak),
                    or_(
                        and_(
                            UploadMono.__table__.c.UOM.is_(None),
                            no_period.c.UOM.is_(None)),
                        UploadMono.__table__.c.UOM == no_period.c.UOM),
                    or_(
                        and_(
                            UploadMono.__table__.c.EffDate.is_(None),
                            no_period.c.mindate.is_(None)),
                        UploadMono.__table__.c.EffDate == no_period.c.mindate))).\
                    values(Period=period_cnt)
                mysql_engine.execute(append_period)
                self.session.commit()
                if period_cnt > 1:
                    print("period count over 1")
                    monoalias = aliased(UploadMono)
                    # noinspection PyPep8
                    exp_date_query = self.session.query(
                        UploadMono.__table__.c.UploadMono_ID,
                        UploadMono.__table__.c.VendCntrNum,
                        UploadMono.__table__.c.VendProdNum,
                        UploadMono.__table__.c.QBreak,
                        UploadMono.__table__.c.UOM,
                        UploadMono.__table__.c.ExpDate,
                        monoalias.EffDate,
                        UploadMono.__table__.c.Period,
                        monoalias.Period,
                    ).join(monoalias, and_(
                        or_(monoalias.VendCntrNum == UploadMono.__table__.c.VendCntrNum,
                            and_(monoalias.VendCntrNum.is_(None), UploadMono.__table__.c.VendCntrNum.is_(None))),
                        or_(monoalias.VendProdNum == UploadMono.__table__.c.VendProdNum,
                            and_(monoalias.VendProdNum.is_(None), UploadMono.__table__.c.VendProdNum.is_(None))),
                        or_(monoalias.QBreak == UploadMono.__table__.c.QBreak,
                            and_(monoalias.QBreak.is_(None), UploadMono.__table__.c.QBreak.is_(None))),
                        or_(monoalias.UOM == UploadMono.__table__.c.UOM,
                            and_(monoalias.UOM.is_(None), UploadMono.__table__.c.UOM.is_(None))),
                        or_(monoalias.Period == UploadMono.__table__.c.Period + 1,
                            and_(monoalias.Period.is_(None), UploadMono.__table__.c.Period.is_(None)))
                    )).all()
                    for row in exp_date_query:
                        if row.EffDate is not None:
                            CntrUploadModel.logger.log(logging.DEBUG,
                                                       "Row: {{0}}".format(row.EffDate))
                            stmt = UploadMono.__table__.update().where(
                                UploadMono.__table__.c.UploadMono_ID == row.UploadMono_ID
                            ).values({'ExpDate': row.EffDate - datetime.timedelta(days=1)})
                            mysql_engine.execute(stmt)
                    self.session.commit()
        else:
            CntrUploadModel.logger.error("No Upload Mapping with a Worksheet Column. Function skipped.")

    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_distinct_cntr(self):
        query = self.session.query(UploadMono.__table__.c.VendCntrNum.label("DistinctVendCntrNum")). \
            distinct(UploadMono.__table__.c.VendCntrNum)
        return query

    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_cntr_details(self, cntr_val):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping

        if cntr_val is None:
            query = self.session.query(
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.ID,
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Num.label("Vendor_Number"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num.label("Vendor_Contract_Number"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num.label("CEP_Contract_Number"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Desc.label("Description"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Eff_Date.label("Effective_Date"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Exp_Date.label("Expiration_Date")). \
                order_by(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Num.asc()). \
                order_by(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num.asc())
        else:
            query = self.session.query(
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.ID,
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Num.label("Vendor_Number"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num.label("Vendor_Contract_Number"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num.label("CEP_Contract_Number"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Desc.label("Description"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Eff_Date.label("Effective_Date"),
                ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Exp_Date.label("Expiration_Date")). \
                filter(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num == cntr_val). \
                order_by(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Num.asc()). \
                order_by(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num.asc())
        return query

    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_prod_sel_tbl(self):
        self.session.commit()
        query = self.session.query(ProductMatching.__table__.c.Prod_Match_ID,
                                   ProductMatching.__table__.c.VendProdNum.label("Vendor_Product_Number"),
                                   ProductMatching.__table__.c.Vendor_ID.label("Vendor_ID"),
                                   ProductMatching.__table__.c.CEP_Part_Num.label("CEP_Part_Number"),
                                   ProductMatching.__table__.c.CustProdNum.label("Customer_Part_Number"),
                                   ProductMatching.__table__.c.Count.label("Count")). \
            order_by(ProductMatching.__table__.c.Count.desc())
        return query

    @debug(lvl=logging.DEBUG, prefix='')
    def delete_unchecked_prod_matches(self, prod_sel_lst):
        delete = ProductMatching.__table__.delete().where(
            ~ProductMatching.__table__.c.Prod_Match_ID.in_(prod_sel_lst))
        mysql_engine.execute(delete)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_upload_matched_tbl(self):
        self.table_create_if_not_exists("pythontest", "upload_matched", "UploadMatched")

        query = self.session.query(
            UploadMono.__table__.c.UploadMono_ID,
            UploadMono.__table__.c.UploadMulti_ID,
            UploadMono.__table__.c.VendCntrNum,
            UploadMono.__table__.c.CEPCntrNum,
            UploadMono.__table__.c.Vendor_ID,
            UploadMono.__table__.c.VendProdNum,
            ProductMatching.__table__.c.CEP_Part_Num,
            UploadMono.__table__.c.CustProdNum,
            UploadMono.__table__.c.QBreak,
            UploadMono.__table__.c.UOM,
            UploadMono.__table__.c.ContrPrice,
            UploadMono.__table__.c.ContrCost,
            UploadMono.__table__.c.EffDate,
            UploadMono.__table__.c.ExpDate,
            UploadMono.__table__.c.Period,
        ).filter(and_(UploadMono.__table__.c.Vendor_ID == ProductMatching.__table__.c.Vendor_ID,
                      UploadMono.__table__.c.VendProdNum == ProductMatching.__table__.c.VendProdNum))
        # ).outerjoin(ProductMatching,
        #             and_(UploadMono.__table__.c.Vendor_ID == ProductMatching.__table__.c.Vendor_ID,
        #                  UploadMono.__table__.c.VendProdNum == ProductMatching.__table__.c.VendProdNum))

        insert = UploadMatched.__table__.insert().from_select(
            [UploadMatched.__table__.c.UploadMono_ID,
             UploadMatched.__table__.c.UploadMulti_ID,
             UploadMatched.__table__.c.VendCntrNum,
             UploadMatched.__table__.c.CEPCntrNum,
             UploadMatched.__table__.c.Vendor_ID,
             UploadMatched.__table__.c.VendProdNum,
             UploadMatched.__table__.c.CEPProdNum,
             UploadMatched.__table__.c.CustProdNum,
             UploadMatched.__table__.c.QBreak,
             UploadMatched.__table__.c.UOM,
             UploadMatched.__table__.c.ContrPrice,
             UploadMatched.__table__.c.ContrCost,
             UploadMatched.__table__.c.EffDate,
             UploadMatched.__table__.c.ExpDate,
             UploadMatched.__table__.c.Period],
            query
        )

        mysql_engine.execute(insert)

    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_upload_matched_tbl(self):
        self.session.commit()
        query = self.session.query(
            UploadMatched.__table__.c.UploadMatched_ID,
            UploadMatched.__table__.c.UploadMono_ID,
            UploadMatched.__table__.c.UploadMulti_ID,
            UploadMatched.__table__.c.VendCntrNum.label("Vend_Cntr_Num"),
            UploadMatched.__table__.c.CEPCntrNum.label("CEP_Cntr_Num"),
            UploadMatched.__table__.c.Vendor_ID.label("Vendor_ID"),
            UploadMatched.__table__.c.VendProdNum.label("Vend_Prod_Num"),
            UploadMatched.__table__.c.CEPProdNum.label("CEP_Prod_Num"),
            UploadMatched.__table__.c.CustProdNum.label("Cust_Prod_Num"),
            UploadMatched.__table__.c.QBreak.label("Q_Break"),
            UploadMatched.__table__.c.UOM,
            UploadMatched.__table__.c.ContrPrice.label("Contr_Price"),
            UploadMatched.__table__.c.ContrCost.label("Contr_Cost"),
            UploadMatched.__table__.c.EffDate.label("Eff_Date"),
            UploadMatched.__table__.c.ExpDate.label("Exp_Date"),
            UploadMatched.__table__.c.Period)
        return query

    # noinspection PyPep8
    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_csv_results(self, period):
        price_n = case([(UploadMatched.ContrPrice.isnot(None), "N"),
                        (UploadMatched.ContrPrice.is_(None), "")], else_='problem').label("Price_N")
        cost_n = case([(UploadMatched.ContrCost.isnot(None), "N"),
                       (UploadMatched.ContrCost.is_(None), "")], else_='problem').label("Cost_N")

        query = self.session.query(
            UploadMatched.__table__.c.CEPProdNum.label("CEP_Prod_Num"),
            UploadMatched.__table__.c.CEPCntrNum.label("CEP_Cntr_Num"),
            price_n,
            UploadMatched.__table__.c.ContrPrice.label("Price_Amt"),
            cost_n,
            UploadMatched.__table__.c.ContrCost.label("Cost_Amt"),
            UploadMatched.__table__.c.EffDate.label("Eff_Date"),
            UploadMatched.__table__.c.ExpDate.label("Exp_Date"),
            literal("0", Integer).label("Load_Pcnt")
        ).filter(UploadMatched.__table__.c.Period == period)
        return query

    @debug(lvl=logging.DEBUG, prefix='')
    def supply_cntr_match(self, cep_cntr_match):
        self.cep_cntr_match = cep_cntr_match
        self.append_cep_cntr_info()
        self.populate_prod_sel_tbl()
        # self.supply_missing_exp_date()

    @debug(lvl=logging.DEBUG, prefix='')
    def append_cep_cntr_info(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping

        cep_cntr = self.session.query(
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num,
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Cntr_Num,
            ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Vend_Num
        ).filter(ARW_PRF_Mapping.cntr_header_01_current.__table__.c.Cntr_Num ==
                 self.cep_cntr_match.get("CEP_Contract_Number")).first()

        stmt = update(UploadMono). \
            values(CEPCntrNum=cep_cntr.Cntr_Num,
                   Vendor_ID=cep_cntr.Vend_Num)
        mysql_engine.execute(stmt)

        # noinspection PyPep8
        stmt = update(UploadMono). \
            where(UploadMono.__table__.c.VendCntrNum.is_(None)). \
            values(VendCntrNum=cep_cntr.Vend_Cntr_Num)
        mysql_engine.execute(stmt)

        # noinspection PyPep8
        stmt = UploadMono.__table__.update().where(
            UploadMono.__table__.c.ExpDate.is_(None)
        ).values({'ExpDate': self.cep_cntr_match.get("Expiration_Date")})
        mysql_engine.execute(stmt)

    @debug(lvl=logging.DEBUG, prefix='')
    def remove_cep_cntr_info(self):
        stmt = update(UploadMono). \
            values(CEPCntrNum=None,
                   Vendor_ID=None,
                   VendCntrNum=None)
        mysql_engine.execute(stmt)

        stmt = UploadMono.__table__.update().where(
            UploadMono.__table__.c.ExpDate == self.cep_cntr_match.get("Expiration_Date")
        ).values({'ExpDate': None})
        mysql_engine.execute(stmt)

    @debug(lvl=logging.DEBUG, prefix='')
    def populate_prod_sel_tbl(self):
        mysql_session_maker.close_all()
        self.session = mysql_session_maker()
        self.table_create_if_not_exists("pythontest", "cntr_prodmatching", "ProductMatching")
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping

        query_1 = self.session.query(
            UploadMono.__table__.c.Vendor_ID,
            UploadMono.__table__.c.VendProdNum,
            UploadMono.__table__.c.CustProdNum,
            ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num
        ).outerjoin(ARW_PRF_Mapping.prod_vend_01_current.__table__,
                    and_(
                        UploadMono.__table__.c.Vendor_ID ==
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num,
                        UploadMono.__table__.c.VendProdNum ==
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Part_Num)). \
            distinct(UploadMono.__table__.c.VendProdNum)

        insert = ProductMatching.__table__.insert().from_select(
            [ProductMatching.__table__.c.Vendor_ID,
             ProductMatching.__table__.c.VendProdNum,
             ProductMatching.__table__.c.CustProdNum,
             ProductMatching.__table__.c.CEP_Part_Num],
            query_1
        )

        mysql_engine.execute(insert)
        self.session.commit()

        query_2 = self.session.query(ProductMatching).all()

        for row in query_2:
            update_stmt = update(ProductMatching). \
                where(ProductMatching.__table__.c.VendProdNum == row.VendProdNum). \
                values(Count=self.session.query(func.count(ProductMatching.__table__.c.VendProdNum))
                       .filter(ProductMatching.__table__.c.VendProdNum == row.VendProdNum).scalar()
                       )
            mysql_engine.execute(update_stmt)

    # # noinspection PyPep8
    # @debug(lvl=logging.DEBUG, prefix='')
    # def supply_missing_exp_date(self):
    #     stmt = UploadMono.__table__.update().where(
    #         UploadMono.__table__.c.ExpDate.is_(None)
    #     ).values({'ExpDate': self.cep_cntr_match.get("Expiration_Date")})
    #     mysql_engine.execute(stmt)

    # noinspection PyProtectedMember
    @debug(lvl=logging.DEBUG, prefix='')
    def save_csv_export(self):
        period_qry = self.session.query(UploadMatched.__table__.c.Period).distinct()
        for period in period_qry:
            print("Period: {0}".format(period.Period))
            filename = self.upload_filename.replace("\\", "/") + "_Period-{period}.csv".format(period=period.Period)
            csv_results = self.fetch_csv_results(period.Period)
            hdr_lst = []
            for _ in csv_results.column_descriptions:
                hdrs = _.get('name').replace(" ", "_").replace("'", "").replace('"', "")
                hdr_lst.append(hdrs)

            with open(filename, mode='w', newline="") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(hdr_lst)
                for row in csv_results.all():
                    write_list = []
                    for hdr, value in row._asdict().items():
                        print(hdr, value)
                        if hdr in ("Eff_Date", "Exp_Date"):
                            # TODO: Address  eff_date and/or exp_date are not date/time, but just date
                            write_list.append(value.strftime('%m/%d/%Y'))
                        else:
                            write_list.append(value)

                    csv_writer.writerow(write_list)


class UploadMapping(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 mapping_id,
                 datatype,
                 label,
                 col_obj,
                 ws_col_obj=None,
                 static_value=None
                 ):
        self.mapping_id = mapping_id
        self.datatype = datatype
        self.label = label
        self.col_obj = col_obj
        self.ws_col_obj = ws_col_obj
        self.static_value = static_value
