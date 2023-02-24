# script to run for batch exporting hires tiff files

import sys
import getopt
import os
import subprocess
import json
import numpy as np

import pyclesperanto_prototype as cle
from skimage.io import imread, imsave

from helper_fx import *

sys.path.append("~/Github/fosquant/")
path_to_macro = os.path.join(os.getcwd(), "export_hires_batch.ijm" )
subprocess.call("cp {} ~/Fiji.app/macros/".format(path_to_macro), shell=True)

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""

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
        elif opt in ("-j", "--save_jpg"):
            args_dict["save_jpg"] = True
        elif opt in ("-p", "--save_png"):
            args_dict["save_png"] = True
        elif opt in ("-t", "--save_tif"):
            args_dict["save_tif"] = True
        
    print("Arguments parsed successfully")
    
    return args_dict

def edf(image, channel, path):    

    # initialize GPU
    device = cle.select_device("Quadro")
    print("Used GPU: ", device)

    image = np.asarray(imread("..//data//channel3.tif"))

    image = image[:,:,:,channel]
    print(image.shape)

    result_image = None
    test_image = cle.push(image)
    result_image = cle.extended_depth_of_focus_variance_projection(test_image, result_image, radius_x=2, radius_y=2, sigma=10)

    # cle.imshow(result_image)
    # imsave(path, result_image)

    return result_image

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

    for tif in tifs:
        print(tif)
        stub = tif.split(".")[0]



        
        channel_strings = args_dict["channels"].split()
        for chan in channel_strings:
            print(chan)
            # make folder if needed
            # check overwrite

            logger.info("Using extended depth of focus to process {} for channel {}".format(tif, chan))

            result_image = edf(os.path.join(".", tif), int(chan))

            # save as necessary
                
            


        # if "1" in channel_strings:
        #     args_dict["chan1"] = True
        # if "2" in channel_strings:
        #     args_dict["chan2"] = True
        # if "3" in channel_strings:
        #     args_dict["chan3"] = True


        # c1 = int(args_dict["chan1"])
        # c2 = int(args_dict["chan2"])
        # c3 = int(args_dict["chan3"])

        # jpg = args_dict["save_jpg"]
        # png = args_dict["save_png"]
        # tif = args_dict["save_tif"]

        # logger.info("Opening ImageJ to process {}".format(vsi))

logger.info("Finished.")




