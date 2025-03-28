import sys
from pathlib import Path
import click
import json
import subprocess
from urllib.parse import urljoin

import pandas as pd

from helper_fx import setup_logger, check_existing_files

sys.path.append("~/Github/fosquant/")

import click
import json
import subprocess
import sys
from pathlib import Path
import pandas as pd

@click.command()
@click.option("--config-file", type=str, default="config.json", help="A file containing config options. If not present are parsed correctly the script will exit.")
@click.option("--animals", "-a", type=str, default="", help="List of animals to be processed")
@click.option("--get-metafile", "-m", type=bool, is_flag=True, help="If selected attempts to download metafile from Azure")
@click.option("--get-data", "-d", type=bool, is_flag=True, help="If selected attempts to download datafiles from Azure")
@click.option("--overwrite", type=bool, is_flag=True, help="Choose if you want the option to overwrite files")
def download(config_file, animals, get_metafile, get_data, overwrite):
    """
    Downloads data and metafile from Azure based on the provided configuration file.

    Args:
        config_file (str): A file containing config options. If not present or parsed correctly, the script will exit.
        animals (str): List of animals to be processed.
        get_metafile (bool): If selected, attempts to download metafile from Azure.
        get_data (bool): If selected, attempts to download datafiles from Azure.
        overwrite (bool): Choose if you want the option to overwrite files.
    """
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
        
    if get_metafile:
        logger.info("Downloading metafile from remote Azure repo...")
        subprocess.run(["azcopy", "cp", config_data["metafile"], config_data["project_dir"]])
        
    csv_file = Path(config_data["project_dir"]) / Path(config_data["metafile"]).name
    logger.info("Reading CSV file... {}".format(csv_file))
    if not Path(csv_file).exists():
        logger.info("CSV file cannot be found. Exiting.")
        sys.exit(2)
        
    df = pd.read_csv(csv_file)
    
    if animals == "all":
        animals_to_download = df["animal"].unique()
    elif animals == "":
        logger.info("No animals given. Exiting")
        sys.exit(2)
    else:
        animals_to_download = animals.split()
        
    # make directory structure
    path_root = Path(config_data["project_dir"])

    if not path_root.is_dir():
        logger.info("Project path does not exist. Exiting.")
        sys.exit(2)
        
    for animal in animals_to_download:
        animal_root_path = path_root / animal
        animal_raw_path = animal_root_path / "rawdata"

        for path in [animal_root_path, animal_raw_path]:
            if not path.is_dir():
                path.mkdir()

        if get_data:
            if not check_existing_files(animal_raw_path, overwrite):
                print("exiting")
                continue
            
        row = df[(df["animal"] == animal)]
        if len(row) == 0:
            logger.info("{} not in metafile.".format(animal))
            continue
        
        print(row)
        
        slide_files = [slide.item() for slide in [row["slide1A"], row["slide1B"], row["slide1C"]] if slide.item() != "none" ]
        vsi_files = [file if file.endswith(".vsi") else file + ".vsi" for file in slide_files]
        
        folder_columns = [col for col in df.columns if 'folder' in col]
        if len(folder_columns) == 1:
            remote_folder = row["folder"].item()
            vsi_paths = [Path(remote_folder) / vsi_file for vsi_file in vsi_files]
        elif len(folder_columns) == 0:
            print("no folders given in metafile. Exiting")
            sys.exit(2)
        else:
            if len(folder_columns) != len(slide_files):
                print("number of folders does not match number of slides. Exiting")
                sys.exit(2)
            else:
                vsi_paths = []
                for idx, file in enumerate(slide_files):
                    vsi_paths.append(Path(row[folder_columns[idx]].item()) / vsi_files[idx])
        
        for idx, file in enumerate(vsi_paths):
            vsi_file_remote = file
            vsi_file_local = animal_raw_path / "{}_{}A.vsi".format(animal, idx+1)
            
            logger.debug("{}, {}".format(vsi_file_remote, vsi_file_local))

            vsi_folder_remote_stub = "_{}_".format(file.name.split(".")[0])
            vsi_folder_remote = file.parent / vsi_folder_remote_stub
            
            subprocess.run(["azcopy", "cp", urljoin(config_data["remote"], str(vsi_file_remote)), vsi_file_local])
            subprocess.run(["azcopy", "cp", urljoin(config_data["remote"], str(vsi_folder_remote)), animal_raw_path, "--recursive=true"])
            
if __name__ == "__main__":
    print("processing stuff")
    download()
    print("done")

