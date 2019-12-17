from cep_price_console.utils.log_utils import debug, CustomAdapter
from cep_price_console.utils.utils import get_basedir
from cep_price_console.utils.config_gui import ConfigGUI, MySQLSection, MSSQLSection, IniSection, IniKey
import logging
import configparser
import os
import pathlib
from appdirs import AppDirs
from tkinter import messagebox

logger = CustomAdapter(logging.getLogger(str(__name__)), None)

config = None


COMPANY_NAME = "Controlled Environment Products"
DESCRIPTION = ""
VERSION_MAJOR = "1"
VERSION_MINOR = "1"
VERSION_BUILD = "1"
COMMENTS = ""
VERSION_COMBO = "v{major}-{minor}".format(major=VERSION_MAJOR, minor=VERSION_MINOR)
APP_TITLE = "CEP Price Console {}".format(VERSION_COMBO)
APP_NAME = "cep_price_console_{}".format(VERSION_COMBO)

NSIS_PATH = pathlib.Path("")
SOURCE_PATH = pathlib.Path(get_basedir())
SPEC_FILE = SOURCE_PATH / "{}.spec".format(APP_NAME)

DIST_PATH = SOURCE_PATH / "dist" / APP_NAME
LICENSE_DATA_FILE = SOURCE_PATH / "LICENSE.md"
SETUP_PATH = DIST_PATH / "setup"
UNINSTALL_LIST = SETUP_PATH / "uninstall_list.nsh"
INSTALL_LIST = SETUP_PATH / "install_list.nsh"
CFG_LIST = SETUP_PATH / "cfg_list.nsh"

DATA_PATH = SOURCE_PATH / "data"
ARW_PRF_MAPPING_FILE = DATA_PATH / "ARW_PRF_Mapping" / "ARW_PRF_Definitions_v1_03.xlsm"
MEDIA_PATH = DATA_PATH / "media"
FAVICON = MEDIA_PATH / "CEP_favicon.ico"
ICON_FILE = MEDIA_PATH / "CEP_logo.gif"

LOGGING_YAML = SOURCE_PATH / "cep_price_console" / "utils" / "log_config.yaml"

README_FILENAME = SOURCE_PATH / "README.md"

dirs = AppDirs(APP_NAME, COMPANY_NAME)
CONFIG_FILE = pathlib.Path(dirs.user_config_dir, "config.ini")
LOGGING_PATH = pathlib.Path(dirs.user_log_dir)
DEBUG_LOG = LOGGING_PATH / "debug.log"
INFO_LOG = LOGGING_PATH / "info.log"
ERROR_LOG = LOGGING_PATH / "error.log"

config_gui_obj = ConfigGUI()

sect_directory = IniSection("directory", gui_obj=config_gui_obj)
sect_mysql_database = MySQLSection("mysql_database", gui_obj=config_gui_obj)
sect_mssql_database = MSSQLSection("mssql_database", gui_obj=config_gui_obj)


# region Directory Section  ####################################################################################
contract_dir = IniKey(
    section=sect_directory,
    key="contract_dir",
    default=os.path.join("\\\\", "${{{s}:{k}}}".format(s="mysql_database", k="mysql_host_var"),
                         "attachments",
                         "PriceContracts"),
    read_only=True
)
arw_export_dir = IniKey(
    section=sect_directory,
    key="arw_export_dir",
    default=os.path.join("\\\\", "${{{s}:{k}}}".format(s="mysql_database", k="mysql_host_var"),
                         "attachments",
                         "AUTOARW FILE EXPORTS"),
    read_only=True
)
# endregion ####################################################################################################

# region Database Section  #####################################################################################
# MySQL Credentials
mysql_username = IniKey(
    section=sect_mysql_database,
    key="mysql_username",
    default="")
mysql_password = IniKey(
    section=sect_mysql_database,
    key="mysql_password",
    default="")
mysql_user_database = IniKey(
    section=sect_mysql_database,
    key="mysql_user_database",
    default="")
mysql_host_var = IniKey(
    section=sect_mysql_database,
    key="mysql_host_var",
    default="",
    read_only=True)

# MSSQL Credentials
mssql_username = IniKey(
    section=sect_mssql_database,
    key="mssql_username",
    default="")
mssql_password = IniKey(
    section=sect_mssql_database,
    key="mssql_password",
    default="")
mssql_dsn = IniKey(
    section=sect_mssql_database,
    key="mssql_dsn",
    default="",
    read_only=True)
# endregion ####################################################################################################
config_gui_obj.populate()


@debug(lvl=logging.DEBUG, prefix="")
def write_default_config():
    global config
    for section in IniSection.section_dict.values():
        logger.log(logging.DEBUG, "Configuring section: [{sect}]".format(sect=section))
        config[section] = {}
        for key_obj in section.key_dict.values():
            logger.log(
                logging.DEBUG,
                "Configuring key: [{s}][{k}] = {v}".format(
                    k=key_obj.key,
                    s=key_obj.section,
                    v=key_obj.default.replace("{", "{{").replace("}", "}}"))
            )
            config[str(key_obj.section)][key_obj.key] = key_obj.default
    write_config()


@debug(lvl=logging.DEBUG, prefix="")
def write_config():
    global config
    # Creating parent directory
    logger.log(logging.DEBUG, "Writing config file to {}".format(CONFIG_FILE))
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CONFIG_FILE.open('w') as config_file:
        config.write(config_file)


@debug(lvl=logging.DEBUG, prefix="")
def read_config():
    global config
    missing_dict = {
        "default": [],
        "config": []
    }
    config.read(CONFIG_FILE)
    for section_read in config.sections():
        section_message = "Section {sect}".format(sect=section_read)
        sect_obj = IniSection.section_dict.get(section_read)
        if sect_obj is not None:
            logger.log(logging.DEBUG, section_message + " match found")
            sect_obj.missing = False
        else:
            logger.log(logging.DEBUG, section_message + " default match not found")
        for key_read in config[section_read]:
            key_message = "[{section}]{key}".format(
                section=section_read, key=key_read)
            if sect_obj is not None:
                key_obj = sect_obj.key_dict.get(key_read)
                if key_obj is not None:
                    logger.log(logging.DEBUG, key_message + " match found")
                    key_obj.missing = False
                else:
                    missing_dict["default"].append(key_message)
                    logger.log(logging.DEBUG, key_message + " default match not found")
            else:
                missing_dict["default"].append(key_message)
                logger.log(logging.DEBUG, key_message + " default match not found")
    for section in IniSection.section_dict.values():
        for key_obj in section.key_dict.values():
            key_message = "[{section}]{key}".format(
                section=section.section, key=key_obj.key)
            if section.missing:
                missing_dict["config"].append(key_message)
                logger.log(logging.ERROR,
                           "Section {sect} config file match not found, Missing Keys: {sect}|{key}".format(
                               sect=key_obj.section, key=key_obj.key
                           ))
                key_obj.missing = True
            else:
                if key_obj.missing:
                    missing_dict["config"].append(key_message)
                    logger.log(logging.ERROR, "[{section}]{key} config file match not found".format(
                        section=section, key=key_obj.key, value=key_obj.default))

    missing_msg = "Your config.ini file is corrupted. \nIt is located at {}\n".format(CONFIG_FILE)
    cntr = 0
    for label, missing_list in missing_dict.items():
        if len(missing_list) != 0:
            if label == "default":
                missing_msg += "\nThe following unexpected values are present\n"
            elif label == "config":
                missing_msg += "\nThe following expected values are missing:\n"
            else:
                raise ValueError

            for val in missing_list:
                missing_msg += "    {}\n".format(val)
                cntr += 1
    if cntr != 0:
        return missing_msg
    else:
        return None


@debug(lvl=logging.DEBUG)
def init_config():
    global config
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

    # Checking for an existing configuration file
    if not CONFIG_FILE.exists():
        write_default_config()
    config_corruption_msg = read_config()

    if config_corruption_msg is not None:
        messagebox.showwarning(
            "Corrupted Config File",
            config_corruption_msg
        )


@debug(lvl=logging.DEBUG)
def file_check():
    cntr = 0
    missing_files = "The following files are missing: \n"
    must_exist = [
        SOURCE_PATH,
        LICENSE_DATA_FILE,
        ARW_PRF_MAPPING_FILE,
        FAVICON,
        ICON_FILE,
        LOGGING_YAML
    ]
    # if development_env:
    #     must_exist.extend([NSIS_PATH, SPEC_FILE])
    for filepath in must_exist:
        if not filepath.exists():
            missing_files += "    {}".format(filepath)
            cntr += 1

    if cntr != 0:
        if missing_files is not None:
            messagebox.showwarning(
                "Missing Files",
                missing_files
            )
