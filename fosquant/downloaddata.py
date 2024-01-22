# import sys
# import getopt
# import os
# import shutil
# import subprocess
# import json

# from datetime import datetime

# import pandas as pd

# from helper_fx import *



import sys
from pathlib import Path
import click
import json
import subprocess

from helper_fx import setup_logger

sys.path.append("~/Github/fosquant/")

@click.command()
@click.option("--config-file", type=str, default="config.json", help="A file containing config options. If not present are parsed correctly the script will exit.")
@click.option("--animals", "-a", type=str, default="", help="List of animals to be processed")
@click.option("--get-metafile", "-m", type=bool, is_flag=True, help="If selected attempts to download metafile from Azure")
@click.option("--get-data", "-d", type=bool, is_flag=True, help="If selected attempts to download datafiles from Azure")
@click.option("--overwrite", type=bool, is_flag=True, help="Choose if you want the option to overwrite files")
def download(config_file, animals, get_metafile, get_data, overwrite):
    print("Downloading...")
    
    # finds and opens config file
    print(f"The config file is {config_file}")
    try:
        f = open(config_file)
        config_data = json.load(f)
    except:
        print("Exiting because cannot find config file:", config_file)
        sys.exit(2)
        
    logger = setup_logger(config_data["project_dir"])
        
    if config_data["metafile"]:
        logger.info("Downloading metafile from remote Azure repo...")
        path_to_azcopy = config_data["path_to_azcopy"]
        subprocess.call("{} cp {} {}".format(path_to_azcopy, config_data["metafile"], config_data["project_dir"]), shell=True)    


if __name__ == "__main__":
    print("processing stuff")
    download()
    






# csv_file = os.path.join(args_dict["project_dir"], os.path.basename(config_data["metafile"]))
# logger.info("Reading CSV file... {}".format(csv_file))
# if not os.path.exists(csv_file):
#     logger.info("CSV file cannot be found. Exiting.")
#     sys.exit(2)

# df = pd.read_csv(csv_file)

# if args_dict["animals"] == "all":
#     args_dict["animals"] = df["animal"].unique()
# elif args_dict["animals"] == "":
#     logger.info("No animals given. Exiting")
#     sys.exit(2)
# else:
#     args_dict["animals"] = args_dict["animals"].split()

# # make directory structure
# path_root = args_dict["project_dir"]

# if not os.path.isdir(path_root):
#     logger.info("Project path does not exist. Exiting.")
#     sys.exit(2)

# for animal in args_dict["animals"]:
#     animal_root_path = os.path.join(path_root, animal)
#     animal_raw_path = os.path.join(animal_root_path, "rawdata")

#     for path in [animal_root_path, animal_raw_path]:
#         if not os.path.isdir(path):
#             os.mkdir(path)

#     if args_dict["get_data"]:
#         if not check_existing_files(animal_raw_path, args_dict["overwrite"]):
#             print("exiting")
#             continue

#         row = df[(df["animal"] == animal)]
#         if len(row) == 0:
#             logger.info("{} not in metafile.".format(animal))
#             continue

#         slide_files = [slide.item() for slide in [row["slide1A"], row["slide1B"], row["slide1C"]] if slide.item() != "none" ]
#         remote_folder = row["folder"].item()

#         logger.info("Downloading files... {}".format(slide_files))
#         path_to_azcopy = config_data["path_to_azcopy"]

#         for idx, file in enumerate(slide_files):
#             if not file.endswith(".vsi"):
#                 file = file + ".vsi"
                
#             vsi_file_remote = os.path.join(config_data["remote"], remote_folder, file)
#             vsi_file_local = os.path.join(animal_raw_path, "{}_{}A.vsi".format(animal, idx+1))

#             logger.debug("{}, {}".format(vsi_file_remote, vsi_file_local))

#             vsi_folder_remote_stub = "_{}_".format(file.split(".")[0])
#             vsi_folder_remote = os.path.join(config_data["remote"], remote_folder, vsi_folder_remote_stub)

#             vsi_folder_local = "_{}_{}A_".format(animal, idx+1)

#             subprocess.call("{} cp {} {}".format(path_to_azcopy, vsi_file_remote, vsi_file_local), shell=True)
#             subprocess.call("{} cp {} {} --recursive=true".format(path_to_azcopy, vsi_folder_remote, animal_raw_path), shell=True)

#             ### need to work out why I had these lines here ###
#             # os.chdir(animal_raw_path)
#             # # subprocess.call("mv {} {}".format(os.path.join(animal_raw_path, vsi_folder_remote_stub),
#             # #                                   os.path.join(animal_raw_path, vsi_folder_local)), shell=True)
#             # if os.path.exists(os.path.join(animal_raw_path, vsi_folder_local)):
#             #     shutil.rmtree(vsi_folder_local)

#             # os.rename(vsi_folder_remote_stub, vsi_folder_local)
            
#             # #need to fix this line
#             # if not (os.path.exists(vsi_file_local)) or (os.path.exists(vsi_folder_local)):
#             #     logger.debug("Failed to get file using azcopy. Check azcopy log.")

