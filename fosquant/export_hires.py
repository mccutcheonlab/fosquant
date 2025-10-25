import sys
import getopt
import os
from pathlib import Path
import subprocess
import json
import numpy as np

from time import perf_counter

from skimage.io import imread, imsave
from skimage.util import img_as_uint

from helper_fx import *
from check_integrity import Check

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["sections"] = ""
    args_dict["overwrite"] = False
    args_dict["delete_intermediates"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:s:r:ox")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        elif opt in ("-r", "--rotate"):
            args_dict["rotate"] = arg
        elif opt in ("-c", "--channels"):
            args_dict["channels"] = arg
        elif opt in ("-s", "--sections"):
            args_dict["sections"] = arg
        elif opt in ("-o", "--overwrite"):
            args_dict["overwrite"] = True 
        elif opt in ("-x", "--delete-intermediates"):
            args_dict["delete_intermediates"] = True 

    print("Arguments parsed successfully")
    
    return args_dict

def get_section_from_tif(path, dims, chan):

    # dims = check_bounds(path, dims, series_hires)

    # simply read im with imread

    img = imread(path, dims)

    print("dims are", dims)

    with bf.ImageReader(path) as reader:
        planes = []
        for z in range(3):
            im = reader.read(c=chan, z=z, series=series_hires, XYWH=dims)
            planes.append(im)

    img = np.dstack(planes)
    img = img_as_uint(img)

    return img

if __name__ == "__main__":
    f = open("../config_hires.json")
    config_data = json.load(f)
    args_dict = parse_args(sys.argv, config_data)
    use_temp_folder = False

    folder = Path(args_dict["project_dir"])
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

    print(folder)
    for animal in args_dict["animals"]:
        try:
            os.chdir(folder / animal)
        except FileNotFoundError:
            logger.info("No folder corresponds to {}. Nothing to export.".format(animal))
            continue
        
        if "rawdata" not in os.listdir("."):
            logger.info("No rawdata folder for {}. No images to work with.".format(animal))
            continue

        os.chdir(os.path.join(".", "rawdata"))

        tif_files = [tif for tif in os.listdir(".") if tif.endswith("edited.tif")]
        logger.info("Found {} .tif files".format(len(tif_files)))

        check = Check(os.path.join(folder, animal), logger)
        if check.check_hires():
            logger.info("All hires images detected for {}. Continuing to next".format(animal))
            continue
        
        if use_temp_folder:
            if len(tif_files) > 0:
            temp_folder = "/data_temp/{}".format(animal)
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
                subprocess.call("cp .. {} -r".format(temp_folder), shell=True)
                os.chdir(temp_folder)
            else:
                print("No .tif files. Exiting.")
                sys.exit(2)

        for tif in tif_files:
            print(tif)
            tic = perf_counter()
            stub = tif.split(".")[0]
            logger.info("{}".format(os.getcwd()))
            tifpath = Path(os.getcwd()) / "rawdata" / tif
            sectionpath = Path(os.getcwd()) / "rawdata" / stub + "_sections.zip"
            series_rois = args_dict["series_rois"]
            series_hires = args_dict["series_hires"]
            rotate = args_dict["rotate"]

            logger.info("Using python-bioformats to process {}".format(vsi))

            rois = get_scaled_roi(sectionpath)

        for roi, dims in rois.items():
            roi_tic = perf_counter()
            for chan in channel_strings:
                chan_path = os.path.join(os.getcwd(), "hires", "chan{}".format(chan))
                logger.info("looking for {}".format(os.path.join(chan_path, stub + roi + ".png")))
                if os.path.exists(os.path.join(chan_path, stub + roi + ".png")):
                    print("Should skip here...")
                    if args_dict["overwrite"] == False:
                        logger.info("PNG file already exists for {}, channel {}".format(stub, chan))
                        continue
                else:
                    print("File not detected")

                try:
                    im = get_section_from_tif(tifpath, dims, chan)
                except:
                    logger.warning("Could not process {} for channel {}".format(roi, chan))
                    continue

                im = np.rot90(im, 2)

                imsave(os.path.join(chan_path, "{}{}.png".format(stub,roi)), im)
                logger.info("Saving 16-bit .png to {}".format(chan_path))

                f = "{}{}.png".format(stub,roi)
                subprocess.call("cp {} {}".format(os.path.join(chan_path, f), os.path.join(folder, animal, "hires", "chan{}".format(chan))), shell=True)
                
            roi_toc = perf_counter()
            print("Section {} took {} sec".format(roi, roi_toc-roi_tic))

        toc = perf_counter()
        logger.info("Processed {} in {:0.4f} sec".format(tif, toc-tic))

        if args_dict["delete_intermediates"]:
            subprocess.call("rm /data_temp/{} -r".format(animal), shell=True)
            subprocess.call("trash-empty", shell=True)

    logger.info("Finished.")