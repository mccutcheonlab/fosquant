import sys
import os
import logging

import numpy as np

from datetime import datetime

from read_roi import read_roi_zip

def flatten_list(listoflists):
    flat_list = [item for sublist in listoflists for item in sublist]
    return flat_list

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
    logfile = os.path.join(logdir, "{}.log".format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))

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
    
def get_scaled_roi(roipath, series_hires=8, series_lowres=12):

    roidata = read_roi_zip(roipath)
    scale_factor = (series_hires - series_lowres)**2

    rois = {}
    for item in roidata:
        s = roidata[item]
        print(s)
        print(type(s))
        try:
            x, y, w, h = s["left"], s["top"], s["width"], s["height"]
        except KeyError:
            print("XYWH not found. Calculating from coordinates.")
            x = np.min(s["x"])
            y = np.min(s["y"])
            w = np.max(s["x"]) - np.min(s["x"])
            h = np.max(s["y"]) - np.min(s["y"])

        rois[item] = tuple([dim*scale_factor for dim in (x,y,w,h)])

    return rois

def get_rois(path):
    roifiles = [os.path.join(path,f) for f in os.listdir(path) if f.endswith("ROIs.zip")]

    rois = []
    for roipath in roifiles:
        roidata = read_roi_zip(roipath)
        rois.append(list(roidata.keys()))

    rois = [roi.replace("_", "") for roi in flatten_list(rois)]

    return rois
