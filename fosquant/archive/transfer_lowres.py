import sys
import getopt
import os
import subprocess
import json

from helper_fx import *

sys.path.append("~/Github/fosquant/")

# get and parse options

def parse_args(argv, config_data):

    arg_help = "python transfer_lowres.py -a <animal names>"

    args_dict = {}
    args_dict["project_dir"] = config_data["path_to_project_dir"]
    args_dict["animals"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "ha:")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        
    print("Arguments parsed successfully")
    
    return args_dict

f = open("../config.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

logger = setup_logger(args_dict["project_dir"])

folder = config_data["path_to_project_dir"]
os.chdir(folder)

if args_dict["animals"] == "all":
    args_dict["animals"] = [d for d in os.listdir(folder) if config_data["prefix"] in d]
elif args_dict["animals"] == "":
    logger.info("No animals given. Exiting")
    sys.exit(2)
else:
    args_dict["animals"] = args_dict["animals"].split()

print(args_dict["animals"])
# work out to or from - merge/sync folders
for animal in args_dict["animals"]:
    try:
        os.chdir(os.path.join(folder, animal))
    except FileNotFoundError:
        logger.info("No folder corresponds to {}. Nothing to transfer.".format(animal))
        continue
    
    if "lowres" not in os.listdir("."):
        logger.info("No lowres folder for {}. Nothing to transfer.".format(animal))
        continue
    
    path_to_azcopy = config_data["path_to_azcopy"]
    lowres_local = os.path.join(".", "lowres")
    lowres_remote = os.path.join(config_data["remote_lowres"], animal)

    logger.info("Transferring lowres files from VM to Azure for {}".format(animal))
    subprocess.call("{} cp {} {} --recursive=true".format(path_to_azcopy, lowres_local, lowres_remote), shell=True)
    




