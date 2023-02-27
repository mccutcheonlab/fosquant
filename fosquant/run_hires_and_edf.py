# script to run for batch exporting hires tiff files

import sys
import getopt
import os
import subprocess
import json
import numpy as np

from time import perf_counter

import pyclesperanto_prototype as cle
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte

from helper_fx import *

sys.path.append("~/Github/fosquant/")
path_to_macro = os.path.join(os.getcwd(), "export_hires_batch.ijm" )
subprocess.call("cp {} ~/Fiji.app/macros/".format(path_to_macro), shell=True)

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["overwrite"] = False
    args_dict["delete_intermediates"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:ox")
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
        elif opt in ("-o", "--overwrite"):
            args_dict["overwrite"] = True 
        elif opt in ("-x", "--delete-intermediates"):
            args_dict["delete_intermediates"] = True 

    print("Arguments parsed successfully")
    
    return args_dict

def edf(tif, channel):    

    image = tif[:,:,:,channel]
    print(image.shape)

    result_image = None
    test_image = cle.push(image)
    result_image = cle.extended_depth_of_focus_variance_projection(test_image, result_image, radius_x=2, radius_y=2, sigma=10)

    return cle.pull(result_image).astype("uint16")

f = open("../config_hires.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

folder = args_dict["project_dir"]
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

if len(args_dict["channels"]) < 1:
    print("No channels provided for analysis. Exiting.")
    sys.exit(2)

for animal in args_dict["animals"]:
    try:
        os.chdir(os.path.join(folder, animal))
    except FileNotFoundError:
        logger.info("No folder corresponds to {}. Nothing to export.".format(animal))
        continue
    
    if "rawdata" not in os.listdir("."):
        logger.info("No raw data folder for {}. Nothing to export.".format(animal))
        continue

    os.chdir(os.path.join(".", "rawdata"))

    vsi_files = [vsi for vsi in os.listdir(".") if vsi.endswith(".vsi")]
    logger.info("Found {} .vsi files".format(len(vsi_files)))

    if len(vsi_files) > 0:
        temp_folder = "/data_temp/{}/rawdata".format(animal)
        os.makedirs(temp_folder)
        subprocess.call("cp . {} -r".format(temp_folder), shell=True)
        os.chdir(temp_folder)
    else:
        print("No .vsi files. Exiting.")
        sys.exit(2)

    for vsi in vsi_files:
        print(vsi)
        tic = perf_counter()
        stub = vsi.split(".")[0]
        vsipath = os.path.join(os.getcwd(), vsi)
        rois = os.path.join(os.getcwd(), stub + "_ROIs.zip")
        series_rois = args_dict["series_rois"]
        series_hires = args_dict["series_hires"]
        rotate = args_dict["rotate"]

        logger.info("Opening ImageJ to process {}".format(vsi))
        subprocess.call("{} -macro export_hires_batch.ijm '{}, {}, {}, {}, {}' -batch \
                         ".format(args_dict["path_to_imagej"], vsipath, rois, series_rois, series_hires, rotate), shell=True)
        toc = perf_counter()
        logger.info("Processed {} in {:0.4f} sec".format(vsi, toc-tic))

    os.chdir(os.path.join("..", "hires", "raw_tifs"))

    tifs = [tif for tif in os.listdir(".") if tif.endswith(".tif")]
    logger.info("Found {} .tif files".format(len(tifs)))

    for tif_file in tifs:
        print(tif_file)
        stub = tif_file.split(".")[0]

        tif = np.asarray(imread(tif_file))

        channel_strings = args_dict["channels"].split()
        for chan in channel_strings:

            chan_path = os.path.join("..", "chan{}".format(chan))
            if not os.path.isdir(chan_path):
                os.mkdir(chan_path)
            else:
                if not check_existing_files(chan_path, args_dict["overwrite"]):
                    print("exiting")

            logger.info("Using extended depth of focus to process {} for channel {}".format(tif_file, chan))
            result = edf(tif, int(chan))

            imsave(os.path.join(chan_path, stub+".png"), result)
            logger.info("Saving 16-bit .png to {}".format(chan_path))

        target_dir = os.path.join(folder, animal, "hires")
        os.mkdir(target_dir)
        for chan in channel_strings:
            chan_path = os.path.join("..", "chan{}".format(chan))
            subprocess.call("cp {} {} -r".format(chan_path, os.path.join(target_dir, "chan{}".format(chan))))

        if args_dict["delete_intermediates"]:
            subprocess.call("rmdir /data_temp/{} -r".format(animal))

logger.info("Finished.")




