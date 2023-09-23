import sys
import os
import logging

import numpy as np

from skimage.draw import polygon2mask

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

def get_mean_rois_vect(im, im_rois):
    """
    Replaces ROI cell masks with mean values from original image. Useful for
    selecting cells based on a threshold value of fluorescence.
    
    Args
    im : Image object (e.g. from PNG) or numpy array (mxn)
        Image with original pixel values
    im_rois : Image object (e.g. from PNG) or numpy array (mxn)
        Image with ROI masks, e.g. from cellpose

    Returns:
        Image array with cell ROIs replaced with mean value.
        List of floats with mean for each ROI
    """
    # Create a mask for pixels that belong to ROIs (excluding background label 0)
    roi_mask = im_rois > 0

    # Calculate the unique labels for the ROIs
    unique_labels = np.unique(im_rois[roi_mask])

    # Calculate the mean values for each ROI
    roi_means = np.array([np.mean(im[im_rois == label]) for label in unique_labels])

    # Create a lookup table to map labels to their corresponding mean values
    lookup_table = np.zeros(im_rois.max() + 1, dtype=roi_means.dtype)
    lookup_table[unique_labels] = roi_means

    # Apply the mean values to the entire image using the lookup table
    im_out = lookup_table[im_rois]

    # Ensure im_out is of the same data type as im
    im_out = im_out.astype(im.dtype)

    print(np.percentile(roi_means, [1,10,25,50,75,90,99]))

    return im_out, roi_means

def make_thresholded_mask(im, im_mask, roi_coords, threshold=0):

    mask = polygon2mask(im.shape, roi_coords)
    im_mask_roi = im_mask * mask

    im_mean, _ = get_mean_rois_vect(im, im_mask_roi)

    im_mean_mask = im_mean > threshold

    return im_mask * im_mean_mask

def normalize_image(image):
    normed_im = image/np.max(image) * 255
    return np.clip(normed_im, 0, 255)