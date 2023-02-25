# script to run for batch exporting hires tiff files

import sys
import getopt
import os
import json
import numpy as np

from time import perf_counter

import pyclesperanto_prototype as cle
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte

from helper_fx import *

sys.path.append("~/Github/fosquant/")

device = cle.select_device("Tesla")
print("Used GPU: ", device)

tic = perf_counter()

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["overwrite"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:ojpt")
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
        elif opt in ("-j", "--save_jpg"):
            args_dict["save_jpg"] = True
        elif opt in ("-p", "--save_png"):
            args_dict["save_png"] = True
        elif opt in ("-t", "--save_tif"):
            args_dict["save_tif"] = True
        
    print("Arguments parsed successfully")
    
    return args_dict

def edf(tif, channel):    

    image = tif[:,:,:,channel]
    print(image.shape)

    result_image = None
    test_image = cle.push(image)
    result_image = cle.extended_depth_of_focus_variance_projection(test_image, result_image, radius_x=2, radius_y=2, sigma=10)

    return cle.pull(result_image)

f = open("../config_hires.json")
config_data = json.load(f)
args_dict = parse_args(sys.argv, config_data)

folder = args_dict["project_dir"]
logger = setup_logger(folder)
os.chdir(folder)

if not (args_dict["save_jpg"]) and (args_dict["save_png"]) and (args_dict["save_tif"]):
    print("No saved files requested. Select one format to save. Exiting.")
    sys.exit(2)

if len(args_dict["channels"]) < 1:
    print("No channels provided for analysis. Exiting.")
    sys.exit(2)

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
    
    if "hires" not in os.listdir("."):
        logger.info("No hires folder for {}. Nothing to operate on. Try exporting hires tifs first.".format(animal))
        continue

    os.chdir(os.path.join(".", "hires", "raw_tifs"))

    tifs = [tif for tif in os.listdir(".") if tif.endswith(".tif")]
    logger.info("Found {} .tif files".format(len(tifs)))

    for tif_file in tifs:
        print(tif_file)
        stub = tif_file.split(".")[0]

        tif = np.asarray(imread(tif_file))

        channel_strings = args_dict["channels"].split()
        for chan in channel_strings:

            chan_path = os.path.join("..", "chan{}".format(chan))
            if not os.path.isdir(chan_path):
                os.mkdir(chan_path)
            else:
                if not check_existing_files(chan_path, args_dict["overwrite"]):
                    print("exiting")

            logger.info("Using extended depth of focus to process {} for channel {}".format(tif_file, chan))
            result = edf(tif, int(chan))

            np.save(os.path.join(chan_path, stub+".npy"), result)

            result *= 255.0/result.max() 

            # result_image = np.interp(result_image, (result_image.min(), result_image.max()), (0, 255))

            print(type(result))

            if args_dict["save_jpg"]:
                imsave(os.path.join(chan_path, stub+".jpg"), result)
                print("Saving jpg")
            
            if args_dict["save_png"]:
                imsave(os.path.join(chan_path, stub+".png"), result)
                print("Saving png")

            if args_dict["save_tif"]:
                imsave(os.path.join(chan_path, stub+".tif"), result)
                print("Saving tif")

toc = perf_counter()

logger.info("Finished in {:.4f} sec.".format(toc-tic))




