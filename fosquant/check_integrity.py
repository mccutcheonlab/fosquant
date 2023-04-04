import os
import collections
from read_roi import read_roi_zip
from helper_fx import setup_logger, flatten_list

class Check():
    def __init__(self, folder, logger):
        self.folder = folder
        self.logger = logger
        self.verbose = False

        self.rawdata_dir = os.path.join(self.folder, "rawdata")
        self.lowres_dir = os.path.join(self.folder, "lowres")
        self.hires_dir = os.path.join(self.folder, "hires")

    def set_verbose(self):
        self.verbose=True

    def check_rawdata(self):

        if self.verbose: self.logger.info("Checking integrity of RAWDATA folder...")

        if not os.path.exists(self.rawdata_dir):
            self.logger.warning("No rawdata folder exists in {}".format(self.folder))
            return False

        self.vsi_files = [vsi for vsi in os.listdir(self.rawdata_dir) if vsi.endswith(".vsi")]
        if len(self.vsi_files) == 0:
            self.logger.warning("No .vsi files found in rawdata for {}".format(self.folder))
            return False

        if self.verbose: self.logger.info("Found {} .vsi files".format(len(self.vsi_files)))

        for vsi in self.vsi_files:
            scanfolder = "_{}_".format(vsi.split(".")[0])
            if scanfolder not in os.listdir(self.rawdata_dir):
                self.logger.warning("No matching vsi data folder found for {}".format(vsi))
                return False
            else:
                if self.verbose: self.logger.info("Matching vsi data folder found for {}".format(vsi))

        return True

    def get_section_rois(self):

        if self.verbose: self.logger.info("Collecting ROI files from rawdata folder...")

        self.rois = []
        self.roifiles = [f for f in os.listdir(self.rawdata_dir) if "_ROIs.zip" in f]

        if len(self.roifiles) == 0:
            self.logger.warning("No ROI files found in rawdata for {}".format(self.folder))
            return False
        
        for roifile in self.roifiles:
            try:
                temp_roidata = read_roi_zip(os.path.join(self.rawdata_dir, roifile))
            except:
                self.logger.warning("{} may not be a zipfile".format(roifile))
                continue
            
            self.rois.append(list(temp_roidata.keys()))
            
        self.rois = [roi.replace("_", "") for roi in flatten_list(self.rois)]
        if self.verbose: self.logger.info("{} ROIs found for {}".format(len(self.rois), self.folder))
        
        return True

    def check_vsi_rois(self):

        if self.verbose: self.logger.info("Checking whether ROIs match .vsi files...")

        if not self.get_section_rois():
            return False
        
        if not hasattr(self, "vsi_files"):
            if not self.check_rawdata():
                return False
        
        for vsi in self.vsi_files:
            expected_roifile = "{}_ROIs.zip".format(vsi.split(".")[0])
            if expected_roifile not in self.roifiles:
                self.logger.warning("No ROI zip file found for {}".format(vsi))
                return False
            else:
                if self.verbose: self.logger.info("Matching ROI zip file found for {}".format(vsi))
        
        return True

    def check_lowres(self):

        if self.verbose: self.logger.info("Checking integrity of LOWRES folder...")

        if not os.path.exists(self.lowres_dir):
            self.logger.warning("No lowres folder exists in {}".format(project_dir))
            return False
        
        self.jpg_files = [jpg for jpg in os.listdir(self.lowres_dir) if jpg.endswith(".jpg")]
        if len(self.jpg_files) == 0:
            self.logger.warning("No .jpgs found in lowres for {}".format(self.folder))
            return False
        
        if self.verbose: self.logger.info("Found {} .jpg files".format(len(self.jpg_files)))

        if hasattr(self, "rois"):
            section_names = [s.split(".")[0].split("_")[-1] for s in self.jpg_files]
            if self.rois.sort() == section_names.sort():
                if self.verbose: self.logger.info("All ROIs detected match lowres sections")
                return True
            else:
                self.logger.warning("ROIs from ROI file DO NOT MATCH lowres sections")
                return False
                # add code to say where mismatch is
        else:
            self.logger.warning("No ROIs found to match")

        # check if .json exists (or other alignment files)

    def check_hires(self):

        if self.verbose: self.logger.info("Checking integrity of HIRES folder for {}".format(self.folder))

        if not hasattr(self, "chans"):
            if not self.get_chans(): return False

        for chan in self.chans:
            chan_dir = os.path.join(self.hires_dir, chan)
            self.png_files = [png for png in os.listdir(chan_dir) if (png.endswith(".png")) and ("masks" not in png)] # need to ensure only pngs pre-cellpose
            if len(self.png_files) == 0:
                self.logger.warning("No PNGs found in {}".format(chan_dir))
                return False

            if self.verbose: self.logger.info("Found {} .png files".format(len(self.png_files)))
            section_names = [s.split(".")[0].split("_")[-1] for s in self.png_files]

            if not hasattr(self, "rois"):
                if not self.get_section_rois():
                    self.logger.warning("No section ROIs available for {}".format(self.folder))
                    return False

            #TODO make separate function to check rois to section names and remove print statements
            if collections.Counter(self.rois) == collections.Counter(section_names):
                if self.verbose:
                    self.logger.info("ROIs from ROI file match hires sections in {}".format(chan_dir))
            else:
                self.logger.warning("ROIs from ROI file DO NOT MATCH hires sections in {}".format(chan_dir))
                return False
        
        return True

    def check_masks(self):

        self.logger.info("Checking whether PNG masks exist for {}".format(self.folder))

        if not hasattr(self, "chans"):
            if not self.get_chans(): return False

        for chan in self.chans:
            chan_dir = os.path.join(self.hires_dir, chan)
            self.mask_files = [png for png in os.listdir(chan_dir) if (png.endswith(".png")) and ("masks" in png)] # need to ensure only masks files
            if len(self.mask_files) == 0:
                self.logger.warning("No mask files found in {}".format(chan_dir))
                return False

            if self.verbose: self.logger.info("Found {} .png files".format(len(self.mask_files)))
            section_names = [s.split(".")[0].split("_")[-3] for s in self.mask_files]
            print(section_names)

            if not hasattr(self, "rois"):
                if not self.get_section_rois():
                    self.logger.warning("No section ROIs available for {}".format(self.folder))
                    return False

            if collections.Counter(self.rois) == collections.Counter(section_names):
                if self.verbose: self.logger.info("ROIs from ROI file match mask files in {}".format(chan_dir))
            else:
                self.logger.warning("ROIs from ROI file DO NOT MATCH mask files in {}".format(chan_dir))
                return False
            
        return True

    def get_chans(self):
        
        if not os.path.exists(self.hires_dir):
            self.logger.warning("No hires folder exists in {}".format(self.folder))
            return False
        
        self.chans = [folder for folder in os.listdir(self.hires_dir) if "chan" in folder]

        if len(self.chans) == 0:
            self.logger.warning("No channel folders found in {}".format(self.hires_dir))
            return False
        
        return True

    def check_user_rois(self):
        
        self.logger.info("Checking whether user-defined ROI file exists for {}".format(self.folder))

        if not os.path.exists(self.lowres_dir):
            self.logger.warning("No lowres folder exists in {}".format(self.folder))
            return False
        
        self.user_roi_files = [f for f in os.listdir(self.lowres_dir) if "ROIs.zip" in f]
        if len(self.user_roi_files) > 0:
            return True
        else:
            self.logger.warning("No User-defined ROI files in {}".format(self.lowres_dir))
            return False
        
    def check_all(self):
        if not self.check_rawdata(): return False
        if not self.check_vsi_rois(): return False
        if not self.check_lowres(): return False
        if not self.check_hires(): return False
        if not self.check_masks(): return False
        if not self.check_user_rois(): return False
        self.logger.info("All integrity checks passed for {}".format(self.folder))
        return True

if __name__ == "__main__":
    project_dir = "D:\\TestData\\fostrap\\FTIG\\FT108"
    project_dir = "/mnt/d/TestData/fostrap/FTIG/FT108"
    # project_dir = "/data/FTIG/FT106"

    logger = setup_logger(project_dir)

    check = Check(project_dir, logger)
    # check.set_verbose()
    # print(check.check_rawdata())
    # print(check.check_vsi_rois())
    # # print(check.get_section_rois())
    # print(check.check_lowres())
    print(check.check_hires())
    # print(check.check_masks())
    # print(check.check_user_rois())

    # print(check.check_all())
    

    
