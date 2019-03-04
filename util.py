import time
import functools
import os
import subprocess
import logging
import logging.handlers


def time_count(func):
    """Calculate the running time of the function. Will change the
    return of the function. Returns a tuple containing the time and the
    return of the function itself
    """
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        st = time.time()
        task_r = func(*args, **kwargs)
        et = time.time()
        mt = et - st
        return task_r, mt
    return func_wrapper


def ensure_dir(path, backup=True):
    """Make sure a path exists.

    If the path exists but It's not a directory, it can be backed up
    or deleted.
    :param path: A path string.
    :param backup: True or False.
    """
    if os.path.isdir:
        return
    tmp = path
    while True:
        if os.path.lexists(tmp):
            if not os.path.isdir(tmp) and backup:
                bak = tmp + ".%s" % (int(time.time()))
                os.rename(tmp, bak)
            elif not os.path.isdir(tmp):
                os.remove(tmp)
            os.makedirs(path)
            break
        tmp = os.path.dirname(tmp)


def execute_cmd(cmd):
    """Execute a Linux command synchronously.

    :param cmd: A Linux command
    :return: (str, str, str)
    """
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    return p.returncode, output, err


def execute_cmd_async(cmd):
    """Execute a Linux command asynchronously."""
    subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def get_logger(name="sven.txt", directory=None, file_level=logging.DEBUG,
               terminal_level=logging.WARN, max_bytes=10*1024*1024):
    """Convenient to record log.

    It is very convenient for debugging and logging.
    :param name: Log file name，If directory is None. created in the current directory.
    :param directory: If directory is not exist, will create.
    :param file_level: log file record level.
    :param terminal_level: log terminal show level.
    :param max_bytes: log file max Bytes.
    :return: <class 'logging.Logger'>
    """
    terminal_formatter = logging.Formatter(
        "%(module)s.%(funcName)s:%(lineno)s - %(levelname)s - %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(module)s.%(funcName)s:%(lineno)s - %(levelname)s - %(message)s", '%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if directory is None:
        path = os.path.join(os.path.dirname(__file__), name)
    else:
        os.mkdir(directory)
        path = os.path.join(directory, name)
    # create handler file_handler
    terminal_handler = logging.StreamHandler()
    file_handler = logging.handlers.RotatingFileHandler(
        path, maxBytes=max_bytes, backupCount=10)
    # set level
    terminal_handler.setLevel(terminal_level)
    file_handler.setLevel(file_level)
    # set formatter
    terminal_handler.setFormatter(terminal_formatter)
    file_handler.setFormatter(file_formatter)
    # add handler
    logger.addHandler(terminal_handler)
    logger.addHandler(file_handler)
    return logger

