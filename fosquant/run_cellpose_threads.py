import sys
import getopt
import os
import subprocess
import json
import numpy as np

from time import perf_counter

from helper_fx import *

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["overwrite"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:o")
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

        p = []
        p.append("cellpose ")

        # basically assemble big list of subprocess commands for all animals/channels and then pass list to separate function for threading
        

# python -m cellpose --dir . --pretrained_model cyto --chan 1 --chan2 0 --diameter 10 --verbose --use_gpu --save_png --fast_mode

# https://stackoverflow.com/questions/2629680/deciding-among-subprocess-multiprocessing-and-thread-in-python
# https://stackoverflow.com/questions/30686295/how-do-i-run-multiple-subprocesses-in-parallel-and-wait-for-them-to-finish-in-py
# https://pypi.org/project/psutil/
