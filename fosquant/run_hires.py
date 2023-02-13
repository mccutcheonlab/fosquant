# script to run for batch exporting hires files

import sys
import getopt
import os
import subprocess
import json
import logging

from datetime import datetime

import pandas as pd

sys.path.append("~/Github/fosquant/")

# get and parse options
def parse_args(argv, config_data):
    args_dict = {}
    args_dict["animals"] = ""
    args_dict["channels"] = config_data["channels"]
    args_dict["rotate"] = config_data["rotate"]
    args_dict["save_jpg"] = config_data["save_jpg"]
    args_dict["save_png"] = config_data["save_png"]
    args_dict["save_tif"] = config_data["save_tif"]

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

print(config_data)
print(args_dict)


if not (args_dict["save_jpg"]) and (args_dict["save_png"]) and (args_dict["save_tif"]):
    print("No saved files requested. Select one format to save. Exiting.")

folder = config_data["path_to_data"]

if args_dict["animals"] == "all":
    aaa = [d for d in os.path.isdir(os.listdir(folder)) if "rawdata" in os.listdir(os.path.join(folder, d))]
    # aaa = [d for d in os.listdir(folder)]
    print(aaa)
    # args_dict["animals"] = df["animal"].unique()
# elif args_dict["animals"] == "":
#     logger.info("No animals given. Exiting")
#     sys.exit(2)
# else:
#     args_dict["animals"] = args_dict["animals"].split()



# os.listdir(folder)


# for animal in args_dict["animals"]:
#     print(animal)

#os.chdir(folder, )

# subprocess.call("{} -macro split_2p_tiff.ijm '{}, {}, {}, {}, {}' -batch ".format(path_to_imagej, imaging_file_local, ses_ij_path, proj, chunks, z), shell=True)
