import sys
import getopt
import os
import subprocess
import json
import numpy as np

from time import perf_counter

from helper_fx import *
from check_integrity import check_hires

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["overwrite"] = False
    args_dict["skip_integrity_check"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:oi")
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
        elif opt in ("-o", "--overwrite"):
            args_dict["overwrite"] = True
        elif opt in ("-i", "--check_integrity"):
            args_dict["skip_integrity_check"] = True 

    print("Arguments parsed successfully")
    
    return args_dict

f = open("../config_cellpose.json")
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
    
    if "hires" not in os.listdir("."):
        logger.info("No hires data folder for {}. Nothing to export.".format(animal))
        continue

    os.chdir(os.path.join(".", "hires"))

    channel_strings = args_dict["channels"].split()
    for chan in channel_strings:
        print(chan)
        if args_dict["skip_integrity_check"] == False:
            rois = get_rois(os.path.join(folder, animal, "rawdata"))
            if check_hires(os.path.join(folder, animal), logger, rois=rois):
                logger.info("Integrity check of HIRES folder is passed. Continuing with cellpose")
            else:
                print("failed")
                continue
        
        chan_path = os.path.join(folder, animal, "hires", "chan{}".format(chan))
        model = os.path.join(folder, "models", args_dict["model_chan{}".format(chan)])
        diameter = args_dict["diameter_chan{}".format(chan)]

        mask_files = [f for f in os.listdir(chan_path) if "cp_masks" in f]
        if len(mask_files) > 0:
            logger.info("Mask files detected in output folder. Exiting.")
            continue

        cellpose_template_string = "python -m cellpose --dir {} --pretrained_model {} --chan 0 --chan2 0 --diameter {} --verbose --use_gpu --save_png --fast_mode --no_npy --batch_size 8"
        subprocess.call(cellpose_template_string.format(chan_path, model, diameter), shell=True)
        # print(cellpose_template_string.format(chan_path, model, diameter))

        # p = []
        # p.append("cellpose ")

        # basically assemble big list of subprocess commands for all animals/channels and then pass list to separate function for threading
        

# python -m cellpose --dir . --pretrained_model cyto --chan 1 --chan2 0 --diameter 10 --verbose --use_gpu --save_png --fast_mode

# https://stackoverflow.com/questions/2629680/deciding-among-subprocess-multiprocessing-and-thread-in-python
# https://stackoverflow.com/questions/30686295/how-do-i-run-multiple-subprocesses-in-parallel-and-wait-for-them-to-finish-in-py
# https://pypi.org/project/psutil/
