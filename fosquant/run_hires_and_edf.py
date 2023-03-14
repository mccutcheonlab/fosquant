# script to run for batch exporting hires tiff files

import sys
import getopt
import os
import subprocess
import json
import numpy as np

from time import perf_counter

import pyclesperanto_prototype as cle
from skimage.io import imread, imsave
from skimage.util import img_as_uint

from helper_fx import *
from check_integrity import Check

import javabridge
import bioformats as bf


javabridge.start_vm(class_path=bf.JARS)

# myloglevel="ERROR"
# rootLoggerName = javabridge.get_static_field("org/slf4j/Logger","ROOT_LOGGER_NAME", "Ljava/lang/String;")
# rootLogger = javabridge.static_call("org/slf4j/LoggerFactory","getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
# logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level",myloglevel, "Lch/qos/logback/classic/Level;")

sys.path.append("~/Github/fosquant/")

# get and parse options
def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["channels"] = ""
    args_dict["overwrite"] = False
    args_dict["delete_intermediates"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:c:r:ox")
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
        elif opt in ("-o", "--overwrite"):
            args_dict["overwrite"] = True 
        elif opt in ("-x", "--delete-intermediates"):
            args_dict["delete_intermediates"] = True 

    print("Arguments parsed successfully")
    
    return args_dict

def _init_logger():
    """This is so that Javabridge doesn't spill out a lot of DEBUG messages
    during runtime.
    From CellProfiler/python-bioformats.
    """
    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger",
                                         "ROOT_LOGGER_NAME",
                                         "Ljava/lang/String;")

    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory",
                                "getLogger",
                                "(Ljava/lang/String;)Lorg/slf4j/Logger;",
                                rootLoggerName)

    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level",
                                   "WARN",
                                   "Lch/qos/logback/classic/Level;")

    javabridge.call(rootLogger,
            "setLevel",
            "(Lch/qos/logback/classic/Level;)V",
            logLevel)

def get_section_from_vsi(path, dims, chan, series_hires=8):

    # myloglevel="ERROR"
    # rootLoggerName = javabridge.get_static_field("org/slf4j/Logger","ROOT_LOGGER_NAME", "Ljava/lang/String;")
    # rootLogger = javabridge.static_call("org/slf4j/LoggerFactory","getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    # logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level",myloglevel, "Lch/qos/logback/classic/Level;")

    dims = check_bounds(path, dims, series_hires)

    with bf.ImageReader(path) as reader:
        planes = []
        for z in range(3):
            im = reader.read(c=chan, z=z, series=series_hires, XYWH=dims)
            planes.append(im)

    img = np.dstack(planes)
    img = img_as_uint(img)

    return img

def check_bounds(path, dims, series):

    logger.info("{}, {}, {}".format(path, dims, series))

    dims = list(dims)

    myXML = bf.get_omexml_metadata(path)
    o = bf.OMEXML(myXML)
    X = o.image(series).Pixels.get_SizeX()
    Y = o.image(series).Pixels.get_SizeY()

    if X < (dims[0] + dims[2]):
        dims[0] = X - dims[2]

    if Y < (dims[1] + dims[3]):
        dims[1] = Y - dims[3]

    return tuple(dims)

def edf(image):

    result_image = None
    image = np.transpose(image, (2, 0, 1))
    test_image = cle.push(image)
    result_image = cle.extended_depth_of_focus_variance_projection(test_image, result_image, radius_x=2, radius_y=2, sigma=10)

    print(type(result_image), np.max(result_image))

    return cle.pull(result_image).astype("uint16")

_init_logger()

f = open("../config_hires.json")
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

for animal in args_dict["animals"]:
    try:
        os.chdir(os.path.join(folder, animal))
    except FileNotFoundError:
        logger.info("No folder corresponds to {}. Nothing to export.".format(animal))
        continue
    
    if "rawdata" not in os.listdir("."):
        logger.info("No raw data folder for {}. Nothing to export.".format(animal))
        continue

    os.chdir(os.path.join(".", "rawdata"))

    vsi_files = [vsi for vsi in os.listdir(".") if vsi.endswith(".vsi")]
    logger.info("Found {} .vsi files".format(len(vsi_files)))

    check = Check(os.path.join(folder, animal), logger)
    if check.check_hires():
        logger.info("Hires images detected for {}. Continuing to next".format(animal))
        continue

    if len(vsi_files) > 0:
        temp_folder = "/data_temp/{}".format(animal)
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            subprocess.call("cp .. {} -r".format(temp_folder), shell=True)
        os.chdir(temp_folder)
    else:
        print("No .vsi files. Exiting.")
        sys.exit(2)

    channel_strings = args_dict["channels"].split()
    for chan in channel_strings:
        chan_path = os.path.join(".", "hires", "chan{}".format(chan))
        if not os.path.isdir(chan_path):
            os.makedirs(chan_path)
        # else:
        #     if not check_existing_files(chan_path, args_dict["overwrite"]):
        #         print("exiting")


    for vsi in vsi_files:
        print(vsi)
        tic = perf_counter()
        stub = vsi.split(".")[0]
        logger.info("{}".format(os.getcwd()))
        vsipath = os.path.join(os.getcwd(), "rawdata", vsi)
        roipath = os.path.join(os.getcwd(), "rawdata", stub + "_ROIs.zip")
        series_rois = args_dict["series_rois"]
        series_hires = args_dict["series_hires"]
        rotate = args_dict["rotate"]

        logger.info("Using python-bioformats to process {}".format(vsi))

        rois = get_scaled_roi(roipath)

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
                im = get_section_from_vsi(vsipath, dims, chan)
                try:
                    im = get_section_from_vsi(vsipath, dims, chan)
                except:
                    logger.warning("Could not process {} for channel {}".format(roi, chan))
                    continue
                logger.info("Using extended depth of focus to process {} for channel {}".format(roi, chan))
                result = edf(im)

                result = np.rot90(result, 2)

                imsave(os.path.join(chan_path, "{}{}.png".format(stub,roi)), result)
                logger.info("Saving 16-bit .png to {}".format(chan_path))

                f = "{}{}.png".format(stub,roi)
                subprocess.call("cp {} {}".format(os.path.join(chan_path, f), os.path.join(folder, animal, "hires", "chan{}".format(chan))), shell=True)
                
            roi_toc = perf_counter()
            print("Section {} took {} sec".format(roi, roi_toc-roi_tic))

        toc = perf_counter()
        logger.info("Processed {} in {:0.4f} sec".format(vsi, toc-tic))
    
    javabridge.kill_vm()

    if args_dict["delete_intermediates"]:
        subprocess.call("rm /data_temp/{} -r".format(animal), shell=True)
        subprocess.call("trash-empty", shell=True)

logger.info("Finished.")




