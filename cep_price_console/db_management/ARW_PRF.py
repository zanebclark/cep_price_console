from cep_price_console.utils.utils import is_path_exists_or_creatable, creation_date
from cep_price_console.db_management.server_utils import mysql_login_required
from cep_price_console.utils.log_utils import debug, CustomAdapter
from cep_price_console.utils.excel_utils import Workbook
import cep_price_console.db_management.server_utils as server_utils
from cep_price_console.utils import config
from sqlalchemy.schema import CreateSchema
from sqlalchemy.sql import text
# from sqlalchemy.ext.declarative import DeferredReflection
# noinspection PyUnresolvedReferences
from sqlalchemy import exc, and_, select, or_, func
import importlib
import logging
import datetime
import os
import csv
import textwrap


reflected = False
creation_module = None


@debug(lvl=logging.DEBUG, prefix='')
def get_creation_module():
    global creation_module
    if creation_module is None:
        for table in list(server_utils.mysql_base.metadata.tables.keys()):
            server_utils.mysql_base.metadata.remove(server_utils.mysql_base.metadata.tables[table])
        creation_module = importlib.import_module("cep_price_console.db_management.ARW_PRF_Creation")
        return creation_module
    else:
        return creation_module


class ArwPrfImporter(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    @mysql_login_required
    def __init__(self, relative_filename):
        self.relative_filename = relative_filename
        self.wb_cls = Workbook(relative_filename)
        self.session = server_utils.mysql_session_maker()

    @debug(lvl=logging.DEBUG)
    def investigate_arw_prf_xl(self):
        for sheet_name in self.wb_cls.ws_lst:
            prf_obj = self.ws_format_check(sheet_name)
            if prf_obj is not None:
                self.field_instantiation(prf_obj)
            self.wb_cls.wb.unload_sheet(sheet_name)

    @debug(lvl=logging.DEBUG)
    def ws_format_check(self, sheet_name):
        # PrimaryReportFile.clear_dict()
        formatting_error = False
        tbl_init_dict = {}
        self.wb_cls.ws_sel = sheet_name
        for col in range(1, self.wb_cls.col_count + 1):
            col_dict = dict(
                arw_or_static=None,
                table_name=None,
                filepath_or_master_table_name=None,
            )
            #  Table-Level loop
            #  Row 1 in every spreadsheet should have Y/N values signifying that the column
            #       be considered for table import. Import only the columns w/ Y values.
            for row in range(1, 4):
                cell_val = self.wb_cls.fetch_value(row, col).formatted_value
                try:
                    cell_val = str(cell_val).strip()
                except ValueError:
                    ArwPrfImporter.logger.error("Sheet Name: {0}, Column: {1}, Row: {2}, Value not a string: {3}"
                                                .format(sheet_name, col, str(row), cell_val))
                else:
                    if row == 1:
                        if cell_val in ('Y', 'S', 'N', 'MySQL File?'):
                            col_dict['arw_or_static'] = cell_val
                        else:
                            formatting_error = True
                            ArwPrfImporter.logger.error("Sheet Name: {0}, Column: {1}, Row: {2}, First row value not "
                                                        "'Y', 'S', 'N' or 'MySQL File?': {3}".format(sheet_name, col,
                                                                                                     row, cell_val))
                            break
                    elif row == 2:
                        if self.wb_cls.fetch_value(1, col).formatted_value != 'S':
                            if cell_val.strip() != "N/A":
                                if cell_val[-4:].upper() == ".CSV":
                                    fileroot = config.config["directory"]["arw_export_dir"]
                                    filepath = os.path.join(fileroot, cell_val)

                                    ArwPrfImporter.logger.log(logging.DEBUG, "filepath: {0}".format(filepath))

                                    if not is_path_exists_or_creatable(filepath):
                                        formatting_error = True
                                        ArwPrfImporter.logger.error("Sheet Name: {0}, Column: {1}, Row: {2}, Invalid "
                                                                    "filepath: {3}".format(sheet_name, col, row,
                                                                                           cell_val))
                                        break
                                    else:
                                        col_dict['filepath_or_master_table_name'] = filepath
                                else:
                                    formatting_error = True
                                    ArwPrfImporter.logger.error("Sheet Name: {0}, Column: {1}, Row: {2}, "
                                                                "Second row value must be a filepath or "
                                                                "'N/A': {3}".format(sheet_name, col, row, cell_val))
                                    break
                            elif cell_val.strip() == "N/A":
                                col_dict['filepath_or_master_table_name'] = cell_val
                        elif self.wb_cls.fetch_value(1, col).formatted_value == 'S':
                            col_dict['filepath_or_master_table_name'] = cell_val
                    elif row == 3:
                        # table_name = None
                        ArwPrfImporter.logger.log(logging.NOTSET,
                                                  "Sheet Name: {0}, Column: {1}, Row: {2}, "
                                                  "ARW Column List: {3}, Cell Value: {4}"
                                                  .format(sheet_name, col, row, arw_col_list.get(str(col)), cell_val))
                        if col <= 22:
                            if arw_col_list.get(str(col)) != cell_val:
                                formatting_error = True
                                ArwPrfImporter.logger.error("Sheet Name: {0}, Column: {1}, Row: {2}, Column Ordering "
                                                            "Error: {3}".format(sheet_name, col, row, cell_val))
                                break
                            elif arw_col_list.get(str(col)) == cell_val:
                                col_dict['table_name'] = cell_val
                        else:
                            col_dict['table_name'] = cell_val
            if formatting_error:
                break
            # ArwPrfImporter.logger.log(logging.NOTSET, "Sheet Name: {0}, Column: {1}".format(sheet_name, col))
            # for str_key in col_dict.keys():
            #     str_value = col_dict.get(str_key)
            #     ArwPrfImporter.logger.log(logging.DEBUG, "Key: {0}, Value: {1}".format(str_key, str_value))

            if col > 22:
                tbl_init_dict[str(col)] = col_dict

        if not formatting_error:
            prf_obj = PrimaryReportFile(self.session, sheet_name)

            for col_key in sorted(tbl_init_dict.keys(), key=lambda x: int(x)):
                col_value = tbl_init_dict.get(col_key)
                ArwPrfImporter.logger.log(logging.NOTSET, "Key: {0}, Value: {1}".format(col_key, col_value.values()))

            prf_obj.tbl_init_dict = tbl_init_dict
            self.table_instantiation(prf_obj)
            return prf_obj

        else:
            return None
        # self.wb_cls.wb.unload_sheet(sheet_name)

    @debug(lvl=logging.DEBUG)
    def table_instantiation(self, prf_obj):
        for col in sorted(prf_obj.tbl_init_dict.keys(), key=lambda x: int(x)):
            col_dict = prf_obj.tbl_init_dict.get(col)
            if col_dict.get('arw_or_static') == 'Y':
                current_table = CurrentTable(
                    session=self.session,
                    prf_name=prf_obj.filename,
                    prf_col=int(col),
                    base_table_name=col_dict.get('table_name'),
                    table_name=col_dict.get('table_name') + "_01_current",
                    filepath=col_dict.get('filepath_or_master_table_name'))
                prf_obj.current_tbl_dict[col] = current_table

                archive_table = ArchiveTable(
                    session=self.session,
                    prf_name=prf_obj.filename,
                    prf_col=int(col),
                    base_table_name=col_dict.get('table_name'),
                    table_name=col_dict.get('table_name') + "_02_archive",
                    filepath=col_dict.get('filepath_or_master_table_name'))
                prf_obj.archive_tbl_dict[col] = archive_table
            elif col_dict.get('arw_or_static') == 'S':
                static_table = StaticTable(
                    session=self.session,
                    prf_name=prf_obj.filename,
                    prf_col=int(col),
                    base_table_name=col_dict.get('table_name'),
                    table_name=col_dict.get('table_name') + "_01_static",
                    master_table_name=col_dict.get('filepath_or_master_table_name'))
                prf_obj.static_tbl_dict[col] = static_table

    @debug(lvl=logging.DEBUG)
    def field_instantiation(self, prf_obj):
        self.wb_cls.ws_sel = prf_obj.sheetname
        col_num_list = list(prf_obj.current_tbl_dict.keys()) + list(prf_obj.archive_tbl_dict.keys()) + list(
            prf_obj.static_tbl_dict.keys())
        col_num_list = [int(x) for x in list(set(col_num_list))]
        # print(col_num_list)

        for row in range(4, self.wb_cls.row_count + 1):
            try:
                new_field = Field(
                    arw_name=self.wb_cls.fetch_value(row, "A").formatted_value,
                    logical_field=self.wb_cls.fetch_value(row, "B").formatted_value,
                    tag=self.wb_cls.fetch_value(row, "C").formatted_value,
                    length=self.wb_cls.fetch_value(row, "D").formatted_value,
                    nested=self.wb_cls.fetch_value(row, "E").formatted_value,
                    desc=self.wb_cls.fetch_value(row, "F").formatted_value,
                    column_name=self.wb_cls.fetch_value(row, "H").formatted_value,
                    data_type=self.wb_cls.fetch_value(row, "I").formatted_value,
                    fill=self.wb_cls.fetch_value(row, "J").formatted_value,
                    primary_key=self.wb_cls.fetch_value(row, "K").formatted_value,
                    nullable=self.wb_cls.fetch_value(row, "L").formatted_value,
                    unique=self.wb_cls.fetch_value(row, "M").formatted_value,
                    index=self.wb_cls.fetch_value(row, "N").formatted_value,
                    binary_col=self.wb_cls.fetch_value(row, "O").formatted_value,
                    auto_incremental=self.wb_cls.fetch_value(row, "P").formatted_value,
                    generated=self.wb_cls.fetch_value(row, "Q").formatted_value,
                    static_key=self.wb_cls.fetch_value(row, "R").formatted_value,
                    dflt_exp=self.wb_cls.fetch_value(row, "U").raw_raw_val,
                    notes=self.wb_cls.fetch_value(row, "A").formatted_value,
                )
            except ValueError as err:
                if not err.args:
                    err.args = ('',)
                err.args = ("Sheet Name: {0}, Row: {1}"
                            .format(prf_obj.sheetname,
                                    row),
                            ) + err.args
                ArwPrfImporter.logger.error(err.args)
            else:
                for col in sorted(col_num_list):
                    try:
                        order = int(self.wb_cls.fetch_value(row, col).formatted_value)
                    except ValueError:
                        ArwPrfImporter.logger.log(
                            logging.DEBUG, "Value is not an integer. Field not appended to any dictionary.")
                    else:
                        current_tbl_obj = prf_obj.current_tbl_dict.get(str(col))
                        if current_tbl_obj is not None:
                            ArwPrfImporter.logger.log(
                                logging.DEBUG,
                                "Column: {0}, Table: {1}, Value is an integer. Field appended to dictionary.".format(
                                    col, current_tbl_obj.table_name))
                            current_tbl_obj.fields[str(order)] = new_field
                        else:
                            ArwPrfImporter.logger.log(
                                logging.DEBUG,
                                "Column: {0}. Current Table Dictionary. Get returned 'None'".format(col))

                        archive_tbl_obj = prf_obj.archive_tbl_dict.get(str(col))
                        if archive_tbl_obj is not None:
                            ArwPrfImporter.logger.log(
                                logging.DEBUG,
                                "Column: {0}, Table: {1}, Value is an integer. Field appended to dictionary.".format(
                                    col, archive_tbl_obj.table_name))
                            archive_tbl_obj.fields[str(order)] = new_field
                        else:
                            ArwPrfImporter.logger.log(
                                logging.DEBUG,
                                "Column: {0}. Archive Table Dictionary. Get returned 'None'".format(col))

                        static_tbl_obj = prf_obj.static_tbl_dict.get(str(col))
                        if static_tbl_obj is not None:
                            ArwPrfImporter.logger.log(
                                logging.DEBUG,
                                "Column: {0}, Table: {1}, Value is an integer. Field appended to dictionary.".format(
                                    col, static_tbl_obj.table_name))
                            static_tbl_obj.fields[str(order)] = new_field
                        else:
                            ArwPrfImporter.logger.log(
                                logging.DEBUG,
                                "Row: {1}, Column: {0}. Static Table Dictionary. Get returned 'None'".format(col, row))
        tbl_obj_lst = \
            list(prf_obj.current_tbl_dict.values()) + \
            list(prf_obj.archive_tbl_dict.values()) + \
            list(prf_obj.static_tbl_dict.values())
        for tbl_obj in tbl_obj_lst:
            tbl_obj.post_field_instantiation()
        # self.wb_cls.wb.unload_sheet(prf_obj.sheetname)

    @debug(lvl=logging.DEBUG)
    def write_module_file(self, creation=False, mapping=False):
        if bool(PrimaryReportFile.prf_dict.values()):
            filename = None
            if sum([creation, mapping]) != 1:
                raise ValueError
            elif creation:
                filename = config.SOURCE_PATH / "cep_price_console" / "db_management" / "ARW_PRF_Creation.py"
                with filename.open("w") as module_file:
                    print("from sqlalchemy.ext.declarative import DeferredReflection", file=module_file)
                    print("from sqlalchemy import Column, Table, func", file=module_file)
                    print("from sqlalchemy.sql import case, and_, or_, literal", file=module_file)
                    print("from sqlalchemy.ext.hybrid import hybrid_property", file=module_file)
                    print("from sqlalchemy.types import Date, DateTime, Integer, Numeric, String, Time",
                          file=module_file)
                    print("from sqlalchemy.dialects.mysql import LONGTEXT", file=module_file)
                    print("import cep_price_console.db_management.server_utils as server_utils\n\n", file=module_file)
            elif mapping:
                filename = config.SOURCE_PATH / "cep_price_console" / "db_management" / "ARW_PRF_Mapping.py"
                with filename.open("w") as module_file:
                    print("from sqlalchemy.ext.declarative import DeferredReflection", file=module_file)
                    print("from sqlalchemy import Table, func", file=module_file)
                    print("from sqlalchemy.sql import case, and_, or_, literal", file=module_file)
                    print("from sqlalchemy.ext.hybrid import hybrid_property", file=module_file)
                    print("import cep_price_console.db_management.server_utils as server_utils\n\n", file=module_file)
            with filename.open("a") as module_file:
                filename_statement = "Workbook Filename: {0}\n".format(self.wb_cls.xl_fullpath_pretty)
                max_length = 110
                fmt_string = "# " + "\n# ".join([filename_statement[i:i + max_length] for i in
                                                 range(0, len(filename_statement), max_length)])
                print(fmt_string, file=module_file)
                print("# Timestamp: {0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                      file=module_file)
                print("\n", file=module_file)
                print("class InformReflection(DeferredReflection, server_utils.mysql_base):", file=module_file)
                print("    __abstract__ = True\n\n", file=module_file)

                for prf_obj in PrimaryReportFile.prf_dict.values():
                    ArwPrfImporter.logger.log(logging.NOTSET, "Primary Report File: {0}".
                                              format(prf_obj.sheetname))
                    tbl_obj_lst = \
                        list(prf_obj.current_tbl_dict.values()) + \
                        list(prf_obj.archive_tbl_dict.values()) + \
                        list(prf_obj.static_tbl_dict.values())
                    for tbl_obj in sorted(tbl_obj_lst, key=lambda x: x.table_name):
                        ArwPrfImporter.logger.log(logging.NOTSET, "Tablename: {0}".format(tbl_obj.table_name))
                        if creation:
                            print(tbl_obj.creation_stmt, file=module_file)
                        elif mapping:
                            print(tbl_obj.mapping_stmt, file=module_file)
        elif not bool(PrimaryReportFile.prf_dict.values()):
            ArwPrfImporter.logger.error("Primary Report File list empty.")
            self.investigate_arw_prf_xl()
            self.write_module_file(creation, mapping)

    @debug(lvl=logging.DEBUG)
    def create_schemas(self):
        for prf_obj in PrimaryReportFile.prf_dict.values():
            prf_obj.create_if_not_exists()

    @debug(lvl=logging.DEBUG)
    def drop_and_create_all_tables(self):
        for prf_obj in PrimaryReportFile.prf_dict.values():
            prf_obj.drop_and_create_tables()

    @debug(lvl=logging.DEBUG)
    def scheduled_script(self):
        if hasattr(self, 'session'):
            if bool(PrimaryReportFile.prf_dict.values()):
                for prf_obj in PrimaryReportFile.prf_dict.values():
                    prf_obj.update_schema()
                schema_create_if_not_exists('pythontest')
                self.fill_prod_uom()
            elif not bool(PrimaryReportFile.prf_dict.values()):
                ArwPrfImporter.logger.error("Primary Report File list empty.")
                self.investigate_arw_prf_xl()
                self.scheduled_script()

    @debug(lvl=logging.DEBUG, prefix='')
    def fill_prod_uom(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        base_uom_update = ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.update().where(
            ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.UOM_Factor_Desc == "1"
        ).values(
            Base_UOM_Factor=ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.UOM,
            Base_UOM_Qty=1
        )
        server_utils.mysql_engine.execute(base_uom_update)
        self.session.commit()

        # noinspection PyPep8,PyComparisonWithNone
        no_base_uom = self.session.query(ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.ID).filter(
            and_(ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Factor.is_(None),
                 ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Qty.is_(None)))

        while no_base_uom.count() > 0:
            # noinspection PyPep8,PyComparisonWithNone
            has_base_uom = \
                select([ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Prod_Num,
                        ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.UOM,
                        ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.UOM_Qty,
                        ARW_PRF_Mapping.prod_uom_v2_01_current.Of_UOM,
                        ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Factor,
                        ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Qty,
                        ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.UOM_Factor_Desc]) \
                    .where(and_(
                    ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Factor.isnot(None),
                    ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Qty.isnot(None))) \
                    .distinct() \
                    .alias("has_base_uom")

            # for _ in server_utils.mysql_engine.execute(has_base_uom):
            #     ArwPrfImporter.logger.log(logging.DEBUG, _)
            # noinspection PyPep8,PyComparisonWithNone
            update_next_uom_level = ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.update().where(and_(
                or_(
                    and_(
                        ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Prod_Num.is_(None),
                        has_base_uom.c.Prod_Num.is_(None)),
                    ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Prod_Num == has_base_uom.c.Prod_Num),
                or_(
                    and_(
                        ARW_PRF_Mapping.prod_uom_v2_01_current.Of_UOM.is_(None),
                        has_base_uom.c.UOM.is_(None)),
                    ARW_PRF_Mapping.prod_uom_v2_01_current.Of_UOM == has_base_uom.c.UOM),
                and_(ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Factor.is_(None),
                     ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.Base_UOM_Qty.is_(None)))) \
                .values(Base_UOM_Factor=has_base_uom.c.Base_UOM_Factor,
                        Base_UOM_Qty=(has_base_uom.c.Base_UOM_Qty *
                                      ARW_PRF_Mapping.prod_uom_v2_01_current.__table__.c.UOM_Qty))

            server_utils.mysql_engine.execute(update_next_uom_level)
            self.session.commit()

    @debug(lvl=logging.DEBUG, prefix='')
    def recreate(self):
        if hasattr(self, 'session'):
            self.write_module_file(creation=True)
            get_creation_module()
            self.create_schemas()
            self.drop_and_create_all_tables()
            self.write_mapping()

    @debug(lvl=logging.DEBUG, prefix='')
    def write_mapping(self):
        if hasattr(self, 'session'):
            self.write_module_file(mapping=True)
            self.scheduled_script()


arw_col_list = {
    "1": "Name",
    "2": "Logical Field",
    "3": "Tag",
    "4": "Length",
    "5": "Nested",
    "6": "Description",
    "7": "|",
    "8": "Column Name",
    "9": "Datatype",
    "10": "Fill",
    "11": "PK",
    "12": "Nullable",
    "13": "UQ",
    "14": "IND",
    "15": "B",
    "16": "AI",
    "17": "G",
    "18": "SK",
    "19": "Mapping",
    "20": "Static Name",
    "21": "Default/ Expression",
    "22": "Notes"
}


class PrimaryReportFile(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    prf_dict = {}

    @debug(lvl=logging.DEBUG, prefix='Primary Report File Initiated')
    def __init__(self,
                 session,
                 filename):
        self.session = session
        self.filename = filename.lower()
        self.sheetname = filename
        self.tbl_init_dict = {}
        self.current_tbl_dict = {}
        self.archive_tbl_dict = {}
        self.static_tbl_dict = {}
        PrimaryReportFile.prf_dict[self.sheetname] = self

    # @classmethod
    # def clear_dict(cls):
    #     cls.prf_dict = {}

    @debug(lvl=logging.DEBUG, prefix='')
    def exists(self):
        try:
            server_utils.mysql_engine.execute("SHOW CREATE SCHEMA `{0}`;".format(self.filename)).scalar()
            PrimaryReportFile.logger.log(logging.NOTSET, "Schema Exists: {0}".format(self.filename))
            return True
        except exc.DBAPIError:
            PrimaryReportFile.logger.log(logging.NOTSET, "Schema Does Not Exist: {0}".format(self.filename))
            return False

    @debug(lvl=logging.DEBUG, prefix='')
    def create(self):
        PrimaryReportFile.logger.log(logging.NOTSET, "Creating Schema: {0}".format(self.filename))
        server_utils.mysql_engine.execute(CreateSchema(self.filename))

    @debug(lvl=logging.DEBUG, prefix='')
    def create_if_not_exists(self):
        if not self.exists():
            self.create()

    @debug(lvl=logging.DEBUG, prefix='')
    def drop_and_create_tables(self):
        tbl_lst = \
            list(self.current_tbl_dict.values()) + \
            list(self.archive_tbl_dict.values()) + \
            list(self.static_tbl_dict.values())
        for tbl_obj in tbl_lst:
            tbl_obj.drop_and_create_if_not_exists()
        # ARW_PRF_Mapping.InformReflection.prepare(server_utils.mysql_engine)

    @debug(lvl=logging.DEBUG, prefix='')
    def update_schema(self):
        for current_tbl_obj in self.current_tbl_dict.values():
            self.session.commit()
            current_tbl_obj.truncate()
            current_tbl_obj.append()
        for archive_tbl_obj in self.archive_tbl_dict.values():
            create_date = datetime.datetime.strptime(creation_date(archive_tbl_obj.filepath), "%Y-%m-%d %H:%M:%S")
            max_date_time = archive_tbl_obj.max_date_time()
            if create_date != max_date_time:
                archive_tbl_obj.append()
            archive_tbl_obj.delete_sub_max_date_time()
        # for static_tbl_obj in self.static_tbl_dict.values():
        #     pass
        # append static


class Field(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    type_list = (
        "BigInteger",
        "Boolean",
        "Date",
        "DateTime",
        "Enum",
        "Float",
        "Integer",
        "Interval",
        "LargeBinary",
        "MatchType",
        "Numeric",
        "PickleType",
        "SchemaType",
        "SmallInteger",
        "String",
        "Text",
        "Time",
        "Unicode",
        "UnicodeText",
        "LONGTEXT"
    )

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self,
                 arw_name="",
                 logical_field="",
                 tag="",
                 length="",
                 nested="",
                 desc="",
                 column_name="",
                 data_type="N/A",
                 primary_key="",
                 nullable="",
                 unique="",
                 index="",
                 binary_col="",
                 fill="",
                 auto_incremental="",
                 dflt_exp="",  # Don't need it
                 generated="",  # Don't need it
                 static_key="",  # Don't need it
                 default="",  # Don't need it
                 notes=""):
        self.arw_name = arw_name  # ARW Name with spaces and such (Column A)
        self.logical_field = logical_field  # If this is true, don't look for this value in the .csv file (Column B)
        self.tag = tag  # ARW Tag (Column C)
        self.length = length  # ARW Length (Not the length associated with datatype) (Column D)
        self.nested = nested  # ARW value (Column E)
        self.desc = desc  # ARW Description of field (Column F)
        # None of the above fields influence the field's status in the DB

        self.column_name = column_name  # My assigned name without spaces (check that this is true in setter)(Column H)
        self.data_type = data_type  # SQL Datatype (convert to SQL Alchemy Datatype) (Column I)
        self.primary_key = primary_key  # Is this a primary key? (Column K)
        self.nullable = nullable  # Is this a NotNull field? (Column L)
        self.unique = unique  # Is this a Unique Index? (Column M)
        self.index = index  # Is this an Index? (Column N)
        self.binary_col = binary_col  # Is this a Binary Column? (Column O)
        self.fill = fill  # Datatype length (Column J)
        self.auto_incremental = auto_incremental  # Is this field Auto-Incremental? (Column R)
        self.generated = generated  # Is this field generated? (Column S)
        self.static_key = static_key  # Is this field a static key? (Column T)
        self.default = default  # Don't really know
        self.dflt_exp = dflt_exp  # What is the default expression for this field? (Only used if generated) (Column W)
        self.notes = notes  # Don't really know (Column X)
        self.get_create_field()

    # region arw_name  ##########################################################################################s######
    @property
    @debug(lvl=logging.NOTSET)
    def arw_name(self):
        return self._arw_name

    @arw_name.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def arw_name(self, value):
        try:
            str_val = str(value)
            self._arw_name = str_val.strip()
        except ValueError:
            raise ValueError("{0}: Value cannot be converted to string: {1}".format("arw_name", value))

    # endregion ########################################################################################################

    # region logical_field  ############################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def logical_field(self):
        return self._logical_field

    @logical_field.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def logical_field(self, value):
        try:
            str_val = str(value).upper().strip()
            if str_val in ("Y", "N"):
                self._logical_field = str_val.strip()
            else:
                raise ValueError("{0}.{1}: Value must be 'Y' or 'N': {2}".
                                 format(self.arw_name, "logical_field", value))
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                             format(self.arw_name, "logical_field", value))

    # endregion ########################################################################################################

    # region tag  ######################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def tag(self):
        return self._tag

    @tag.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def tag(self, value):
        try:
            str_val = str(value)
            self._tag = str_val.strip()
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                             format(self.arw_name, "tag", value))

    # endregion ########################################################################################################

    # region length  ###################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def length(self):
        return self._length

    @length.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def length(self, value):
        try:
            int_val = int(value)
            self._length = int_val
        except ValueError:
            try:
                str_val = str(value)
                if str_val.upper().strip() == "N/A":
                    self._length = None
                else:
                    raise ValueError("{0}.{1}: Value is not 'N/A': {2}".format(self.arw_name, "length", value))
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to an integer: {2}"
                                 .format(self.arw_name, "length", value))

    # endregion ########################################################################################################

    # region nested  ###################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def nested(self):
        return self._nested

    @nested.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def nested(self, value):
        try:
            str_val = str(value)
            self._nested = str_val.strip()
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".format(self.arw_name, "nested", value))

    # endregion ########################################################################################################

    # region desc  #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def desc(self):
        return self._desc

    @desc.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def desc(self, value):
        try:
            str_val = str(value).replace("'", '"').strip()
            str_val = ' '.join(str_val.splitlines())
            str_val.strip()
            self._desc = str_val
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}"
                             .format(self.arw_name, "desc", value))

    # endregion ########################################################################################################

    # region column_name  ##############################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def column_name(self):
        return self._column_name

    @column_name.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def column_name(self, value):
        try:
            str_val = str(value).strip()
            if len(str_val) > 64:
                raise Exception("{0}.{1}: String length greater than the 64 character limit: {2}"
                                .format(self.arw_name, "column_name", value))
            scrubbed_val = str_val.replace("(", "").replace(")", "").replace("/", "").replace("-", "").replace("#", "")
            if str_val == scrubbed_val:
                try:
                    int(scrubbed_val[:1])
                except ValueError:
                    self._column_name = scrubbed_val
                else:
                    raise Exception("{0}.{1}: First character of value cannot be a number: {2}"
                                    .format(self.arw_name, "column_name", value))
            else:
                raise Exception("{0}.{1}: Value has one of the following illegal characters: {{(, ), /, -, #}}: {2}"
                                .format(self.arw_name, "column_name", value))
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}"
                             .format(self.arw_name, "column_name", value))

    # endregion ########################################################################################################

    # region data_type  ################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def data_type(self):
        return self._data_type

    @data_type.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def data_type(self, value):
        try:
            str_val = str(value)
            if str_val.strip() in Field.type_list:
                self._data_type = str_val.strip()
            else:
                raise ValueError("{0}.{1}: Value not in datatype list: {2}"
                                 .format(self.arw_name, "data_type", value))
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}"
                             .format(self.arw_name, "data_type", value))

    # endregion ########################################################################################################

    # region fill  #####################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def fill(self):
        return self._fill

    @fill.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def fill(self, value):
        if self.data_type in (
                "BigInteger",
                "Boolean",
                "Date",
                "DateTime",
                "Integer",
                "SmallInteger",
                "Time",
                "Text",
                "LONGTEXT"
        ):
            if value not in ("", None):
                raise ValueError("{0}.{1}: Datatype does not allow for a fill: {2}"
                                 .format(self.arw_name, "fill", self.data_type))
            else:
                self._fill = None
        elif self.data_type in (
                "LargeBinary",
                "String",
                # "Text",
                "Unicode",
                "UnicodeText",
                "Float"
        ):
            if value in ("", None):
                raise ValueError("{0}.{1}: Datatype requires a fill: {2}"
                                 .format(self.arw_name, "fill", self.data_type))
            else:
                try:
                    int_val = int(value)
                    if self.data_type == "String" and self.binary_col:
                        self._fill = "length={0}, collation='binary'".format(str(int_val))
                    else:
                        self._fill = "length={0}".format(str(int_val))
                except ValueError:
                    raise ValueError("{0}.{1}: Value cannot be converted to an integer: {2}"
                                     .format(self.arw_name, "fill", value))
        elif self.data_type == "Float":
            try:
                int_val = int(value)
                self._fill = "precision={0}".format(str(int_val))
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to an integer: {2}"
                                 .format(self.arw_name, "fill", value))
        elif self.data_type == "Numeric":
            try:
                str_val = str(value).strip()
                pre_str, scale_str = str_val.split(",")
                try:
                    pre_int = int(pre_str.strip())
                    scale_int = int(scale_str.strip())
                    self._fill = "precision={0}, scale={1}".format(str(pre_int), str(scale_int))
                except ValueError:
                    raise ValueError("{0}.{1}: Error with precision or scale integer conversion: "
                                     "precision={2}, scale={3}".
                                     format(self.arw_name, "fill", pre_str, scale_str))
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "fill", value))
        elif self.data_type in (
                "Enum",
                "Interval",
                "MatchType",
                "PickleType",
                "SchemaType"
        ):
            raise ValueError("{0}.{1}: What the fuck are you doing using this datatype?: {2}"
                             .format(self.arw_name, "fill", self.data_type))

    # endregion ########################################################################################################

    # region primary_key  ##############################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def primary_key(self):
        return self._primary_key

    @primary_key.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def primary_key(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "primary_key", value))
        if str_val.strip().upper() == "X":
            self._primary_key = True
        elif str_val.strip().upper() == "":
            self._primary_key = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "primary_key", value))

    # endregion ########################################################################################################

    # region nullable  #################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def nullable(self):
        return self._nullable

    @nullable.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def nullable(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "nullable", value))
        if str_val.strip().upper() == "X":
            if not self.primary_key:
                self._nullable = True
            else:
                raise ValueError("{0}.{1}: Primary key cannot be nullable: {2}".
                                 format(self.arw_name, "nullable", value))
        elif str_val.strip().upper() == "":
            self._nullable = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "nullable", value))

    # endregion ########################################################################################################

    # region unique  ###################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def unique(self):
        return self._unique

    @unique.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def unique(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "unique", value))
        if str_val.strip().upper() == "X":
            self._unique = True
        elif str_val.strip().upper() == "":
            self._unique = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "unique", value))

    # endregion ########################################################################################################

    # region index  ####################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def index(self):
        return self._index

    @index.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def index(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "index", value))
        if str_val.strip().upper() == "X":
            self._index = True
        elif str_val.strip().upper() == "":
            self._index = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "index", value))

    # endregion ########################################################################################################

    # region binary_col  ###############################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def binary_col(self):
        return self._binary_col

    @binary_col.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def binary_col(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "binary_col", value))
        if str_val.strip().upper() == "X":
            if self.data_type in ("String", "Text"):
                self._binary_col = True
            else:
                raise ValueError("{0}.{1}: Only string and text datatypes can be binary: {2}".
                                 format(self.arw_name, "binary_col", self.data_type))
        elif str_val.strip().upper() == "":
            self._binary_col = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "binary_col", value))

    # endregion ########################################################################################################

    # region auto_incremental  #########################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def auto_incremental(self):
        return self._auto_incremental

    @auto_incremental.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def auto_incremental(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "auto_incremental", value))
        if str_val.strip().upper() == "X":
            if self.index and self.data_type in (
                    "BigInteger",
                    "Boolean",
                    "Float",
                    "Integer",
                    "Numeric",
                    "SmallInteger"):
                self._auto_incremental = True
            else:
                raise ValueError("{0}.{1}: Autoincremented columns must be indexed and numeric.".
                                 format(self.arw_name, "auto_incremental"))
        elif str_val.strip().upper() == "":
            self._auto_incremental = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "auto_incremental", value))

    # endregion ########################################################################################################

    # region generated  ################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def generated(self):
        return self._generated

    @generated.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def generated(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "generated", value))
        if str_val.strip().upper() == "X":
            if not self.auto_incremental:
                self._generated = True
            else:
                raise ValueError("{0}.{1}: Value cannot be generated and autoincremented: {2}".
                                 format(self.arw_name, "generated", value))
        elif str_val.strip().upper() == "":
            self._generated = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "generated", value))

    # endregion ########################################################################################################

    # region static_key  ###############################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def static_key(self):
        return self._static_key

    @static_key.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def static_key(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "static_key", value))
        if str_val.strip().upper() == "X":
            self._static_key = True
        elif str_val.strip().upper() == "":
            self._static_key = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "static_key", value))

    # endregion ########################################################################################################

    # region default  ##################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def default(self):
        return self._default

    @default.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def default(self, value):
        if value is None:
            str_val = ""
        else:
            try:
                str_val = str(value)
            except ValueError:
                raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                                 format(self.arw_name, "default", value))
        if str_val.strip().upper() == "X":
            self._default = True
        elif str_val.strip().upper() == "":
            self._default = False
        else:
            raise ValueError("{0}.{1}: Value must be empty or 'X': {2}".
                             format(self.arw_name, "default", value))

    # endregion ########################################################################################################

    # region dflt_exp  #################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def dflt_exp(self):
        return self._dflt_exp

    @dflt_exp.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def dflt_exp(self, value):
        try:
            str_val = str(value)
            self._dflt_exp = str_val.strip()
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                             format(self.arw_name, "dflt_exp", value))

    # endregion ########################################################################################################

    # region notes  ####################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def notes(self):
        return self._notes

    @notes.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def notes(self, value):
        try:
            str_val = str(value)
            self._notes = str_val.strip().replace(",", '"')
        except ValueError:
            raise ValueError("{0}.{1}: Value cannot be converted to string: {2}".
                             format(self.arw_name, "notes", value))

    # endregion ########################################################################################################

    @debug(lvl=logging.NOTSET, prefix='')
    def get_create_field(self):
        code_line_list = []
        offset = len("Column(")
        code_line_list.append("Column('{column_name}',".format(column_name=self.column_name))
        if self.fill not in ("", None):
            code_line_list.append(
                offset * " " + "{data_type}({fill}),".format(data_type=self.data_type, fill=self.fill))
        else:
            code_line_list.append(offset * " " + "{data_type},".format(data_type=self.data_type))

        if self.primary_key:
            code_line_list.append(offset * " " + "primary_key=True,")
        if self.nullable:
            code_line_list.append(offset * " " + "nullable=True,")
        if self.index and self.unique:
            code_line_list.append(offset * " " + "unique=True,")
            code_line_list.append(offset * " " + "index=True,")
        else:
            if self.index and not self.unique:
                code_line_list.append(offset * " " + "index=True,")
            if self.unique and not self.index:
                code_line_list.append(offset * " " + "unique=True,")
                code_line_list.append(offset * " " + "index=True,")
        if self.auto_incremental:
            code_line_list.append(offset * " " + "autoincrement=True,")
        if self.notes not in ("", None):
            code_line_list.append(offset * " " + "doc='{notes}',".format(notes=self.notes))
        if self.desc not in ("", None):
            max_length = 79
            fmt_string = textwrap.wrap(self.desc, max_length)
            fmt_str_len = len(fmt_string)
            for count, line in enumerate(fmt_string, 1):
                if count == 1:
                    if count == fmt_str_len:
                        code_line_list.append(
                            offset * " " + "comment='{description}',".format(description=line.strip()))
                    else:
                        code_line_list.append(offset * " " + "comment='{description}'".format(description=line.strip()))
                elif count == fmt_str_len:
                    code_line_list.append(offset * " " + "        '{description}',".format(description=line.strip()))
                else:
                    code_line_list.append(offset * " " + "        '{description}'".format(description=line.strip()))
        if not self.generated:
            if self.dflt_exp not in (None, "", "None"):
                if isinstance(self.dflt_exp, str):
                    code_line_list.append(offset * " " + "default='{dflt_exp}', ".format(dflt_exp=self.dflt_exp))
                else:
                    Field.logger.log(logging.ERROR, "Figure out what to do with int/float generated columns: {0}"
                                     .format(self.arw_name))
        elif self.generated:
            if self.dflt_exp in (None, ""):
                Field.logger.log(logging.ERROR, "Generated without default expression: {0}".format(self.arw_name))
            elif self.dflt_exp not in (None, ""):
                code_line_list = []
                for line in self.dflt_exp.splitlines():
                    code_line_list.append("{0}".format(line.replace("    ", "    ")))
                Field.logger.log(logging.NOTSET, "Code:")
                for line in code_line_list:
                    Field.logger.log(logging.NOTSET, "    {code_line}".format(code_line=line))
                return code_line_list
        final_code_list = []
        code_list_len = len(code_line_list)
        for line in code_line_list[0:code_list_len - 1]:
            final_code_list.append(line)
        final_line = code_line_list[code_list_len - 1][:-1] + "),"
        final_code_list.append(code_line_list[code_list_len - 1][:-1] + "),")

        Field.logger.log(logging.NOTSET, "Code:")
        for line in final_code_list:
            Field.logger.log(logging.NOTSET, "    {code_line}".format(code_line=line))
        return final_code_list

    @debug(lvl=logging.NOTSET, prefix='')
    def convert_csv_value(self, csv_string):
        formatted_value = "Unassigned Error"
        if csv_string == '':
            formatted_value = None
            Field.logger.log(logging.NOTSET, "CSV String: {csv_string}, Formatted Value: {formatted_value}".
                             format(csv_string=csv_string, formatted_value=formatted_value))
        else:
            if self.data_type in ("Text", "String", "Unicode", "UnicodeText"):
                try:
                    formatted_value = str(csv_string)
                except ValueError:
                    formatted_value = "Error converting to string"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
            elif self.data_type in ("BigInteger", "Integer", "SmallInteger"):
                try:
                    formatted_value = int(csv_string)
                except ValueError:
                    formatted_value = "Error converting to an integer"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
            elif self.data_type in ("Numeric", "Float"):
                try:
                    formatted_value = float(csv_string)
                except ValueError:
                    formatted_value = "Error converting to a float"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
            elif self.data_type == "Boolean":
                if csv_string.strip().upper() == "FALSE":
                    formatted_value = False
                elif csv_string.strip().upper() == "TRUE":
                    formatted_value = True
                else:
                    formatted_value = "Error converting to a boolean"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
            elif self.data_type in ("LargeBinary", "Enum", "Interval", "MatchType", "PickleType", "SchemaType"):
                formatted_value = "Unmapped Datatype"
                Field.logger.log(
                    logging.ERROR,
                    "ARW Name: {arw_name}, Column Name: {column_name}, "
                    "CSV Value: {csv_string}, Datatype: {data_type}".format(
                        arw_name=self.arw_name,
                        column_name=self.column_name,
                        csv_string=csv_string,
                        data_type=self.data_type))
            elif self.data_type == "DateTime":
                try:
                    formatted_value = csv_string
                except ValueError:
                    formatted_value = "Date Conversion Error"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
            elif self.data_type == "Date":
                try:
                    formatted_value = datetime.datetime.strptime(csv_string, "%m/%d/%Y").date()
                except ValueError:
                    formatted_value = "Date Conversion Error"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
            elif self.data_type == "Time":
                try:
                    formatted_value = datetime.datetime.strptime(csv_string, "%I:%M%p").time()
                except ValueError:
                    formatted_value = "Date Conversion Error"
                    Field.logger.log(
                        logging.ERROR,
                        "ARW Name: {arw_name}, Column Name: {column_name}, "
                        "CSV Value: {csv_string}, Datatype: {data_type}".format(
                            arw_name=self.arw_name,
                            column_name=self.column_name,
                            csv_string=csv_string,
                            data_type=self.data_type))
        return formatted_value


class ConsoleTable(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='Table Initiated')
    def __init__(self,
                 session,
                 prf_name,
                 prf_col,
                 base_table_name,
                 table_name=None):
        self.session = session
        self.prf_name = prf_name
        self.prf_col = prf_col
        self.base_table_name = base_table_name
        self.table_name = table_name
        self._mapping_stmt = None
        self._creation_stmt = None

        self.fields = {}

    # region base_table_name  ##########################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def base_table_name(self):
        return self._base_table_name

    @base_table_name.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def base_table_name(self, value):
        try:
            str_value = str(value).lower()
        except ValueError:
            raise ValueError("{0}: Value cannot be converted to string: {1}".format("base_table_name", value))
        else:
            self._base_table_name = str_value

    # endregion ########################################################################################################

    # region table_name  ##########################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def table_name(self):
        return self._table_name

    @table_name.setter
    @debug(lvl=logging.NOTSET, prefix="")
    def table_name(self, value):
        try:
            str_value = str(value).lower()
        except ValueError:
            raise ValueError("{0}: Value cannot be converted to string: {1}".format("table_name", value))
        else:
            self._table_name = str_value
            self.map = None
            self.create = None

    # endregion ########################################################################################################

    # region prf_name  #################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def prf_name(self):
        return self._prf_name

    @prf_name.setter
    @debug(lvl=logging.NOTSET)
    def prf_name(self, value):
        try:
            str_value = str(value).lower()
        except ValueError:
            raise ValueError("{0}: Value cannot be converted to string: {1}".format("prf_name", value))
        else:
            self._prf_name = str_value

    # endregion ########################################################################################################

    # region mapping_stmt  ##########################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def mapping_stmt(self):
        return self._mapping_stmt

    @mapping_stmt.setter
    @debug(lvl=logging.NOTSET)
    def mapping_stmt(self, _):
        if bool(self.fields):
            gen_field_lst = []
            code = "# noinspection PyPep8Naming\n"
            code += "class {table_name}({reflection}):\n" \
                .format(table_name=self.table_name, reflection="InformReflection")
            code += " " * 4 + "__table__ = Table('{table_name}', {base_name}.metadata,\n".format(
                table_name=self.table_name,
                base_name="server_utils.mysql_base"
            )
            for field_order in sorted(self.fields.keys(), key=lambda x: int(x)):
                field_obj = self.fields.get(field_order)
                if field_obj.generated and field_obj.dflt_exp not in (None, "", "None"):
                    gen_field_lst.append(field_obj)
            code += " " * 22 + "schema='{schema_name}')\n".format(schema_name=self.prf_name)
            if bool(gen_field_lst):
                for field_obj in gen_field_lst:
                    code += "\n"
                    gen_code_lst = field_obj.get_create_field()
                    for line in gen_code_lst:
                        code += "    " + line + "\n"
            code += "\n"
            self._mapping_stmt = code
        elif not bool(self.fields):
            raise NotImplementedError

    # endregion ########################################################################################################

    # region creation_stmt  ##########################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def creation_stmt(self):
        return self._creation_stmt

    @creation_stmt.setter
    @debug(lvl=logging.NOTSET)
    def creation_stmt(self, _):
        if bool(self.fields):
            gen_field_lst = []
            offset = 22
            code = "# noinspection PyPep8Naming\n"
            code += "class {0}(server_utils.mysql_base):\n" \
                .format(self.table_name)
            code += " " * 4 + "__table__ = Table('{table_name}', {base_name}.metadata,\n".format(
                table_name=self.table_name,
                base_name="server_utils.mysql_base"
            )
            for field_order in sorted(self.fields.keys(), key=lambda x: int(x)):
                field_obj = self.fields.get(field_order)
                if field_obj.generated and field_obj.dflt_exp not in (None, "", "None"):
                    gen_field_lst.append(field_obj)
                else:
                    code_lst = field_obj.get_create_field()
                    for line in code_lst:
                        code += " " * offset + line + "\n"
            code += " " * offset + "schema='{schema_name}')\n".format(schema_name=self.prf_name)
            if bool(gen_field_lst):
                for field_obj in gen_field_lst:
                    code += "\n"
                    gen_code_lst = field_obj.get_create_field()
                    for line in gen_code_lst:
                        code += "    " + line + "\n"

            code += "\n"
            self._creation_stmt = code
        elif not bool(self.fields):
            raise NotImplementedError

    # endregion ########################################################################################################

    # noinspection PyAttributeOutsideInit
    @debug(lvl=logging.NOTSET, prefix='')
    def post_field_instantiation(self):
        self.mapping_stmt = None
        self.creation_stmt = None

    @debug(lvl=logging.DEBUG, prefix='')
    def exists(self):
        if not server_utils.mysql_engine.dialect.has_table(
                server_utils.mysql_engine,
                self.table_name,
                schema=self.prf_name):
            ConsoleTable.logger.log(
                logging.NOTSET,
                "Table does not exist: {0}.{1}".format(self.prf_name, self.table_name)
            )
            return False
        else:
            ConsoleTable.logger.log(logging.NOTSET, "Table exists: {0}.{1}".format(self.prf_name, self.table_name))
            return True

    @debug(lvl=logging.DEBUG, prefix='')
    def create_a(self):
        statement = "creation_module.{table_name}.__table__.create({engine_name})" \
            .format(table_name=self.table_name,
                    engine_name="server_utils.mysql_engine")
        ConsoleTable.logger.log(logging.NOTSET, "{schema_name}.{table_name} Create Statement: {statement}".
                                format(schema_name=self.prf_name,
                                       table_name=self.table_name,
                                       statement=statement))
        exec(statement)

    @debug(lvl=logging.DEBUG, prefix='')
    def drop(self):
        statement = "creation_module.{table_name}.__table__.drop({engine_name})" \
            .format(table_name=self.table_name,
                    engine_name="server_utils.mysql_engine")
        ConsoleTable.logger.log(logging.DEBUG, "{schema_name}.{table_name} Drop Statement: {statement}".
                                format(schema_name=self.prf_name,
                                       table_name=self.table_name,
                                       statement=statement))
        exec(statement)

    @debug(lvl=logging.DEBUG, prefix='')
    def truncate(self):
        statement = ("TRUNCATE `{schema_name}`.`{table_name}`;".format(schema_name=self.prf_name,
                                                                       table_name=self.table_name))
        ConsoleTable.logger.log(logging.NOTSET, "{schema_name}.{table_name} Truncate Statement: {statement}".
                                format(schema_name=self.prf_name,
                                       table_name=self.table_name,
                                       statement=statement))
        server_utils.mysql_engine.execute(statement)
        # statement = "creation_module.{table_name}.__table__.delete({engine_name})" \
        #     .format(table_name=self.table_name,
        #             engine_name="server_utils.mysql_engine")
        # exec(statement)

    @debug(lvl=logging.DEBUG, prefix='')
    def drop_and_create_if_not_exists(self):
        if not self.exists():
            self.create_a()
        else:
            self.drop()
            self.create_a()


class ARWTable(ConsoleTable):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='ARW Table Initiated')
    def __init__(self,
                 session,
                 prf_name,
                 prf_col,
                 base_table_name,
                 table_name,
                 filepath=None,
                 ):
        super().__init__(
            session=session,
            prf_name=prf_name,
            prf_col=prf_col,
            base_table_name=base_table_name,
            table_name=table_name
        )
        self.filepath = filepath

    # region filepath  #################################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def filepath(self):
        return self._filepath

    @filepath.setter
    @debug(lvl=logging.NOTSET)
    def filepath(self, value):
        try:
            str_value = str(value)
        except ValueError:
            raise AttributeError("{0}: Value cannot be converted to string: {1}".format("filepath", value))
        else:
            fileroot = config.SOURCE_PATH / "cep_price_console" / "db_management"

            # TODO: Production Change
            filepath = str_value
            # filepath = fileroot + str_value
            if is_path_exists_or_creatable(filepath):
                self._filepath = filepath
            else:
                raise AttributeError("{0}: Value is not a valid filepath: {1}".format("filepath", filepath))
    # endregion ########################################################################################################


class StaticTable(ConsoleTable):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='Static table initiated')
    def __init__(self,
                 session,
                 prf_name,
                 prf_col,
                 base_table_name,
                 table_name,
                 master_table_name=None):
        super().__init__(
            session=session,
            prf_name=prf_name,
            prf_col=prf_col,
            base_table_name=base_table_name,
            table_name=table_name
        )
        self.master_table_name = master_table_name
        self._append_stmt = None

    # region append_stmt  ##############################################################################################
    @property
    @debug(lvl=logging.NOTSET)
    def append_stmt(self):
        return self._append_stmt

    @append_stmt.setter
    @debug(lvl=logging.DEBUG)
    def append_stmt(self, value):
        self._append_stmt = value
    # endregion ########################################################################################################


class CurrentTable(ARWTable):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG)
    def append(self):
        filepath_useful = self.filepath.replace('\\\\', '+-+-+-+-').replace('\\', '\\\\').replace('+-+-+-+-', '\\\\')
        order_mapping_dict = {}
        temp_field_key_list = list(self.fields.keys())
        with open(filepath_useful, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                for col_num, col_name in enumerate(row.keys()):
                    for field_key in sorted(temp_field_key_list, key=lambda x: int(x)):
                        field_obj = self.fields.get(field_key)
                        if field_obj.arw_name == col_name:
                            order_mapping_dict[col_num] = field_obj
                            temp_field_key_list.remove(field_key)
                            break
                break

        field_lst = []
        set_lst = []
        set_dict = {}
        var_cntr_int = 0

        for field_key in sorted(order_mapping_dict.keys(), key=lambda x: int(x)):
            field_obj = order_mapping_dict.get(field_key)
            if field_obj.logical_field == "N":
                if field_obj.data_type in (
                        "BigInteger", "Date", "DateTime", "Float", "Integer", "Numeric", "SmallInteger", "Time"):
                    var_cntr_int += 1
                    var_str = "@var" + str(var_cntr_int)
                    set_dict[var_str] = field_obj
                    field_lst.append("    {0}".format(var_str))
                elif not field_obj.generated:
                    # field_lst.append("    {0}".format(field_obj.column_name))
                    field_lst.append("    `{0}`".format(field_obj.column_name))
            elif field_obj.logical_field == "Y":
                if field_obj.column_name not in ("ID", "Date_Time_Stamp"):
                    pass
        for var_str, field_obj in set_dict.items():
            if field_obj.data_type in ("Date", "DateTime", "Time"):
                func_str = "STR_TO_DATE"
                format_str = ""
                aug_var_str = var_str
                if field_obj.data_type == "DateTime":
                    format_str = "%Y-%m-%d %H.%i.%s"
                elif field_obj.data_type == "Date":
                    format_str = "%m/%d/%Y"
                elif field_obj.data_type == "Time":
                    format_str = "%h:%i %p"
                    aug_var_str = "CONCAT(SUBSTRING({0},1,5),' ',SUBSTRING({0},6))".format(var_str)
                set_lst.append("    `{col_name}` = {func_str}({aug_var_str}, '{format_str}')".format(
                    col_name=field_obj.column_name,
                    func_str=func_str,
                    aug_var_str=aug_var_str,
                    format_str=format_str
                ))
            elif field_obj.data_type in ("BigInteger", "Float", "Integer", "Numeric", "SmallInteger"):
                func_str = "NULLIF"
                aug_var_str = var_str
                set_lst.append("    `{col_name}` = {func_str}({aug_var_str}, '')".format(
                    col_name=field_obj.column_name,
                    func_str=func_str,
                    aug_var_str=aug_var_str,
                ))
        set_stmt = ""
        if len(set_dict) == 0:
            pass
        elif len(set_dict) > 0:
            set_stmt = "\n" + ',\n'.join(map(str, set_lst)) + ",\n   "

        file_creation_date = creation_date(self.filepath)
        filepath_useful = self.filepath.replace('\\', '\\\\')
        sql = text("""
        LOAD DATA LOCAL INFILE '{filename}'
        INTO TABLE `{schema_name}`.`{table_name}`
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\\"'
        LINES TERMINATED BY '\\r\\n'
        IGNORE 1 LINES (
        {field_lst}
        )
        SET{set_stmt} `Date_Time_Stamp` = '{file_creation_date}';""".format(
            filename=filepath_useful,
            schema_name=self.prf_name,
            table_name=self.table_name,
            field_lst=',\n'.join(map(str, field_lst)),
            set_stmt=set_stmt,
            file_creation_date=file_creation_date))
        self.session.execute(sql)
        self.session.commit()


class ArchiveTable(ARWTable):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self,
                 session,
                 prf_name,
                 prf_col,
                 base_table_name,
                 table_name,
                 filepath=None,
                 ):
        super().__init__(
            session=session,
            prf_name=prf_name,
            prf_col=prf_col,
            base_table_name=base_table_name,
            table_name=table_name,
            filepath=filepath)
        self._append_stmt = None

    @debug(lvl=logging.DEBUG, prefix='')
    def append(self):
        # noinspection PyUnusedLocal, PyUnresolvedReferences
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        query_stmt = "self.session.query(\n"

        insert_stmt = "ARW_PRF_Mapping.{table_name}.__table__.insert().from_select([\n".format(
            table_name=self.table_name
        )

        for col_num, field_obj in sorted(self.fields.items(), key=lambda x: int(x[0])):
            if field_obj.column_name != 'ID':
                if not field_obj.generated:
                    query_stmt += "    ARW_PRF_Mapping.{base_table_name}_01_current.{field_name},\n".format(
                        base_table_name=self.base_table_name,
                        field_name=field_obj.column_name
                    )

                    insert_stmt += "    ARW_PRF_Mapping.{table_name}.__table__.c.{field_name},\n".format(
                        table_name=self.table_name,
                        field_name=field_obj.column_name
                    )
        query_stmt += ")"
        print(query_stmt)
        # noinspection PyUnusedLocal
        query_obj = eval(query_stmt)
        insert_stmt += "    ],\n    query_obj\n)"
        # noinspection PyUnusedLocal
        insert_obj = eval(insert_stmt)
        server_utils.mysql_engine.execute(insert_obj)

    @debug(lvl=logging.DEBUG, prefix='')
    def max_date_time(self):
        # noinspection PyUnusedLocal, PyUnresolvedReferences
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping

        statement = "self.session.query(func.max(ARW_PRF_Mapping.{table_name}.__table__.c.Date_Time_Stamp)).scalar()" \
            .format(table_name=self.table_name)
        evaluated_statement = None
        try:
            evaluated_statement = eval(statement)
        finally:
            return evaluated_statement

    @debug(lvl=logging.DEBUG, prefix='')
    def delete_sub_max_date_time(self):
        # noinspection PyUnresolvedReferences, PyUnusedLocal
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        max_date_time_per_date_statement = \
            "self.session.query(" \
            "func.max(ARW_PRF_Mapping.{table_name}.__table__.c.Date_Time_Stamp).label('DateTime')," \
            "func.DATE(ARW_PRF_Mapping.{table_name}.__table__.c.Date_Time_Stamp).label('Date'))." \
            "group_by(func.DATE(ARW_PRF_Mapping.{table_name}.__table__.c.Date_Time_Stamp)).subquery()".format(
                table_name=self.table_name)
        # noinspection PyUnusedLocal
        max_date_time_per_date = eval(max_date_time_per_date_statement)

        id_not_max_date_time_per_date_statement = \
            "self.session.query(ARW_PRF_Mapping.{table_name}.__table__.c.ID)." \
            "outerjoin(max_date_time_per_date, " \
            "ARW_PRF_Mapping.{table_name}.__table__.c.Date_Time_Stamp == max_date_time_per_date.c.DateTime)." \
            "filter(max_date_time_per_date.c.DateTime.is_(None))".format(
                table_name=self.table_name)

        id_not_max_date_time_per_date = eval(id_not_max_date_time_per_date_statement)

        # noinspection PyUnusedLocal
        delete_list = [r[0] for r in id_not_max_date_time_per_date]

        delete_not_max_id_statement = \
            "ARW_PRF_Mapping.{table_name}.__table__.delete().where(" \
            "ARW_PRF_Mapping.{table_name}.__table__.c.ID.in_(delete_list))".format(
                table_name=self.table_name)

        delete_not_max_id = eval(delete_not_max_id_statement)

        server_utils.mysql_engine.execute(delete_not_max_id)


logger = CustomAdapter(logging.getLogger(str(__name__)), None)


@debug(lvl=logging.NOTSET, prefix='')
def reset_table(table_obj):
    # noinspection PyUnusedLocal
    drop_and_create = True
    if drop_and_create:
        if not server_utils.mysql_engine.dialect.has_table(server_utils.mysql_engine,
                                                           table_obj.__table__.name,
                                                           schema=table_obj.__table__.schema):
            logger.log(logging.NOTSET, "Table does not exist: {schema_name}.{table_name}".format(
                schema_name=table_obj.__table__.schema, table_name=table_obj.__table__.name))
            table_obj.__table__.create(server_utils.mysql_engine)
        else:
            logger.log(logging.NOTSET, "Table exists: {schema_name}.{table_name}".format(
                schema_name=table_obj.__table__.schema, table_name=table_obj.__table__.name))
            table_obj.__table__.drop(server_utils.mysql_engine)
            table_obj.__table__.create(server_utils.mysql_engine)
    else:
        statement = ("TRUNCATE `{schema_name}`.`{table_name}`;".format(schema_name=table_obj.__table__.schema,
                                                                       table_name=table_obj.__table__.name))
        logger.log(logging.NOTSET, "{schema_name}.{table_name} Truncate Statement: {statement}".
                   format(schema_name=table_obj.__table__.schema,
                          table_name=table_obj.__table__.name,
                          statement=statement))
        server_utils.mysql_engine.execute(statement)


@debug(lvl=logging.DEBUG, prefix='')
def schema_exists(schema_name):
    try:
        server_utils.mysql_engine.execute("SHOW CREATE SCHEMA `{0}`;".format(schema_name)).scalar()
        PrimaryReportFile.logger.log(logging.NOTSET, "Schema Exists: {0}".format(schema_name))
        return True
    except exc.DBAPIError:
        PrimaryReportFile.logger.log(logging.NOTSET, "Schema Does Not Exist: {0}".format(schema_name))
        return False


@debug(lvl=logging.DEBUG, prefix='')
def schema_create(schema_name):
    PrimaryReportFile.logger.log(logging.NOTSET, "Creating Schema: {0}".format(schema_name))
    server_utils.mysql_engine.execute(CreateSchema(schema_name))


@debug(lvl=logging.DEBUG, prefix='')
def schema_create_if_not_exists(schema_name):
    if not schema_exists(schema_name):
        schema_create(schema_name)

