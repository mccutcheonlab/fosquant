# script to run for batch exporting lowres files

import sys
import getopt
import os
import subprocess
import json

from helper_fx import *

sys.path.append("~/Github/fosquant/")
path_to_macro = os.path.join(os.getcwd(), "export_lowres_batch.ijm" )
subprocess.call("cp {} ~/Fiji.app/macros/".format(path_to_macro), shell=True)

# get and parse options
def parse_args(argv, config_data):
    args_dict = {}
    args_dict["animals"] = ""
    args_dict["project_dir"] = config_data["project_dir"]
    args_dict["channels"] = config_data["channels"]
    args_dict["series"] = config_data["series_lowres"] 
    args_dict["rotate"] = config_data["rotate"]
    args_dict["invert"] = config_data["invert"] 

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:s:r:i")
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
        elif opt in ("-s", "--series"):
            args_dict["series"] = arg
        elif opt in ("-r", "--rotate"):
            args_dict["rotate"] = arg
        elif opt in ("-i", "--invert"):
            args_dict["invert"] = True
        
    print("Arguments parsed successfully")
    
    return args_dict

f = open("../config_lowres.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

print(config_data)
print(args_dict)

folder = config_data["project_dir"]
logger = setup_logger(args_dict["project_dir"])
os.chdir(folder)

if args_dict["animals"] == "all":
    args_dict["animals"] = [d for d in os.listdir(folder) if config_data["prefix"] in d]
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
        logger.info("No folder corresponds to {}. Nothing to transfer.".format(animal))
        continue
    
    if "rawdata" not in os.listdir("."):
        logger.info("No raw data folder for {}. Nothing to transfer.".format(animal))
        continue

    os.chdir(os.path.join(".", "rawdata"))

    vsi_files = [vsi for vsi in os.listdir(".") if vsi.endswith(".vsi")]
    print(vsi_files)

    for vsi in vsi_files:
        stub = vsi.split(".")[0]
        rois = stub + "_ROIs.zip"
        channel = args_dict["channels"] 
        rotate = args_dict["rotate"] 
        series = args_dict["series"]
        if args_dict["invert"]:
            invert = "invertOn"
        else:
            invert = "invertOff"

        subprocess.call("{} -macro export_lowres_batch.ijm '{}, {}, {}, {}, {}, {}' ".format(config_data["path_to_imagej"], vsi, rois, series, channel, rotate, invert ), shell=True)
    # if "rawdata" not in os.listdir("."):
    #     logger.info("No raw data folder for {}. Nothing to transfer.".format(animal))
    #     continue
    
    
#     path_to_azcopy = config_data["path_to_azcopy"]
#     lowres_local = os.path.join(".", "lowres")
#     lowres_remote = os.path.join(config_data["remote_lowres"], animal)

#     logger.info("Transferring lowres files from VM to Azure for {}".format(animal))
#     subprocess.call("{} cp {} {} --recursive=true".format(path_to_azcopy, lowres_local, lowres_remote), shell=True)