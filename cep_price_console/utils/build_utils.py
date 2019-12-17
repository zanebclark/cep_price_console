import os
import logging
from cep_price_console.utils.log_utils import setup_logging, CustomAdapter, debug
from cep_price_console.utils.utils import get_basedir
import subprocess
import sys
import ttkwidgets.assets
import pathlib
import inspect
import PyInstaller.__main__
from cep_price_console.utils import config
from PyInstaller.utils.hooks import collect_data_files


@debug(lvl=logging.DEBUG, prefix='')
def gen_list_files_for_nsis():
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    logger.log(logging.DEBUG, "source_dir: {source_dir} \ninst_list: {inst_list} \nuninst_list: {uninst_list}".format(
        source_dir=config.DIST_PATH,
        inst_list=config.INSTALL_LIST,
        uninst_list=config.UNINSTALL_LIST
    ))
    # templates for the output
    inst_dir_tpl = '  SetOutPath "$INSTDIR%s"'
    inst_file_tpl = '  File "${FILES_SOURCE_PATH}%s"'
    uninst_file_tpl = '  Delete "$INSTDIR%s"'
    uninst_dir_tpl = '  RMDir "$INSTDIR%s"'

    if not config.DIST_PATH.is_dir():
        logger.log(logging.DEBUG,
                   "Source directory isn't a directory: {source_dir}".format(source_dir=config.DIST_PATH))
        sys.exit(1)

    stack_of_visited = []
    counter_files = 0
    counter_dirs = 0
    logger.log(logging.DEBUG,
               "Generating the install & uninstall list of files for directory: {0}".format(
                   config.DIST_PATH)
               )
    with config.UNINSTALL_LIST.open('w+') as uninstall_list:
        with config.INSTALL_LIST.open('w+') as install_list:
            print("  ; Files to install\n", file=install_list)
            print('  !define FILES_SOURCE_PATH "{0}"\n'.format(config.DIST_PATH), file=install_list)
            print("  ; Files and dirs to remove\n", file=uninstall_list)

            for dirpath, dirnames, filenames in os.walk(config.DIST_PATH):
                logger.log(logging.DEBUG, "Dirpath: {0}".format(dirpath))
                logger.log(logging.DEBUG, "Dirnames: {0}".format(dirnames))
                logger.log(logging.DEBUG, "Filenames: {0}".format(filenames))

                counter_dirs += 1

                files_and_dirs = dirnames + filenames
                # first separate files
                my_files = [x for x in files_and_dirs if os.path.isfile(dirpath + os.sep + x)]

                # and truncate dir name
                my_dir = dirpath[len(str(config.DIST_PATH)):]

                # save it for uninstall
                stack_of_visited.append(
                    (my_files, my_dir)
                )

                # build install list
                if len(my_files):
                    print(inst_dir_tpl % my_dir, file=install_list)
                    for f in my_files:
                        print(inst_file_tpl % (my_dir + os.sep + f), file=install_list)
                        counter_files += 1
                    print("  ", file=install_list)

        logger.log(logging.DEBUG, "Install list done")
        logger.log(logging.DEBUG, "   {0} files in {1} dirs".format(counter_files, counter_dirs))

        stack_of_visited.reverse()

        # Now build the uninstall list
        for (my_files, my_dir) in stack_of_visited:
            for f in my_files:
                print(uninst_file_tpl % (my_dir + os.sep + f), file=uninstall_list)
            print(uninst_dir_tpl % my_dir, file=uninstall_list)
            print("  ", file=uninstall_list)

    logger.log(logging.DEBUG, "Uninstall list done. Got to end.\n")


@debug(lvl=logging.DEBUG, prefix='')
def gen_config_list_for_nsis():
    # templates for the output
    temp_define_int = '!define {var} {value}'
    temp_define_str = '!define {var} "{value}"'

    with config.CFG_LIST.open('w+') as cfg_file:
        print("; Config values\n", file=cfg_file)
        print(temp_define_str.format(var="APP_TITLE", value=config.APP_TITLE), file=cfg_file)
        print(temp_define_str.format(var="APP_NAME", value=config.APP_NAME), file=cfg_file)
        print(temp_define_str.format(var="COMPANY_NAME", value=config.COMPANY_NAME), file=cfg_file)
        print(temp_define_str.format(
            var="DESCRIPTION",
            value=config.DESCRIPTION.replace('\n', ' ').replace('\r', ' ')
        ), file=cfg_file)
        print(temp_define_str.format(var="LICENSE_DATA_DOC", value=config.LICENSE_DATA_FILE), file=cfg_file)
        # print(temp_define_str.format(var="SOURCE_DIR", value=config.SOURCE_PATH), file=cfg_file) # Don't need it
        print(temp_define_str.format(var="MEDIA_DIR", value=config.MEDIA_PATH), file=cfg_file)
        print(temp_define_str.format(
            var="MEDIA_SUBDIR",
            value=config.MEDIA_PATH.relative_to(config.SOURCE_PATH)
        ), file=cfg_file)
        print(temp_define_str.format(var="DIST_PATH", value=config.DIST_PATH), file=cfg_file)
        print(temp_define_str.format(var="ICON_FILE", value=config.ICON_FILE.name), file=cfg_file)

        print(temp_define_str.format(var="COMMENTS", value=config.COMMENTS), file=cfg_file)
        print(temp_define_str.format(var="README", value=config.README_FILENAME), file=cfg_file)
        # TODO: Where is this readme file?

        print(temp_define_str.format(var="FAVICON_FILE", value=config.FAVICON.name), file=cfg_file)
        print(temp_define_int.format(var="VERSION_MAJOR", value=config.VERSION_MAJOR), file=cfg_file)
        print(temp_define_int.format(var="VERSION_MINOR", value=config.VERSION_MINOR), file=cfg_file)
        print(temp_define_int.format(var="VERSION_BUILD", value=config.VERSION_BUILD), file=cfg_file)


@debug(lvl=logging.DEBUG, prefix='')
def get_add_data_list():
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    add_data_list = []

    add_data_exclude = ['.git',
                        '.idea',
                        "build",
                        "cep_price_console",
                        "dist",
                        "__pycache__",
                        ".gitignore",
                        "__main__.py",
                        "build_utils.py"]
    logger.log(logging.DEBUG, "Add Data Exclude List: {}".format(add_data_exclude))

    for _, dirnames, filenames in os.walk(config.SOURCE_PATH):
        for dir_thing in dirnames:
            if dir_thing not in add_data_exclude:
                add_data_list.append((dir_thing, dir_thing))
        for file in filenames:
            if file not in add_data_exclude:
                add_data_list.append((file, "."))
        break

    path_obj = pathlib.Path(inspect.getsourcefile(ttkwidgets))
    add_data_list.append((
        str(path_obj.parent / "assets"),
        "ttkwidgets\\assets"
    ))

    add_data_list.append((
        str(config.SOURCE_PATH / 'cep_price_console' / 'utils' / "log_config.yaml"),
        "cep_price_console\\utils"
    ))

    add_data_list.extend(collect_data_files('text_unidecode'))

    logger.log(logging.DEBUG, "Datalist:")
    for printing in add_data_list:
        logger.log(logging.DEBUG, "\t{:<30}: {:<30}".format(printing[0], printing[1]))
    return add_data_list


@debug(lvl=logging.DEBUG, prefix='')
def run_pyinstaller():
    setup_logging(get_basedir())
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)

    if config.SPEC_FILE.exists():
        config.SPEC_FILE.unlink()
    if config.CONFIG_FILE.exists():
        config.CONFIG_FILE.unlink()

    hidden_import_list = [
        "pyodbc",
        "pymysql",
        "parsedatetime.pdt_locales.de_DE",
        "parsedatetime.pdt_locales.en_AU",
        "parsedatetime.pdt_locales.en_US",
        "parsedatetime.pdt_locales.es",
        "parsedatetime.pdt_locales.fr_FR",
        "parsedatetime.pdt_locales.icu",
        "parsedatetime.pdt_locales.nl_NL",
        "parsedatetime.pdt_locales.pt_BR",
        "parsedatetime.pdt_locales.ru_RU",
        "cep_price_console.db_management.ARW_PRF_Mapping"]

    logger.log(logging.DEBUG, "Hidden Import List: {}".format(hidden_import_list))

    pyinstaller_args = ['--noconfirm', '--log-level', 'DEBUG', '--nowindowed', '--clean', '--specpath',
                        str(config.SOURCE_PATH),
                        '--add-binary=C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs;.', '--distpath',
                        str(config.SOURCE_PATH / 'dist'), '--workpath', str(config.SOURCE_PATH / 'build')]

    for add_data in get_add_data_list():
        pyinstaller_args.append('--add-data={0};{1}'.format(add_data[0], add_data[1]))
    for hidden_import in hidden_import_list:
        pyinstaller_args.extend(['--hidden-import', hidden_import])
    pyinstaller_args.extend(['--icon', str(config.FAVICON), '--name', str(config.APP_NAME),
                             str(config.SOURCE_PATH / 'cep_price_console' / '__main__.py')])
    logger.log(logging.DEBUG, str(pyinstaller_args))
    PyInstaller.__main__.run(pyinstaller_args)


@debug(lvl=logging.DEBUG, prefix='')
def run_nsis():
    logger = CustomAdapter(logging.getLogger(str(__name__)), None)
    if not config.SETUP_PATH.exists():
        config.SETUP_PATH.mkdir(parents=True)
    else:
        for dirpath, dirnames, filenames in os.walk(config.SETUP_PATH):
            for file in filenames:
                try:
                    os.remove(file)
                except OSError:
                    pass

    gen_list_files_for_nsis()
    gen_config_list_for_nsis()

    nsis_args = [str(config.NSIS_PATH / "makensis.exe"),
                 '/DINST_LIST={}'.format(str(config.INSTALL_LIST)),
                 '/DUNINST_LIST={}'.format(str(config.UNINSTALL_LIST)),
                 '/DCFG_LIST={}'.format(str(config.CFG_LIST)),
                 str(config.SOURCE_PATH / 'cep_price_console' / 'utils' / "create_installer.nsi")]

    try:
        logger.log(logging.DEBUG, "nsis argument list: {}".format(nsis_args))
        subprocess.check_output(nsis_args, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        raise


@debug(lvl=logging.DEBUG, prefix='')
def build_script():
    run_pyinstaller()
    run_nsis()


if __name__ == "__main__":
    build_script()
