import sys
import getopt
import os
import subprocess
import json
import numpy as np

from time import perf_counter
from multiprocessing import Pool, cpu_count

from helper_fx import *
from check_integrity import Check

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["overwrite"] = False
    args_dict["skip_integrity_check"] = False
    args_dict["unanalyzed_files_only"] = False
    args_dict["threaded"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:oiut")
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
        elif opt in ("-u", "--unanalyzed_files_only"):
            args_dict["unanalyzed_files_only"] = True
        elif opt in ("-t", "--threaded"):
            args_dict["threaded"] = True

    print("Arguments parsed successfully")
    
    return args_dict

def run_cellpose_on_single_png(png, animal, chan, model, diameter):
    # logger.info("Running cellpose on channel {} in {} for {}".format(chan, png, animal))
    cellpose_template_string = "python -m cellpose --image_path {} --pretrained_model {} --chan 0 --chan2 0 --diameter {} --verbose --use_gpu --save_png --fast_mode --no_npy --batch_size 8".format(png, model, diameter)
    print(cellpose_template_string)
    # subprocess.call(cellpose_template_string.format(os.path.join(chan_path, png), model, diameter), shell=True)

    return

if __name__ == "__main__":
    f = open("../config_cellpose_laptop_for_testing.json")
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

    pngs_to_analyze=[] # collect list of png paths and other info in this variable for looping through in thread

    #TODO Add explicit references to the animal being analysed so visible in the terminal at run-time
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
                check = Check(os.path.join(folder, animal), logger)
                if check.check_hires():
                    logger.info("Integrity check of HIRES folder is passed for {}. Continuing with cellpose".format(animal))
                else:
                    print("failed")
                    continue
            
            chan_path = os.path.join(folder, animal, "hires", "chan{}".format(chan))
            model = os.path.join(folder, "models", args_dict["model_chan{}".format(chan)])
            diameter = args_dict["diameter_chan{}".format(chan)]

            mask_files = [f for f in os.listdir(chan_path) if "cp_masks" in f]
            if (len(mask_files) > 0) and (not args_dict["unanalyzed_files_only"]):
                logger.info("Mask files detected in output folder. Exiting.")
                continue
            
            if args_dict["unanalyzed_files_only"]:
                pngs = [f for f in os.listdir(chan_path) if (f.endswith(".png")) and ("_cp_masks" not in f)]
                orphan_pngs = [png for png in pngs if png.split(".")[0] + "_cp_masks.png" not in os.listdir(chan_path)]

                for png in orphan_pngs:
                    # Add png_path, animal, channel, model, diamter to list, pngs_to_analyze
                    pngs_to_analyze.append((os.path.join(chan_path, png), animal, chan, model, diameter))

                    # logger.info("Running cellpose on channel {} in {} for {}".format(chan, png, animal))
                    # cellpose_template_string = "python -m cellpose --image_path {} --pretrained_model {} --chan 0 --chan2 0 --diameter {} --verbose --use_gpu --save_png --fast_mode --no_npy --batch_size 8"
                    # subprocess.call(cellpose_template_string.format(os.path.join(chan_path, png), model, diameter), shell=True)

            else:
                # Add all png_paths, model, dimater to list, pngs_to_analyze
                pngs = [f for f in os.listdir(chan_path) if (f.endswith(".png")) and ("_cp_masks" not in f)]
                for png in pngs:
                    pngs_to_analyze.append((os.path.join(chan_path, png), animal, chan, model, diameter))
                # logger.info("Running cellpose on all files in {}".format(chan_path))
                # cellpose_template_string = "python -m cellpose --dir {} --pretrained_model {} --chan 0 --chan2 0 --diameter {} --verbose --use_gpu --save_png --fast_mode --no_npy --batch_size 8"
                # subprocess.call(cellpose_template_string.format(chan_path, model, diameter), shell=True)

    print(pngs_to_analyze)

    if len(pngs_to_analyze) > 0:
        if args_dict["threaded"]:
            pool_args = pngs_to_analyze

            # pool_size = cpu_count()
            pool_size = 4
            print("running threaded", type(pool_args[0]), len(pool_args))
            with Pool(processes=pool_size) as pool:
                print(pool)
                temp = pool.starmap(run_cellpose_on_single_png, pool_args)
        else:
            for png in pngs_to_analyze:
                run_cellpose_on_single_png(*png)


# python run_cellpose_threads.py -a FTxxx -c 1 -t -i

# https://stackoverflow.com/questions/2629680/deciding-among-subprocess-multiprocessing-and-thread-in-python
# https://stackoverflow.com/questions/30686295/how-do-i-run-multiple-subprocesses-in-parallel-and-wait-for-them-to-finish-in-py
# https://pypi.org/project/psutil/
