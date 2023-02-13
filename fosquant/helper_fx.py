import sys
import os
import logging

from datetime import datetime


def setup_logger(projectdir):
    """Sets up logging by creating a logger object and making a directory if needed.

    Use by calling logger.info() or logger.debug()

    Args:
        projectdir (Str): Path to folder where log directory will be created.

    Returns:
        logger: Object allowing lines to be added to log. 
    """
    logdir = os.path.join(projectdir, "log")
    
    if not os.path.isdir(logdir):
        os.mkdir(logdir)

    ## setting up logger
    logfile = os.path.join(logdir, "{}.log".format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))

    logger = logging.getLogger(logfile)
    logger.setLevel(level=logging.DEBUG)

    logStreamFormatter = logging.Formatter(
    fmt=f"%(levelname)-8s %(asctime)s \t line %(lineno)s - %(message)s", 
    datefmt="%H:%M:%S"
    )
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(logStreamFormatter)
    consoleHandler.setLevel(level=logging.DEBUG)

    logger.addHandler(consoleHandler)

    logFileFormatter = logging.Formatter(
        fmt=f"%(levelname)s %(asctime)s L%(lineno)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fileHandler = logging.FileHandler(filename=logfile)
    fileHandler.setFormatter(logFileFormatter)
    fileHandler.setLevel(level=logging.DEBUG)

    logger.addHandler(fileHandler)

    logger.info("Created log file at {}".format(logfile))

    return logger

def check_existing_files(path_to_check, overwrite):
    """Checks if any files exist in given folder. If there are files, checks whether they can be overwritten.

    Args:
        path_to_check (Str): Folder to check for files
        overwrite (Bool): Option to overwrite files or not

    Returns:
        Bool: True if there are no files or if user specifies that they can be overwritten
    """
    if len(os.listdir(path_to_check)) > 0:
        if overwrite == False:
            msg = "Files found in {}. If you want to re-download or re-analyze then run the command again with the -o option.".format(path_to_check)
            try:
                logger.info(msg)
            except: # if logger not available
                print(msg)
            return False
        else:
            i = input("Overwrite option is selected. Do you want to try downloading the raw data again? (y/N)")
            if i != "y":
                return False
            else:
                return True
    else:
        return True