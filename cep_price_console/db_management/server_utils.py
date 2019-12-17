from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from cep_price_console.utils.log_utils import debug, CustomAdapter
import logging
from functools import wraps
from cep_price_console.utils import config
from sqlalchemy.types import DateTime, String
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.engine.default import DefaultDialect
import sqlparse

logger = CustomAdapter(logging.getLogger(str(__name__)), None)

PY3 = str is not bytes
text = str
int_type = int
str_type = str
reflected = False
cust_shipto_combo_expansion = None


class StringLiteral(String):
    """Teach SA how to literalize various things."""

    def literal_processor(self, dialect):
        super_processor = super(StringLiteral, self).literal_processor(dialect)

        def process(value):
            if isinstance(value, int_type):
                return text(value)
            if not isinstance(value, str_type):
                value = text(value)
            result = super_processor(value)
            if isinstance(result, bytes):
                result = result.decode(dialect.encoding)
            return result

        return process


# noinspection PyAbstractClass
@debug(lvl=logging.NOTSET, prefix='')
class LiteralDialect(DefaultDialect):
    colspecs = {
        # prevent various encoding explosions
        String: StringLiteral,
        # teach SA about how to literalize a datetime
        DateTime: StringLiteral,
        # don't format py2 long integers to NULL
        NullType: StringLiteral,
    }


# @debug(lvl=logging.NOTSET, prefix='')
def literalquery(statement):
    """NOTE: This is entirely insecure. DO NOT execute the resulting strings."""
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        statement = statement.statement
    compiled_statement = statement.compile(
        dialect=LiteralDialect(),
        compile_kwargs={'literal_binds': True},
    ).string
    # compiled_statement.replace("SELECT ", "SELECT\n").replace(", ", ",\n")
    return compiled_statement


# @debug(lvl=logging.NOTSET, prefix='')
def verbose_query(statement):
    for desc in statement.column_descriptions:
        name = desc.get('name').replace("'", "").replace('"', "")
        logger.log(logging.DEBUG, name)
    logger.log(logging.DEBUG, "Literal Query: \n" + sqlparse.format(
        literalquery(statement), reindent=True, keyword_case='upper'))
    logger.log(logging.DEBUG, "Beginning of Results" + "-" * 80)
    for line in statement:
        logger.log(logging.DEBUG, str(list(line)))
    logger.log(logging.DEBUG, "End of Results" + "-" * 80)


# region SQL Alchemy Connection Attributes  ############################################################################
mysql_engine = None
mysql_base = declarative_base()
mysql_session_maker = None


@debug(lvl=logging.DEBUG, prefix='')
def mysql_test_creds(user_db=None):
    global mysql_engine

    mysql_engine = create_engine(
        get_mysql_conn_string(user_db),
        echo=True,
        pool_recycle=3600
    )

    try:
        mysql_engine.connect()
    except (ProgrammingError, OperationalError) as e:
        mysql_engine = None
        logger.log(logging.DEBUG, "There is a problem with your login credentials. More detail: {}".format(e.args))
        return False
    else:
        if mysql_session_maker is None:
            mysql_init_engine()
        return True


@debug(lvl=logging.DEBUG, prefix='')
def mysql_init_engine():
    global mysql_engine
    global mysql_base
    global mysql_session_maker

    mysql_base.metadata.bind = mysql_engine
    mysql_session_maker = sessionmaker(bind=mysql_engine)
    CustomAdapter(logging.getLogger('sqlalchemy.engine'))

    import cep_price_console.db_management.ARW_PRF_Mapping as ARW_PRF_Mapping
    if hasattr(ARW_PRF_Mapping, "InformReflection"):
        ARW_PRF_Mapping.InformReflection.prepare(mysql_engine)

    from cep_price_console.db_management.ddi_data_warehouse import DDIDataWarehouse
    DDIDataWarehouse.prepare(mysql_engine)


@debug(lvl=logging.DEBUG, prefix='')
def get_mysql_conn_string(user_db):
    conn_string_template = 'mysql+pymysql://{username}:{password}@{host}:3306/{db}?local_infile=1'
    remote_args = {
        "username": config.config["mysql_database"]["mysql_username"],
        "password": config.config["mysql_database"]["mysql_password"],
        "host": config.config["mysql_database"]["mysql_host_var"],
        "db": ""
    }
    if user_db is not None:
        remote_args["db"] = config.config["mysql_database"]["mysql_user_database"]
    return_value = conn_string_template.format(**remote_args)
    logger.log(logging.DEBUG, "MySQL Connection String: {}".format(return_value))
    return return_value


def mysql_login_required(func):
    @wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if mysql_session_maker is None:
            config_gui = config.config_gui_obj
            config.sect_mysql_database.toggle_creds(good_creds=False)
            config_gui.deiconify()
            config_gui.update_values()
            return None
        return func(*args, **kwargs)
    return wrapper_login_required
# endregion ############################################################################################################


# region Microsoft SQL Connection Attributes  ##########################################################################
mssql_engine = None
mssql_base = declarative_base()
mssql_session_maker = None


# noinspection PyUnusedLocal
@debug(lvl=logging.DEBUG, prefix='')
def mssql_test_creds(user_db=None):
    global mssql_engine
    mssql_engine = create_engine(get_mssql_conn_string(), echo=True)
    logger.log(logging.DEBUG, "mssql_engine type: {}".format(type(mssql_engine)))
    try:
        logger.log(logging.DEBUG, "mssql_engine trying connection")
        mssql_engine.connect()
    except (ProgrammingError, OperationalError) as e:
        mssql_engine = None
        logger.log(logging.DEBUG, "There is a problem with your login credentials. More detail: {}".format(e.args))
        return False
    else:
        logger.log(logging.DEBUG,
                   "mssql_engine no exception. mssql_session_maker: {}".format(type(mssql_session_maker)))
        if mssql_session_maker is None:
            mssql_init_engine()
        return True


@debug(lvl=logging.DEBUG, prefix='')
def mssql_init_engine():
    global mssql_engine
    global mssql_base
    global mssql_session_maker

    mssql_base.metadata.bind = mssql_engine
    mssql_session_maker = sessionmaker(bind=mssql_engine)
    CustomAdapter(logging.getLogger('sqlalchemy.engine'))

    from cep_price_console.db_management.mssql_database import MSSQL_Database
    MSSQL_Database.prepare(mssql_engine)


@debug(lvl=logging.DEBUG, prefix='')
def get_mssql_conn_string():
    conn_string_template = 'mssql+pyodbc://{username}:{password}@{dsn}'
    remote_args = {
        "username": config.config["mssql_database"]["mssql_username"],
        "password": config.config["mssql_database"]["mssql_password"],
        "dsn": config.config["mssql_database"]["mssql_dsn"]
    }
    return_value = conn_string_template.format(**remote_args)
    logger.log(logging.DEBUG, "MSSQL Connection String: {}".format(return_value))
    return return_value


def mssql_login_required(func):
    @wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if mssql_session_maker is None:
            config_gui = config.config_gui_obj
            config.sect_mssql_database.toggle_creds(good_creds=False)
            config_gui.deiconify()
            config_gui.update_values()
            return None
        return func(*args, **kwargs)
    return wrapper_login_required
# endregion ############################################################################################################


@debug(lvl=logging.DEBUG, prefix='')
def schema_create_if_not_exists(schema_name):
    if not schema_exists(schema_name):
        schema_create(schema_name)


@debug(lvl=logging.DEBUG, prefix='')
def schema_exists(schema_name):
    try:
        mysql_engine.execute("SHOW CREATE SCHEMA `{0}`;".format(schema_name)).scalar()
        logger.log(logging.NOTSET, "Schema Exists: {0}".format(schema_name))
        return True
    except exc.DBAPIError:
        logger.log(logging.NOTSET, "Schema Does Not Exist: {0}".format(schema_name))
        return False


@debug(lvl=logging.DEBUG, prefix='')
def schema_create(schema_name):
    logger.log(logging.NOTSET, "Creating Schema: {0}".format(schema_name))
    mysql_engine.execute(CreateSchema(schema_name))


@debug(lvl=logging.DEBUG, prefix='')
def table_create_if_not_exists(schema_name, table_name, table_obj_name):
    schema_create_if_not_exists(schema_name)
    if not table_exists(schema_name, table_name):
        table_create(table_obj_name)
    else:
        table_drop(table_obj_name)
        table_create(table_obj_name)


@debug(lvl=logging.DEBUG, prefix='')
def table_exists(schema_name, table_name):
    if not mysql_engine.dialect.has_table(mysql_engine, table_name, schema=schema_name):
        logger.log(logging.NOTSET,
                   "Table does not exist: {0}.{1}".format(schema_name, table_name))
        return False
    else:
        logger.log(logging.NOTSET,
                   "Table exists: {0}.{1}".format(schema_name, table_name))
        return True


@debug(lvl=logging.DEBUG, prefix='')
def table_create(table_obj_name):
    statement = "{table_obj_name}.__table__.create({engine_name})" \
        .format(table_obj_name=table_obj_name,
                engine_name="mysql_engine")
    logger.log(logging.NOTSET, "{table_obj_name} Create Statement: {statement}".
               format(table_obj_name=table_obj_name,
                      statement=statement))
    exec(statement)


@debug(lvl=logging.DEBUG, prefix='')
def table_drop(table_obj_name):
    logger.log(logging.DEBUG, "{table_obj_name} Drop".
               format(table_obj_name=table_obj_name))
    statement = "{table_obj_name}.__table__.drop({engine_name})" \
        .format(table_obj_name=table_obj_name,
                engine_name="mysql_engine")
    logger.log(logging.DEBUG, "{table_obj_name} Drop Statement: {statement}".
               format(table_obj_name=table_obj_name,
                      statement=statement))
    exec(statement)
    logger.log(logging.DEBUG, "{table_obj_name} Post Drop".
               format(table_obj_name=table_obj_name))


@debug(lvl=logging.DEBUG, prefix='')
def table_name_drop(schema_name, table_name):
    try:
        # noinspection PyUnusedLocal
        connection = mysql_engine.raw_connection()
        cursor = connection.cursor()
    except Exception:
        raise
    else:
        statement = "DROP TABLE IF EXISTS `{schema_name}`.`{table_name}`;" \
            .format(schema_name=schema_name,
                    table_name=table_name)
        logger.log(logging.DEBUG, "{table_obj_name} Drop Statement: {statement}".
                   format(table_obj_name=table_name,
                          statement=statement))
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        logger.log(logging.DEBUG, "{table_obj_name} Post Drop".
                   format(table_obj_name=table_name))
