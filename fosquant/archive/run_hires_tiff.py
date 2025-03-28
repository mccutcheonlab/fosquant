# script to run for batch exporting hires tiff files

import sys
import getopt
import os
from pathlib import Path
import subprocess
import json
import numpy as np

import tifffile as tiff

from time import perf_counter

# import pyclesperanto_prototype as cle
from skimage.io import imread, imsave
from skimage.util import img_as_uint

from helper_fx import *
from check_integrity import Check

sys.path.append("~/Github/fosquant/")

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["sections"] = ""
    args_dict["overwrite"] = False
    args_dict["delete_intermediates"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:s:r:ox")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        elif opt in ("-r", "--rotate"):
            args_dict["rotate"] = arg
        elif opt in ("-c", "--channels"):
            args_dict["channels"] = arg
        elif opt in ("-s", "--sections"):
            args_dict["sections"] = arg
        elif opt in ("-o", "--overwrite"):
            args_dict["overwrite"] = True 
        elif opt in ("-x", "--delete-intermediates"):
            args_dict["delete_intermediates"] = True 

    print("Arguments parsed successfully")
    
    return args_dict

def read_and_crop_tiff(path, crop_x, crop_y, crop_width, crop_height):
    with tiff.TiffFile(path) as tif:
        image = tif.asarray()
        cropped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
        return cropped_image

def get_section_from_tif(path, dims, chan, series_hires=8):

    print("dims are", dims)

    crop_x, crop_y, crop_width, crop_height = dims

    try:
        img = read_and_crop_tiff(path, crop_x, crop_y, crop_width, crop_height)
    except:
        print("Error reading tiff file!!!!!!!!!!!!!!!!!!!!!!!!!")
        sys.exit(2)

    return img

f = open(Path("../config_hires.json"))
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

folder = Path(args_dict["project_dir"])
logger = setup_logger(folder)
os.chdir(folder)

if args_dict["animals"] == "all":
    args_dict["animals"] = [d for d in os.listdir(folder) if args_dict["prefix"] in d]
elif args_dict["animals"] == "":
    logger.info("No animals given. Exiting")
    sys.exit(2)
else:
    args_dict["animals"] = args_dict["animals"].split()

print(args_dict["animals"])

for animal in args_dict["animals"]:
    print(folder)
    try:
        os.chdir(os.path.join(folder, animal))
    except FileNotFoundError:
        logger.info("No folder corresponds to {}. Nothing to export.".format(animal))
        continue
    
    if "rawdata" not in os.listdir("."):
        logger.info("No raw data folder for {}. Nothing to export.".format(animal))
        continue

    os.chdir(os.path.join(".", "rawdata"))

    tif_files = [tif for tif in os.listdir(".") if (tif.endswith(".tif") and "edited" in tif)]
    logger.info("Found {} .tif files".format(len(tif_files)))

    check = Check(os.path.join(folder, animal), logger)
    if check.check_hires():
        logger.info("All hires images detected for {}. Continuing to next".format(animal))
        continue

    if len(tif_files) > 0:
        temp_folder = Path("/data_temp/{}".format(animal))
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            subprocess.call("cp .. {} -r".format(temp_folder), shell=True)
        os.chdir(temp_folder)
    else:
        print("No .tif files. Exiting.")
        sys.exit(2)

    for tif in tif_files:
        print(tif)
        tic = perf_counter()
        stub = tif.split(".")[0]
        logger.info("{}".format(os.getcwd()))
        tifpath = Path(os.getcwd()) / "rawdata" / tif
        roipath = Path(os.getcwd()) / "rawdata" / "{}_ROIs.zip".format(stub)
        # rotate = args_dict["rotate"]

        logger.info("Using TIFFfile to process {}".format(tif))

        rois = get_scaled_roi(roipath, scale_factor=1)

        for roi, dims in rois.items():
            roi_tic = perf_counter()
            chan=1
            chan_path = Path(os.getcwd()) / "hires" / "chan{}".format(chan)
            if not os.path.exists(chan_path):
                os.makedirs(chan_path)
            
            logger.info("looking for {}".format(os.path.join(chan_path, stub + roi + ".png")))
            if os.path.exists(os.path.join(chan_path, stub + roi + ".png")):
                print("Should skip here...")
                if args_dict["overwrite"] == False:
                    logger.info("PNG file already exists for {}, channel {}".format(stub, chan))
                    continue
            else:
                print("File not detected")
            try:
                im = get_section_from_tif(tifpath, dims, chan)
            except:
                logger.warning("Could not process {} for channel {}".format(roi, chan))
                continue

            # result = np.rot90(im, 2)

            imsave(chan_path / "{}_{}.png".format(stub,roi), im)
            logger.info("Saving 16-bit .png to {}".format(chan_path))

            f = "{}_{}.png".format(stub,roi)
            output_folder = Path(folder / animal / "hires" / "chan{}".format(chan))
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            subprocess.call("cp {} {}".format(str(chan_path / f), str(output_folder)), shell=True)
                
            roi_toc = perf_counter()
            print("Section {} took {} sec".format(roi, roi_toc-roi_tic))

        toc = perf_counter()
        logger.info("Processed {} in {:0.4f} sec".format(tif, toc-tic))

    if args_dict["delete_intermediates"]:
        subprocess.call("rm /data_temp/{} -r".format(animal), shell=True)
        subprocess.call("trash-empty", shell=True)

logger.info("Finished.")




