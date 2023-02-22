# script to run for batch exporting hires files

import sys
import getopt
import os
import subprocess
import json

from helper_fx import *

sys.path.append("~/Github/fosquant/")
path_to_macro = os.path.join(os.getcwd(), "export_hires_batch.ijm" )
subprocess.call("cp {} ~/Fiji.app/macros/".format(path_to_macro), shell=True)

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    # args_dict["project_dir"] = config_data["project_dir"]
    # args_dict["series_rois"] = config_data["series_rois"]
    # args_dict["series_hires"] = config_data["hires"]
    # args_dict["rotate"] = config_data["rotate"]
    # args_dict["save_jpg"] = config_data["save_jpg"]
    # args_dict["save_png"] = config_data["save_png"]
    # args_dict["save_tif"] = config_data["save_tif"]

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:jpt")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        elif opt in ("-c", "--channels"):
            args_dict["channels"] = arg
        elif opt in ("-r", "--rotate"):
            args_dict["rotate"] = arg
        elif opt in ("-j", "--save_jpg"):
            args_dict["save_jpg"] = True
        elif opt in ("-p", "--save_png"):
            args_dict["save_png"] = True
        elif opt in ("-t", "--save_tif"):
            args_dict["save_tif"] = True
        
    print("Arguments parsed successfully")
    
    return args_dict

f = open("../config_hires.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

folder = args_dict["project_dir"]
logger = setup_logger(folder)
os.chdir(folder)

if not (args_dict["save_jpg"]) and (args_dict["save_png"]) and (args_dict["save_tif"]):
    print("No saved files requested. Select one format to save. Exiting.")
    sys.exit(2)

if len(args_dict["channels"]) > 0:
    channel_strings = args_dict["channels"].split()
    if "1" in channel_strings:
        args_dict["chan1"] = True
    if "2" in channel_strings:
        args_dict["chan2"] = True
    if "3" in channel_strings:
        args_dict["chan3"] = True

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
        stub = vsi.split(".")[0]
        vsipath = os.path.join(os.getcwd(), vsi)
        rois = os.path.join(os.getcwd(), stub + "_ROIs.zip")
        series_rois = args_dict["series_rois"]
        series_hires = args_dict["series_hires"]
        c1 = int(args_dict["chan1"])
        c2 = int(args_dict["chan2"])
        c3 = int(args_dict["chan3"])
        rotate = args_dict["rotate"]
        jpg = args_dict["save_jpg"]
        png = args_dict["save_png"]
        tif = args_dict["save_tif"]

        logger.info("Opening ImageJ to process {}".format(vsi))
        subprocess.call("{} -macro export_hires_batch.ijm '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}' \
                         ".format(args_dict["path_to_imagej"], vsipath, rois, series_rois, series_hires, c1, c2, c3, rotate, jpg, png, tif), shell=True)
 

    #     #subprocess.call("{} -macro export_hires_batch.ijm '{}, {}, {}, {}, {}, {}' -batch".format(config_data["path_to_imagej"], vsipath, rois, series, channel, rotate, invert ), shell=True)
 
logger.info("Finished.")




