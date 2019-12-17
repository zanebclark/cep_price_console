from cep_price_console.utils.log_utils import CustomAdapter, debug
import logging.config
import platform
import time
import os
import sys
import errno
import subprocess
import pathlib
import os.path

logger = CustomAdapter(logging.getLogger(str(__name__)), None)

ERROR_INVALID_NAME = 123

# Windows-specific error code indicating an invalid pathname.

# See Also
# --------------------------------------------
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms681382%28v=vs.85%29.aspx
#     Official listing of all such codes.


@debug(lvl=logging.NOTSET, prefix='')
def is_pathname_valid(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    # If this pathname is either 1)not a string or 2)is but is empty, this pathname is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            result = False
            logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
            return result

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)  # _ captures the 'head' and pathname captures the 'tail'

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.

        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)  # Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
                # If an OS-specific exception is raised, its error code
                # indicates whether this pathname is valid or not. Unless this
                # is the case, this exception implies an ignorable kernel or
                # filesystem complaint (e.g., path not found or inaccessible).
                #
                # Only the following exceptions indicate invalid pathnames:
                #
                # * Instances of the Windows-specific "WindowsError" class
                #   defining the "winerror" attribute whose value is
                #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
                #   fine-grained and hence useful than the generic "errno"
                #   attribute. When a too-long pathname is passed, for example,
                #   "errno" is "ENOENT" (i.e., no such file or directory) rather
                #   than "ENAMETOOLONG" (i.e., file name too long).
                # * Instances of the cross-platform "OSError" class defining the
                #   generic "errno" attribute whose value is either:
                #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
                #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        result = False
                        logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
                        return result
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    result = False
                    logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
                    return result
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError:
        result = False
        logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
        return result
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        result = True
        logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
        return result
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?


@debug(lvl=logging.NOTSET, prefix='')
def is_path_creatable(pathname: str) -> bool:

    """
    `True` if the current user has sufficient permissions to create the passed pathname; `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.

    dirname = os.path.dirname(pathname) or os.getcwd()
    result = os.access(dirname, os.W_OK)
    logger.log(logging.NOTSET, "is_path_creatable Called. Result: {0}".format(result))
    return result


@debug(lvl=logging.NOTSET, prefix='')
def is_path_exists_or_creatable(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        result = is_pathname_valid(pathname) and (os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        result = False
    logger.log(logging.NOTSET, "is_path_exists_or_creatable Called. Result: {0}".format(result))
    return result


@debug(lvl=logging.NOTSET, prefix='')
def creation_date(path_to_file):
    if is_pathname_valid(path_to_file):
        if platform.system() == 'Windows':
            try:
                result = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(path_to_file)))
                logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
                return result
            except Exception as ex:
                template = "OS: Windows\nAn exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                result = message
                logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
                return result
        else:
            stat = os.stat(path_to_file)
            try:
                result = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stat.st_mtime))
                logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
                return result
            except Exception as ex:
                template = "OS: Not Windows\nAn exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                result = message
                logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
                return result
    elif not is_pathname_valid(path_to_file):
        result = "File does not exist or is inaccessible"
        logger.log(logging.NOTSET, "is_pathname_valid Called. Result: {0}".format(result))
        return result


def get_basedir():
    is_frozen = getattr(sys, 'frozen', False)
    frozen_temp_path = getattr(sys, '_MEIPASS', '')
    # Determining if the program has been "frozen". Locating the base directory
    if is_frozen:
        result = frozen_temp_path
    else:
        result = pathlib.Path(__file__).parent.parent.parent
    return result


@debug(lvl=logging.DEBUG, prefix='')
def subprocess_args(include_stdout=True):
    # From https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
    # Create a set of arguments which make a ``subprocess.Popen`` (and
    # variants) call work with or without Pyinstaller, ``--noconsole`` or
    # not, on Windows and Linux. Typical use::
    #
    #   subprocess.call(['program_to_run', 'arg_1'], **subprocess_args())
    #
    # When calling ``check_output``::
    #
    #   subprocess.check_output(['program_to_run', 'arg_1'],
    #                           **subprocess_args(False))
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    #
    #   Traceback (most recent call last):
    #     File "test_subprocess.py", line 58, in <module>
    #       **subprocess_args(stdout=None))
    #     File "C:\Python27\lib\subprocess.py", line 567, in check_output
    #       raise ValueError('stdout argument not allowed, it will be overridden.')
    #   ValueError: stdout argument not allowed, it will be overridden.
    #
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env})
    return ret
