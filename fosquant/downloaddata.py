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
    args_dict["project_dir"] = config_data["path_to_project_dir"]
    args_dict["metafile"] = False
    args_dict["animals"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "hma:")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-m", "--get_metafile"):
            args_dict["metafile"] = True
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        
    print("Arguments parsed successfully")
    
    return args_dict

f = open("../config.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

logdir = os.path.join(args_dict["project_dir"], "log")
if not os.path.isdir(logdir):
    os.mkdir(logdir)

## setting up logger
logfile = os.path.join(args_dict["project_dir"], "log", "{}.log".format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))

logger = logging.getLogger(logfile)
logger.setLevel(level=logging.DEBUG)

logStreamFormatter = logging.Formatter(
  fmt=f"%(levelname)-8s %(asctime)s \t line %(lineno)s - %(message)s", 
  datefmt="%H:%M:%S"
)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logStreamFormatter)
consoleHandler.setLevel(level=logging.DEBUG)

logger.addHandler(consoleHandler)

logFileFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s L%(lineno)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(filename=logfile)
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.DEBUG)

logger.addHandler(fileHandler)

logger.info("Created log file at {}".format(logfile))

if args_dict["metafile"]:
    logger.info("Downloading metafile from remote repo")
    path_to_azcopy = config_data["path_to_azcopy"]
    subprocess.call("{} cp {} {}".format(path_to_azcopy, config_data["metafile"], args_dict["project_dir"]), shell=True)


csv_file = os.path.join(args_dict["project_dir"], os.path.basename(config_data["metafile"]))
logger.info("Reading CSV file... {}".format(csv_file))
if not os.path.exists(csv_file):
    logger.info("CSV file cannot be found. Exiting.")
    sys.exit(2)

df = pd.read_csv(csv_file)
# print(df.head())

if args_dict["animals"] == "all":
    args_dict["animals"] = df["animal"].unique()
elif args_dict["animals"] == "":
    logger.info("No animals given. Exiting")
    sys.exit(2)
else:
    args_dict["animals"] = args_dict["animals"].split()

