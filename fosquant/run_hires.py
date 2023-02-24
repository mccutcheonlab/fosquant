# script to run for batch exporting hires tiff files

import sys
import getopt
import os
import subprocess
import json

from subprocess import PIPE, run


from time import perf_counter

from helper_fx import *

sys.path.append("~/Github/fosquant/")
path_to_macro = os.path.join(os.getcwd(), "export_hires_batch.ijm" )
subprocess.call("cp {} ~/Fiji.app/macros/".format(path_to_macro), shell=True)

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "a:r:")
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
        
    print("Arguments parsed successfully")
    
    return args_dict

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

logger.info("Finished.")




