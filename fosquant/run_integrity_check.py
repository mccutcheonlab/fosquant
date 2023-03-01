import sys
import getopt
import os
import json

from time import perf_counter

from check_integrity import *

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "a:f:")
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

tic = perf_counter()

f = open("../config.json")
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

for animal in args_dict["animals"]:
    animal_dir = os.path.join(folder, animal)
    if not os.path.exists(animal_dir):
        logger.warning("No folder exists in priject directory for {}".format(animal))
        continue

    rois = check_rawdata(animal_dir, logger)

    if rois != None:
        check_lowres(animal_dir, logger, rois=rois)
        check_hires(animal_dir, logger, rois=rois)
    else:
        check_lowres(animal_dir, logger)
        check_hires(animal_dir, logger)

toc = perf_counter()

logger.info("Finished running in {:.4f} seconds.".format(toc-tic))



