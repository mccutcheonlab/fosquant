# script to run for batch exporting lowres files

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
    args_dict["invert"] = config_data["invert"] 

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:i")
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
        elif opt in ("-i", "--invert"):
            args_dict["invert"] = True
        
    print("Arguments parsed successfully")
    
    return args_dict

f = open("../config_hires.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

print(config_data)
print(args_dict)


folder = config_data["path_to_project_dir"]