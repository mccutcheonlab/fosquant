import os
from read_roi import read_roi_zip
from helper_fx import setup_logger, flatten_list

def check_rawdata(project_dir, logger):

    logger.info("Checking integrity of RAWDATA folder...")

    rawdata_dir = os.path.join(project_dir, "rawdata")
    if not os.path.exists(rawdata_dir):
        logger.warning("No rawdata folder exists in {}".format(project_dir))
        return False

    vsi_files = [vsi for vsi in os.listdir(rawdata_dir) if vsi.endswith(".vsi")]
    logger.info("Found {} .vsi files".format(len(vsi_files)))

    rois = []
    if len(vsi_files) > 0:
        for vsi in vsi_files:
            scanfolder = "_{}_".format(vsi.split(".")[0])
            if scanfolder not in os.listdir(rawdata_dir):
                logger.warning("No matching vsi data folder found for {}".format(vsi))
                return False
            else:
                logger.info("Matching vsi data folder found for {}".format(vsi))

            roifile = "{}_ROIs.zip".format(vsi.split(".")[0])
            if roifile not in os.listdir(rawdata_dir):
                logger.warning("No ROI zip file found for {}".format(vsi))
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
        logger.warning("No lowres folder exists in {}".format(project_dir))
        return False
    
    jpg_files = [jpg for jpg in os.listdir(lowres_dir) if jpg.endswith(".jpg")]
    logger.info("Found {} .jpg files".format(len(jpg_files)))

    if rois != None:
        section_names = [s.split(".")[0].split("_")[-1] for s in jpg_files]
        if rois == section_names:
            logger.info("ROIs from ROI file match lowres sections")
        else:
            logger.warning("ROIs from ROI file DO NOT MATCH lowres sections")
            return False
            # add code to say where mismatch is

    # check if .json exists (or other alignment files)

def check_hires(project_dir, logger, rois=None):

    logger.info("Checking integrity of HIRES folder...")

    hires_dir = os.path.join(project_dir, "hires")
    if not os.path.exists(hires_dir):
        logger.warning("No hires folder exists in {}".format(project_dir))
        return False
    
    chans = [folder for folder in os.listdir(hires_dir) if "chan" in folder]

    for chan in chans:
        chan_dir = os.path.join(hires_dir, chan)
        png_files = [png for png in os.listdir(chan_dir) if (png.endswith(".png")) and ("masks" not in png)] # need to ensure only pngs pre-cellpose
        if len(png_files) == 0:
            logger.warning("No PNGs found in {}".format(chan_dir))
            return False
        else:
            logger.info("Found {} .png files".format(len(png_files)))
            section_names = [s.split(".")[0].split("_")[-1] for s in png_files]
            if rois != None:
                print(rois)
                print(section_names)
                if rois == section_names:
                    logger.info("ROIs from ROI file match hires sections in {}".format(chan_dir))
                    return True
                else:
                    logger.warning("ROIs from ROI file DO NOT MATCH hires sections in {}".format(chan_dir))
                    return False

    # jpg_files = [jpg for jpg in os.listdir(lowres_dir) if jpg.endswith(".jpg")]
    # logger.info("Found {} .jpg files".format(len(jpg_files)))

    # look for pngs, if none alert and move on, if some check that all exist
    # look for cellpose output

def check_masks(project_dir, logger, rois=None):

    logger.info("Checking whether PNG masks exist...")

    hires_dir = os.path.join(project_dir, "hires")
    if not os.path.exists(hires_dir):
        logger.warning("No hires folder exists in {}".format(project_dir))
        return False
    
    chans = [folder for folder in os.listdir(hires_dir) if "chan" in folder]

    for chan in chans:
        chan_dir = os.path.join(hires_dir, chan)
        png_files = [png for png in os.listdir(chan_dir) if (png.endswith(".png")) and ("masks" in png)] # need to ensure only masks files
        if len(png_files) == 0:
            logger.warning("No mask files found in {}".format(chan_dir))
            return False
        else:
            logger.info("Found {} .png files".format(len(png_files)))
            section_names = [s.split(".")[0].split("_")[-3] for s in png_files]
            print(section_names)
            if rois != None:
                print("The rois are", rois)
                print(section_names)
                if rois == section_names:
                    logger.info("ROIs from ROI file match mask files in {}".format(chan_dir))
                    return True
                else:
                    logger.warning("ROIs from ROI file DO NOT MATCH mask files in {}".format(chan_dir))
                    return False

if __name__ == "__main__":
    project_dir = "D:\\TestData\\fostrap\\FTIG\\FT108"
    project_dir = "/mnt/d/TestData/fostrap/FTIG/FT106"
    project_dir = "/data/FTIG/FT106"

    logger = setup_logger(project_dir)

    rois = check_rawdata(project_dir, logger)

    print(rois)

    if rois != None:
        check_lowres(project_dir, logger, rois=rois)
        check_hires(project_dir, logger, rois=rois)
        check_masks(project_dir, logger, rois=rois)
    else:
        check_lowres(project_dir, logger)
        check_hires(project_dir, logger)
        check_masks(project_dir, logger)

    






## 