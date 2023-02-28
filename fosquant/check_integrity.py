import os
from read_roi import read_roi_zip
from helper_fx import setup_logger

def flatten_list(listoflists):
    flat_list = [item for sublist in listoflists for item in sublist]
    return flat_list

def check_rawdata(project_dir, logger):

    logger.info("Checking integrity of RAWDATA folder...")

    rawdata_dir = os.path.join(project_dir, "rawdata")
    if not os.path.exists(rawdata_dir):
        logger.info("No rawdata folder exists in {}".format(project_dir))
        return False

    vsi_files = [vsi for vsi in os.listdir(rawdata_dir) if vsi.endswith(".vsi")]
    logger.info("Found {} .vsi files".format(len(vsi_files)))

    rois = []
    if len(vsi_files) > 0:
        for vsi in vsi_files:
            scanfolder = "_{}_".format(vsi.split(".")[0])
            if scanfolder not in os.listdir(rawdata_dir):
                logger.info("No matching vsi data folder found for {}".format(vsi))
                return False
            else:
                logger.info("Matching vsi data folder found for {}".format(vsi))

            roifile = "{}_ROIs.zip".format(vsi.split(".")[0])
            if roifile not in os.listdir(rawdata_dir):
                logger.info("No ROI zip file found for {}".format(vsi))
                return False
            else:
                logger.info("Matching ROI zip file found for {}".format(vsi))
                roidata = read_roi_zip(os.path.join(rawdata_dir, roifile))
                rois.append(list(roidata.keys()))
        
        rois = [roi.replace("_", "") for roi in flatten_list(rois)]
    
    logger.info("{} ROIs found.".format(len(rois)))
    
    return rois

def check_lowres(project_dir, logger, rois=None):

    logger.info("Checking integrity of LOWRES folder...")

    lowres_dir = os.path.join(project_dir, "lowres")
    if not os.path.exists(lowres_dir):
        logger.info("No lowres folder exists in {}".format(project_dir))
        return False
    
    jpg_files = [jpg for jpg in os.listdir(lowres_dir) if jpg.endswith(".jpg")]
    logger.info("Found {} .jpg files".format(len(jpg_files)))

    if rois != None:
        section_names = [s.split(".")[0].split("_")[-1] for s in jpg_files] 
        if rois.sort() == section_names.sort():
            logger.info("ROIs from ROI file match lowres sections")
        else:
            logger.info("ROIs from ROI file DO NOT MATCH lowres sections")
            return False
            # add code to say where mismatch is

    # check if .json exists (or other alignment files)

def check_hires(project_dir, logger, rois=None):

    logger.info("Checking integrity of HIRES folder...")

    hires_dir = os.path.join(project_dir, "hires")
    if not os.path.exists(hires_dir):
        logger.info("No hires folder exists in {}".format(project_dir))
        return False
    
    chans = [folder for folder in os.listdir(hires_dir) if "chan" in folder]

    for chan in chans:
        chan_dir = os.path.join(hires_dir, chan)
        pngs = [png for png in os.listdir(chan_dir) if png.endswith(".png")]
        if len(pngs) == 0:
            logger.info("No PNGs found in {}".format(chan_dir))
        else:
            



    print(chan_paths)
    # jpg_files = [jpg for jpg in os.listdir(lowres_dir) if jpg.endswith(".jpg")]
    # logger.info("Found {} .jpg files".format(len(jpg_files)))




## Look for hires folder
# check for channel folders
# look for pngs, if none alert and move on, if some check that all exist
# look for cellpose output


project_dir = "D:\\TestData\\fostrap\\FTIG\\FT108"
project_dir = "/mnt/d/TestData/fostrap/FTIG/FT108"

logger = setup_logger(project_dir)

rois = check_rawdata(project_dir, logger)

# if rois != None:
#     check_lowres(project_dir, logger, rois=rois)
# else:
#     check_lowres(project_dir, logger)

check_hires(project_dir, logger)







## 