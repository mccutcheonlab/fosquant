# script to run for batch exporting lowres files

import sys
import getopt
import os
import subprocess
import json
import click
from  pathlib import Path

from helper_fx import *

sys.path.append("~/Github/fosquant/")
path_to_macro = Path.cwd() / "export_lowres_batch.ijm"
path_to_imagej = Path("~/Fiji.app/macros").expanduser() 
subprocess.run(["cp", path_to_macro, path_to_imagej])

@click.command()
@click.option("--config-file", type=str, default="config.json", help="A file containing config options. If not present are parsed correctly the script will exit.")
@click.option("--animals", "-a", type=str, default="", help="List of animals to be processed")
@click.option("--channels", "-c", type=str, default="", help="List of channels to be export")
@click.option("--series", "-s", type=str, default="", help="Series to be used")
@click.option("--rotate", type=str, default="", help="Choose whether to rotate images")
@click.option("--invert", type=bool, is_flag=True, help="Choose if you want to invert the images")
def lowres(config_file, animals, channels, series, rotate, invert):
    
    # finds and opens config file
    print(f"The config file is {config_file}")
    try:
        f = open(config_file)
        config_data = json.load(f)
    except:
        print("Exiting because cannot find config file:", config_file)
        sys.exit(2)
        
    logger = setup_logger(config_data["project_dir"])
    folder = Path(config_data["project_dir"])
    os.chdir(folder)

    if animals == "all":
        animals_to_process = [d for d in os.listdir(folder) if config_data["prefix"] in d]
    elif animals == "":
        logger.info("No animals given. Exiting")
        sys.exit(2)
    else:
        animals_to_process = animals.split()
        
    logger.info("Processing...{}".format(animals_to_process))
    
    for animal in animals_to_process:
        try:
            os.chdir(folder / animal)
        except FileNotFoundError:
            logger.info("No folder corresponds to {}. Nothing to transfer.".format(animal))
            continue
        
        if "rawdata" not in [str(dir.name) for dir in Path.cwd().iterdir() if dir.is_dir()]:
            logger.info("No raw data folder for {}. Nothing to transfer.".format(animal))
            continue
            
        os.chdir(os.path.join(".", "rawdata"))
        
        print(Path.cwd())
        
        vsi_files = [vsi for vsi in Path.cwd().iterdir() if vsi.suffix == ".vsi"]
        logger.info("Found {} .vsi files".format(len(vsi_files)))
        
        for vsi in vsi_files:
            stub = vsi.name.split(".")[0]
            print(stub)
            print(vsi)
            vsipath = os.path.join(os.getcwd(), vsi)
            # rois = os.path.join(os.getcwd(), stub + "_ROIs.zip")
            # channel = args_dict["channels"] 
            # rotate = args_dict["rotate"] 
            # series = args_dict["series"]
            # if args_dict["invert"]:
            #     invert = "invertOn"
            # else:
            #     invert = "invertOff"

            # logger.info("Opening ImageJ to process {}".format(vsi))
            # subprocess.run(["config_data["path_to_imagej"], "-macro", "export_lowres_batch.ijm",  '{}, {}, {}, {}, {}, {}' -batch".format(, vsipath, rois, series, channel, rotate, invert ), shell=True)
    
    logger.info("Finished.")

if __name__ == "__main__":
    print("exporting lowres images...")
    lowres()
    print("done")
    




#     vsi_files = [vsi for vsi in os.listdir(".") if vsi.endswith(".vsi")]
#     logger.info("Found {} .vsi files".format(len(vsi_files)))

#     for vsi in vsi_files:
#         stub = vsi.split(".")[0]
#         vsipath = os.path.join(os.getcwd(), vsi)
#         rois = os.path.join(os.getcwd(), stub + "_ROIs.zip")
#         channel = args_dict["channels"] 
#         rotate = args_dict["rotate"] 
#         series = args_dict["series"]
#         if args_dict["invert"]:
#             invert = "invertOn"
#         else:
#             invert = "invertOff"

#         logger.info("Opening ImageJ to process {}".format(vsi))
#         subprocess.call("{} -macro export_lowres_batch.ijm '{}, {}, {}, {}, {}, {}' -batch".format(config_data["path_to_imagej"], vsipath, rois, series, channel, rotate, invert ), shell=True)
 
# logger.info("Finished.")