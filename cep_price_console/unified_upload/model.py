from cep_price_console.db_management.server_utils import mysql_engine, mysql_session_maker, mysql_base, \
    schema_create_if_not_exists, table_name_drop, get_mysql_conn_string, table_exists
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.sql import expression, functions, exists
from sqlalchemy import Table, Column, Integer, inspect, and_, String, Boolean, not_, case, Numeric
from cep_price_console.utils import config
from cep_price_console.utils.utils import subprocess_args
import inspect
import pathlib
import subprocess
from csvkit.utilities import in2csv, csvsql, csvcut, csvformat, csvgrep
from cep_price_console.utils.log_utils import CustomAdapter, debug
import logging
import os
import xlrd
import sys

logger = CustomAdapter(logging.getLogger(str(__name__)), None)

# Vendor Item Match
# TODO: Include Customer Part Number matching logic option
# TODO: Remove datatype and custom column name for initial rollout
# TODO: Bring vendor selection information into initial query
# TODO: Test the shit out of it.


class Model(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    @debug(lvl=logging.DEBUG, prefix='')
    def __init__(self, view):
        self.view = view

        # View Accessible Properties
        self.wb_filename_default = ""
        self.ws_sheet_names_default = []
        self.ws_name_selection_default = ""
        self.header_row_default = 1

        self.wb_filename = self.wb_filename_default
        self.ws_sheet_names = self.ws_sheet_names_default
        self.ws_name_selection = self.ws_name_selection_default
        self.header_row = self.header_row_default

        self.__wb = None
        self.__ws_obj = None
        self.__dest_wb_filename_obj = ""
        self.__dest_wb = ""
        self.__dest_ws_name = ""
        self.__dest_ws_obj = ""
        self.__dest_header_row = 0
        self.quote_char = "$"
        self.transfer_dir = config.DATA_PATH
        self.__import_table_name = None
        self.__match_table_name = None
        self.match_table = None

        self.schema = config.config["mysql_database"]["mysql_user_database"]
        self.table = None

        # Not Set
        self.archive_dir = None
        self.archive_filename = None
        # This one is required, so don't worry about it
        self.vpn = Function(self, name="Vendor Part Number", req=True, sort=1)

        # For a listed primary vendor, produce a list of parts and

        # If Function.field is not None, Compare VPN to CEP VPN. Produce a list of VPNs that need to change.
        #   Match CEP PN to the altered field to allow the process to continue
        self.vpn_rev = Function(self, name="Vendor Part Number Revision", sort=1)

        # Compares our action indicator to the one in the column. I think the logic to this one is going to be
        self.lagb_action_indicator = Function(self, name="Action Indicator", sort=1)
        self.description = Function(self, name="Description", sort=1)
        self.uom_primary_unit = Function(self, name="Primary UOM", sort=1)
        self.uom_primary_qty = Function(self, name="Primary UOM Quantity", sort=1)
        self.uom_secondary_unit = Function(self, name="Secondary UOM", sort=1)
        self.mfg_name = Function(self, name="Manufacturer Name", sort=1)
        self.mfg_part_number = Function(self, name="Manufacturer Part Number", sort=1)
        self.mfg_url = Function(self, name="Manufacturer URL", sort=1)
        self.brand = Function(self, name="Brand", sort=1)
        self.upc = Function(self, name="UPC", sort=1)
        self.height = Function(self, name="Height", sort=1)
        self.depth = Function(self, name="Depth", sort=1)
        self.width = Function(self, name="Width", sort=1)
        self.weight = Function(self, name="Weight", sort=1)
        self.volume = Function(self, name="Volume", sort=1)
        self.c1_cost = Function(self, name="C1 Cost", sort=1)
        self.l1_price = Function(self, name="L1 Price", sort=1)
        self.unspsc = Function(self, name="UNSPSC Code", sort=1)
        self.func_dict = Function.func_dict
        self.all_primary_vend = False
        self.all_vend_chk_box = False
        self.sel_list = []

    # region wb_filename  ##########################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def wb_filename(self):
        return self.__wb_filename

    @wb_filename.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def wb_filename(self, value):
        self.__wb_filename = value
        self.ws_sheet_names = self.ws_sheet_names_default
        self.ws_name_selection = self.ws_name_selection_default
        self.header_row = self.header_row_default
        if self.wb_filename != self.wb_filename_default:
            try:
                self.__wb = xlrd.open_workbook(self.wb_filename, on_demand=True)
            except Exception:
                raise
            else:
                self.ws_sheet_names = self.wb.sheet_names()
        else:
            self.__wb = None

    # endregion ########################################################################################################

    # region getters  ##################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def wb(self):
        return self.__wb
    # endregion ########################################################################################################

    # region ws_name  ##################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_name_selection(self):
        return self.__ws_name_selection

    @ws_name_selection.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def ws_name_selection(self, value):
        self.__ws_name_selection = value
        self.header_row = self.header_row_default
    # endregion ########################################################################################################

    # region getters  ##################################################################################################
    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def ws_obj(self):
        return self.__ws_obj

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def import_table_name(self):
        return self.__import_table_name

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def match_table_name(self):
        return self.__match_table_name
    # endregion ########################################################################################################

    def sql_import(self):
        # TODO: Archive the original sheet in some way, along with the csv conversion
        try:
            schema_create_if_not_exists(config.config["database"]["mysql_user_database"])
            table_name_drop(schema_name=self.schema, table_name=self.import_table_name)
        except Exception as ex:
            Model.logger.log(logging.ERROR, "Exception: {0} Arguments: {1}".format(type(ex).__name__, ex.args))
            raise
        else:
            try:
                # noinspection PyUnresolvedReferences
                # from csvkit import convert
                in2csv.launch_new_instance()
                args = [csvkit_tool("in2csv"), str(self.wb_filename)]
                args.extend(["--sheet", self.ws_name_selection])  # Append the worksheet name
                if self.header_row != 1:
                    args.extend(["-K", str(self.header_row - 1)])
                args.extend(["|"])  # Convert worksheet into csv, pass to csvcut
                args.extend([csvkit_tool("csvcut"), "-l", "|"])  # Add line number to csv output
                args.extend([csvkit_tool("csvformat")])
                args.extend(["-U", "1"])  # Quote all fields
                args.extend(["-Q", self.quote_char])  # Set Quote character
                args.extend(["|"])  # Pass to csvsql
                args.extend([csvkit_tool("csvsql")])
                args.extend(["-q", self.quote_char])  # Set Quote character
                args.extend(["-u", "1"])  # Set Quote character
                args.extend(["-e", "ansi"])  # Set encoding
                args.extend(["--db", get_mysql_conn_string(user_db=self.schema)])  # Set the db connection string
                args.extend(["--snifflimit", "0"])
                args.extend(["--tables", self.import_table_name])  # Name the table
                args.extend(["--insert", "--overwrite"])
                Model.logger.log(logging.DEBUG,
                                 "Beginning unified csvkit step: {0}".format(subprocess.list2cmdline(args)))

                csvsql_process = subprocess.Popen(args, shell=True, **subprocess_args(False))
                out, err = csvsql_process.communicate()
                Model.logger.log(logging.DEBUG, "Out: {0}".format(out))
                Model.logger.log(logging.DEBUG, "Err: {0}".format(err))
            except subprocess.CalledProcessError as ex:
                Model.logger.log(logging.ERROR,
                                 "CalledProcessError Exception: {0} Arguments: {1}".format(type(ex).__name__, ex.args))
                raise
            except Exception as ex:
                Model.logger.log(logging.ERROR, "Exception: {0} Arguments: {1}".format(type(ex).__name__, ex.args))
                raise
            else:
                Model.logger.log(logging.DEBUG, "Reflecting table in SQLAlchemy:")
                self.table = Table(self.import_table_name,
                                   mysql_base.metadata,
                                   autoload=True,
                                   autoload_with=mysql_engine,
                                   schema=self.schema)

    @debug(lvl=logging.DEBUG, prefix='')
    def upload_query(self):
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        return session.query(self.table)

    @debug(lvl=logging.DEBUG, prefix='')
    def fetch_vendors(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        temp_list = []
        for num, name in (
                session.query(ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Num,
                              ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Name
                              ).order_by(ARW_PRF_Mapping.vend_main_01_current.__table__.c.Vend_Name.asc())):
            temp_list.append("{0:_<5}__{1}".format(num, name.upper().strip()))
        return temp_list

    @debug(lvl=logging.DEBUG, prefix='')
    def create_match_table(self):
        # TODO: Make datatypes make sense.
        schema_create_if_not_exists(config.config["database"]["mysql_user_database"])
        self.match_table = Table(self.match_table_name, mysql_base.metadata,
                                 Column('ID',
                                        Integer,
                                        primary_key=True,
                                        unique=True,
                                        index=True,
                                        autoincrement=True),
                                 Column('Prod_Num',
                                        String(length=255),
                                        nullable=True,
                                        index=True),
                                 Column('Vend_Part_Num',
                                        String(length=255),
                                        nullable=True,
                                        index=True),
                                 Column('VPN_Match',
                                        String(length=255),
                                        nullable=True,
                                        index=True),
                                 Column('Vend_UPC_Num',
                                        String(length=255),
                                        nullable=True),
                                 Column('Vend_UPC_Num_Match',
                                        String(length=255),
                                        nullable=True),
                                 Column('Mfg_Num',
                                        String(length=255),
                                        nullable=True),
                                 Column('Mfg_Num_Match',
                                        String(length=255),
                                        nullable=True),
                                 Column('UPC',
                                        String(length=255),
                                        nullable=True),
                                 Column('UPC_Match',
                                        String(length=255),
                                        nullable=True),
                                 Column('Primary_Vend',
                                        String(length=255),
                                        nullable=True),
                                 Column('Vend_Num',
                                        String(length=255),
                                        nullable=True),
                                 Column('Selected',
                                        Boolean,
                                        default=False),
                                 Column('Match_Types',
                                        String(length=255),
                                        nullable=True),
                                 Column('C1_Cost',
                                        Numeric(precision=19, scale=4),
                                        nullable=True),
                                 Column('Display_UOM',
                                        String(length=3),
                                        nullable=True),
                                 Column('Status',
                                        String(length=2),
                                        nullable=True),
                                 schema=self.schema)
        if table_exists(self.schema, self.match_table_name):
            self.match_table.drop(bind=mysql_engine)
        self.match_table.create(bind=mysql_engine)
        Model.logger.log(logging.ERROR, "Table created: {0}.{1}".format(self.match_table_name, self.schema))

    @debug(lvl=logging.DEBUG, prefix='')
    def fill_match_table(self):
        import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        if self.all_primary_vend:
            all_primary_query = session.query(
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num.label("Prod_Num"),
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Part_Num.label("Vend_Part_Num"),
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_UPC_Num.label("Vend_UPC_Num"),
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num.label("Vend_Num"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Mfg_No.label("Mfg_Num"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.UPC.label("UPC"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend.label("Primary_Vend")
            ).join(
                ARW_PRF_Mapping.prod_main_01_current.__table__,
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num ==
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num
            ).filter(
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num ==
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend
            )

            primary_insert = self.match_table.insert().from_select([
                "Prod_Num",
                "Vend_Part_Num",
                "Vend_UPC_Num",
                "Vend_Num",
                "Mfg_Num",
                "UPC",
                "Primary_Vend",
                "C1_Cost",
                "Display_UOM",
                "Status"
            ], all_primary_query)

            mysql_engine.execute(primary_insert)
        elif self.all_vend_chk_box:
            all_vendors_query = session.query(
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num.label("Prod_Num"),
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Part_Num.label("Vend_Part_Num"),
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_UPC_Num.label("Vend_UPC_Num"),
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num.label("Vend_Num"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Mfg_No.label("Mfg_Num"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.UPC.label("UPC"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend.label("Primary_Vend"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.C1_Cost.label("C1_Cost"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Display_UOM.label("Display_UOM"),
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Status.label("Status")
            ).join(
                ARW_PRF_Mapping.prod_main_01_current.__table__,
                ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num ==
                ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num
            )

            all_vendors_insert = self.match_table.insert().from_select([
                "Prod_Num",
                "Vend_Part_Num",
                "Vend_UPC_Num",
                "Vend_Num",
                "Mfg_Num",
                "UPC",
                "Primary_Vend",
                "C1_Cost",
                "Display_UOM",
                "Status"
            ], all_vendors_query)

            mysql_engine.execute(all_vendors_insert)
        elif self.sel_list:
            for parameter in self.sel_list:
                vend_num = parameter.var.get()[:5]

                primary = False
                if 'selected' in parameter.prim_chk_box.state():
                    primary = True
                    param_query = session.query(
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num.label("Prod_Num"),
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Part_Num.label("Vend_Part_Num"),
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_UPC_Num.label("Vend_UPC_Num"),
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num.label("Vend_Num"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Mfg_No.label("Mfg_Num"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.UPC.label("UPC"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend.label("Primary_Vend"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.C1_Cost.label("C1_Cost"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Display_UOM.label("Display_UOM"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Status.label("Status")
                    ).join(
                        ARW_PRF_Mapping.prod_main_01_current.__table__,
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num ==
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num
                    ).filter(and_(
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend == vend_num,
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num == vend_num)
                    )

                secondary = False
                if 'selected' in parameter.sec_chk_box.state():
                    secondary = True
                    param_query = session.query(
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num.label("Prod_Num"),
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Part_Num.label("Vend_Part_Num"),
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_UPC_Num.label("Vend_UPC_Num"),
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num.label("Vend_Num"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Mfg_No.label("Mfg_Num"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.UPC.label("UPC"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Primary_Vend.label("Primary_Vend"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.C1_Cost.label("C1_Cost"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Display_UOM.label("Display_UOM"),
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Status.label("Status")
                    ).join(
                        ARW_PRF_Mapping.prod_main_01_current.__table__,
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Prod_Num ==
                        ARW_PRF_Mapping.prod_main_01_current.__table__.c.Prod_Num
                    ).filter(
                        ARW_PRF_Mapping.prod_vend_01_current.__table__.c.Vend_Num == vend_num
                    )

                print("Vend ID: {}, Primary: {}, Secondary: {}".format(vend_num, primary, secondary))

                insert = self.match_table.insert().from_select([
                    "Prod_Num",
                    "Vend_Part_Num",
                    "Vend_UPC_Num",
                    "Vend_Num",
                    "Mfg_Num",
                    "UPC",
                    "Primary_Vend",
                    "C1_Cost",
                    "Display_UOM",
                    "Status"
                ], param_query)

                mysql_engine.execute(insert)

    @debug(lvl=logging.DEBUG, prefix='')
    def get_output_query(self):
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        match_dict = {}
        for col in self.match_table.c:
            match_dict[col.name] = col
        for col in self.table.c:
            match_dict[col.name] = col
        output_query = session.query(*match_dict.values()).join(
            self.table,
            self.match_table.c.VPN_Match == self.vpn.upload_col,
            isouter=True
        )
        return output_query

    @debug(lvl=logging.DEBUG, prefix='')
    def match_query_dict(self):
        match_dict = dict(
            Prod_Num=self.match_table.c.Prod_Num,
            Vend_Part_Num=self.match_table.c.Vend_Part_Num,
            VPN_Match=expression.collate(expression.cast(self.vpn.upload_col, String(255)),
                                         'utf8mb4_0900_ai_ci').label("VPN_Match"),
            Vend_UPC_Num=self.match_table.c.Vend_UPC_Num.label("Vend_UPC_Num"),
            Vend_UPC_Num_Match=literal_column("Vend_UPC_Num_Match"),
            Mfg_Num=self.match_table.c.Mfg_Num.label("Mfg_Num"),
            Mfg_Num_Match=literal_column("Mfg_Num_Match"),
            UPC=self.match_table.c.UPC.label("UPC"),
            UPC_Match=literal_column("UPC_Match"),
            Primary_Vend=self.match_table.c.Primary_Vend.label("Primary_Vend"),
            Selected=self.match_table.c.Selected.label("Selected"),
            Match_Types=self.match_table.c.Match_Types.label("Match_Types"),
            C1_Cost=self.match_table.c.C1_Cost.label("C1_Cost"),
            Display_UOM=self.match_table.c.Display_UOM.label("Display_UOM"),
            Status=self.match_table.c.Status.label("Status")
        )
        # TODO: Add columns for the remaining fields you want from the upload
        if self.upc.upload_col is not None:  # TODO: Why the cast and collate?
            print("there's a upc")
            match_dict['Vend_UPC_Num_Match'] = expression.collate(expression.cast(
                self.upc.upload_col, String(255)), 'utf8mb4_0900_ai_ci').label("Vend_UPC_Num_Match")
            match_dict['UPC_Match'] = expression.collate(expression.cast(
                self.upc.upload_col, String(255)), 'utf8mb4_0900_ai_ci').label("UPC_Match")

        if self.mfg_part_number.upload_col is not None:  # TODO: Why the cast and collate?
            print("there's a mfg_part_number")
            match_dict['Mfg_Num_Match'] = expression.collate(expression.cast(
                self.mfg_part_number.upload_col, String(255)), 'utf8mb4_0900_ai_ci').label("Mfg_Num_Match")

        return match_dict

    @debug(lvl=logging.DEBUG, prefix='')
    def insert_vpn_matches_cull_zeros(self):
        print(self.vpn.upload_col.name)
        match_dict = self.match_query_dict()
        for k, v in match_dict.items():
            print(k)
            print(v.name)
        vpn_match_insert = self.match_table.update().where(
            self.match_table.c.Vend_Part_Num == match_dict.get("VPN_Match")
        ).values(match_dict)
        mysql_engine.execute(vpn_match_insert)

        self.zero_cull(upload_column_label="VPN_Match")
        self.match_type_append(upload_column_label="VPN_Match", cep_column_label="Vend_Part_Num")

    # noinspection PyComparisonWithNone
    @debug(lvl=logging.DEBUG, prefix='')
    def insert_matches(self, upload_column_label, cep_column_label):
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        match_dict = self.match_query_dict()

        # noinspection PyPep8
        match_query = session.query(*match_dict.values()).join(
            self.table,
            self.match_table.c[cep_column_label] == match_dict.get(upload_column_label)
        ).filter(and_(match_dict.get(upload_column_label).isnot(None),
                      match_dict.get(upload_column_label) != "",
                      match_dict.get(upload_column_label) != "0",
                      not_(session.query(exists().where(and_(
                          self.match_table.c.Prod_Num == self.match_table.c.Prod_Num,
                          self.match_table.c.VPN_Match == match_dict.get('VPN_Match')))).scalar())))

        insert = self.match_table.insert().from_select([*match_dict.keys()], match_query)

        mysql_engine.execute(insert)

    @debug(lvl=logging.DEBUG, prefix='')
    def zero_cull(self, upload_column_label):
        zero_cull = self.match_table.update().where(
            self.match_table.c[upload_column_label] == "0"
        ).values({upload_column_label: None})
        mysql_engine.execute(zero_cull)

    @debug(lvl=logging.DEBUG, prefix='')
    def match_type_append(self, upload_column_label, cep_column_label):
        # noinspection PyComparisonWithNone,PyPep8
        match_type = self.match_table.update().where(and_(
            self.match_table.c[upload_column_label].isnot(None),
            self.match_table.c.Match_Types.isnot(None))
        ).values({'Match_Types': (self.match_table.c.Match_Types + ", {}".format(cep_column_label))})
        mysql_engine.execute(match_type)

        # noinspection PyComparisonWithNone,PyPep8
        match_type = self.match_table.update().where(and_(
            self.match_table.c[upload_column_label].isnot(None),
            self.match_table.c.Match_Types.is_(None))
        ).values({'Match_Types': "{}".format(cep_column_label)})
        mysql_engine.execute(match_type)

    # noinspection PyComparisonWithNone
    @debug(lvl=logging.DEBUG, prefix='')
    def insert_matches_cull_zeros(self, upload_column_label, cep_column_label):
        self.insert_matches(upload_column_label, cep_column_label)
        self.zero_cull(upload_column_label)
        self.match_type_append(upload_column_label, cep_column_label)

    @debug(lvl=logging.DEBUG, prefix='')
    def case_generator(self, cep_col, label_text):
        # noinspection PyComparisonWithNone,PyPep8
        return case([(cep_col.isnot(None), "{}".format(label_text)),
                     (cep_col.is_(None), None)], else_='problem')

    @debug(lvl=logging.DEBUG, prefix='')
    def match_gui_query(self, cep_col, upload_col, match_desc, id_suffix):
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        return session.query(
            self.match_table.c.ID.label("ID_1"),
            functions.concat(expression.cast(self.match_table.c.ID, String),
                             literal_column("'{}'".format(id_suffix))).label("ID_2"),
            cep_col.label("CEP_Value"),
            upload_col.label("Uploaded_Value"),
            literal_column("'{}:'".format(match_desc), String(length=50)).label("Match_Type"))

    @debug(lvl=logging.DEBUG, prefix='')
    def all_match_gui_query(self):
        self.create_match_table()
        self.fill_match_table()
        self.insert_vpn_matches_cull_zeros()
        self.insert_matches_cull_zeros(upload_column_label='Vend_UPC_Num_Match', cep_column_label='Vend_UPC_Num')
        self.insert_matches_cull_zeros(upload_column_label='UPC_Match', cep_column_label='UPC')
        self.insert_matches_cull_zeros(upload_column_label='Mfg_Num_Match', cep_column_label='Mfg_Num')

        # VPN_Match_Label = self.case_generator(cep_col=self.match_table.c.VPN_Match, label_text="VPN")
        mfg_num_zero_cull = self.match_table.update().where(
            self.match_table.c.Mfg_Num_Match == "0"
        ).values({'Mfg_Num_Match': None})
        mysql_engine.execute(mfg_num_zero_cull)

        # Vend_UPC_Num_Label = self.case_generator(cep_col=self.match_table.c.Vend_UPC_Num_Match, label_text="Vend_UPC")
        # Mfg_Num_Match = self.case_generator(cep_col=self.match_table.c.Mfg_Num_Match, label_text="Mfg Num")
        # UPC_Label = self.case_generator(cep_col=self.match_table.c.UPC_Match, label_text="UPC")
        # noinspection PyCallingNonCallable
        session = mysql_session_maker()
        query = session.query(
            self.match_table.c.ID.label("ID_1"),
            self.match_table.c.ID.label("ID_2"),
            self.match_table.c.Prod_Num.label("CEP_Value"),
            self.match_table.c.Match_Types.label("Uploaded_Value"),
            # functions.concat(VPN_Match_Label, Vend_UPC_Num_Label, Mfg_Num_Match, UPC_Label).label("Uploaded_Value"),
            literal_column("'Match:'", String(length=50)).label("Match_Type"))

        union_queries = [self.match_gui_query(cep_col=self.match_table.c.Vend_Part_Num,
                                              upload_col=self.match_table.c.VPN_Match,
                                              match_desc="Vendor Part Number Match",
                                              id_suffix="a")]

        if self.upc.upload_col is not None:
            union_queries.append(self.match_gui_query(cep_col=self.match_table.c.Vend_UPC_Num,
                                                      upload_col=self.match_table.c.Vend_UPC_Num_Match,
                                                      match_desc="Vendor UPC Match",
                                                      id_suffix="b"))
            union_queries.append(self.match_gui_query(cep_col=self.match_table.c.UPC,
                                                      upload_col=self.match_table.c.UPC_Match,
                                                      match_desc="UPC Match",
                                                      id_suffix="c"))
        if self.mfg_part_number.upload_col is not None:
            union_queries.append(self.match_gui_query(cep_col=self.match_table.c.Mfg_Num,
                                                      upload_col=self.match_table.c.Mfg_Num_Match,
                                                      match_desc="Mfg Part Number Match",
                                                      id_suffix="d"))

        return query.union(*union_queries)

    @debug(lvl=logging.DEBUG, prefix='')
    def check_upload_table(self, checked_dict):
        id_list = [int(key) for key in checked_dict.keys()]
        # noinspection PyComparisonWithNone,PyPep8
        update_select = self.match_table.update().where(and_(
            self.match_table.c.ID.in_(id_list),
            self.match_table.c.VPN_Match.isnot(None))
        ).values({'Selected': True})
        mysql_engine.execute(update_select)


@debug(lvl=logging.DEBUG, prefix='')
def csvkit_tool(tool_name):
    toolpath_opt = dict(
        in2csv=in2csv,
        csvsql=csvsql,
        csvcut=csvcut,
        csvformat=csvformat,
        csvgrep=csvgrep
    )
    tool_path = toolpath_opt.get(tool_name)

    if tool_path is None:
        raise ValueError

    is_frozen = getattr(sys, 'frozen', False)
    frozen_temp_path = getattr(sys, '_MEIPASS', '')
    # Determining if the program has been "frozen". Locating the base directory
    if is_frozen:
        logger.log(logging.DEBUG, "Frozen")
        # for k, v in sys.modules.items():
        #     logger.log(logging.DEBUG, "{}|{}".format(k, v))
        if sys.modules.get("csvkit.utilities.{}".format(tool_name), None):
            logger.log(logging.DEBUG, "Got it")
            thing = inspect.getsourcefile(sys.modules["csvkit.utilities.{}".format(tool_name)])
            logger.log(logging.DEBUG, "thing: {}".format(thing))
            thing2 = pathlib.Path(thing)
            thing3 = os.path.join(thing2.parent.resolve(), thing2.stem)
            logger.log(logging.DEBUG, "thing3: {}".format(thing3))
            return thing3
    else:
        logger.log(logging.DEBUG, "Not Frozen")
        path_obj = pathlib.Path(inspect.getsourcefile(tool_path))
        print(os.path.join(path_obj.parent.resolve(), path_obj.stem))
        return os.path.join(path_obj.parent.resolve(), path_obj.stem)


class Function(object):
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    func_dict = {}

    @debug(lvl=logging.NOTSET, prefix='')
    def __init__(self, model, name, req=False, sort=100):
        self.model = model
        self.name = name
        self.req = req
        self.sort = sort
        self.__field_desc = None
        self.upload_col = None
        Function.func_dict[self.name] = self

    @property
    @debug(lvl=logging.NOTSET, prefix='')
    def field_desc(self):
        return self.__field_desc

    @field_desc.setter
    @debug(lvl=logging.DEBUG, prefix='')
    def field_desc(self, value):
        self.__field_desc = value
        self.upload_col = self.model.table.c[self.__field_desc]
        # for columny in self.model.table.columns:
        #     if self.field_desc.name == columny.name:
        #         self.upload_col = columny
        #         break
