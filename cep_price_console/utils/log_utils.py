import yaml
import traceback
import logging.handlers
import logging.config
import os
from functools import wraps, partial
import inspect
import time
from tkinter import messagebox

# ERROR_INVALID_NAME = 123
# is_frozen = getattr(sys, 'frozen', False)
# frozen_temp_path = getattr(sys, '_MEIPASS', '')
#
# # Determining if the program has been "frozen". Locating the base directory
# if is_frozen:
#     basedir = frozen_temp_path
# else:
#     basedir = os.path.dirname(os.path.abspath(__file__))

debug_log = None
info_log = None
error_log = None


class SystemLogFilter(logging.Filter):
    def filter(self, record):
        return True


class MyLogFormatter(logging.Formatter):
    # format: "%(asctime)s | %(levelname)-8s - %(name)s - %(funcName)s: - %(message)s"
    def format(self, record):
        msg = '%s [%-8s] %50s | %s' % (self.formatTime(record), record.levelname, record.name, record.msg)
        return msg


class CustomAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    @staticmethod
    def indent():
        indentation_level = 0
        for stack in traceback.extract_stack():
            if '\\Python37-32\\lib\\logging\\' not in str(stack) and '\\Python37-32\\lib\\tkinter\\' not in str(stack):
                indentation_level += 1
        return indentation_level - 4

    @staticmethod
    def message(msg, *args):
        return msg.translate({ord('{'): None, ord('}'): None}).format(*args)
        # return msg.format(*args)

    def process(self, msg, kwargs):
        # return '{i}{m}'.format(i='...|'*self.indent(), m=line), kwargs
        result = []
        if isinstance(msg, tuple):
            for line in msg:
                result.append('{i}{m}'.format(i='...|'*self.indent(), m=line))
        else:
            for line in msg.splitlines():
                result.append('{i}{m}'.format(i='...|'*self.indent(), m=line))
        # return ("\n".join(result)), kwargs
        return result, kwargs

    # noinspection PyProtectedMember
    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            for line in msg:
                self.logger._log(level, self.message(line, args), (), **kwargs)


def debug(func=None, *, lvl=logging.DEBUG, prefix=''):

    if func is None:
        return partial(debug, lvl=lvl, prefix=prefix)

    log = CustomAdapter(logging.getLogger(func.__module__))

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        msg = ""
        param_str = ""
        sig = inspect.signature(func)
        ba = sig.bind(*args, **kwargs)
        for arg_name, arg in ba.arguments.items():
            if arg_name != "self":
                if not isinstance(arg, dict):
                    param_str += "{{" + str(arg_name) + " = " + str(arg) + "}}, "
                else:
                    param_str += "{0} Dictionary: ".format(arg_name)
                    for key, value in arg.items():
                        param_str += str(key) + " = " + str(value) + ", "
                    param_str += ", "
        if prefix != '':
            msg = prefix + " | "

        msg += func.__qualname__

        if param_str != "":
            pre_msg = msg + " | Parameters: " + param_str
        else:
            pre_msg = msg
        log.log(lvl, pre_msg)
        result = func(*args, **kwargs)
        end = time.time()
        post_msg = msg + " | Dur: {0:10.3}".format(end - start)
        log.log(lvl, post_msg)
        return result
    return wrapper


def setup_logging(
        default_level=logging.DEBUG,
        env_key='LOG_CFG'
):
    """Setup logging configuration
    """
    from cep_price_console.utils import config
    global debug_log
    global info_log
    global error_log
    config.LOGGING_PATH.mkdir(parents=True, exist_ok=True)

    message = []
    path = config.LOGGING_YAML
    value = os.getenv(env_key, None)
    message.append("Value: {}".format(value))

    if value:
        path = value
        message.append("Value True. Path: {}".format(path))
    else:
        message.append("Value False. Path: {}".format(path))

    if path.exists():
        message.append("Path Exists")
        with open(path, 'rt') as f:
            message.append("Config file being interpreted")
            yaml_config = yaml.safe_load(f.read())
        message.append("Logging configuration being set")
        yaml_config['handlers']['debug_file_handler']['filename'] = config.DEBUG_LOG
        yaml_config['handlers']['info_file_handler']['filename'] = config.INFO_LOG
        yaml_config['handlers']['error_file_handler']['filename'] = config.ERROR_LOG
        logging.config.dictConfig(yaml_config)
    else:
        messagebox.showwarning(
            "Log Configuration File Missing",
            "Path does not exist. No configuration applied: {}".format(path)
        )
        logging.basicConfig(level=default_level)
    return message
