import sys
import getopt
from pathlib import Path
import shutil
import os
from itertools import compress
import pandas as pd
import roifile as rf

# get and parse options
def parse_args(argv):
    args_dict = {}
    args_dict["animals"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "a:")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        
    print("Arguments parsed successfully")
    
    return args_dict

args_dict = parse_args(sys.argv)
args_dict["prefix"] = "FT"

PROJECT_DIR = Path("C:/Users/jmc010/Data/fostrap/")
ROI_FILE_SUFFIX = "_cleaned"

print(args_dict)

if args_dict["animals"] == "all":
    args_dict["animals"] = [d for d in os.listdir(PROJECT_DIR) if args_dict["prefix"] in d]
elif args_dict["animals"] == "":
    print("No animals given. Exiting")
    sys.exit(2)
else:
    args_dict["animals"] = args_dict["animals"].split()

for animal in args_dict["animals"]:
    print("\n******************")
    print("Cleaning duplicated ROIs for", animal)
    folder = PROJECT_DIR / animal
    print(folder)

    try:
        roipath = folder / "lowres" / "{}_userdefined_ROIs.zip".format(folder.name)
        rois = rf.ImagejRoi.fromfile(roipath)
    except FileNotFoundError:
        print(f"No files found for {animal}. Exiting.")
        continue

    df = pd.DataFrame.from_dict(rois)
    print(f"{len(df)} ROIs in original file.")
    dups = ~df.duplicated(subset=["top", "left"])

    rois_red = list(compress(rois, dups.tolist()))
    print(f"{len(rois_red)} ROIs left after removing duplicates.")

    temp_roi_folder = folder / "temp_roi"
    if not os.path.exists(temp_roi_folder):
        os.mkdir(temp_roi_folder)
    for idx, roi in enumerate(rois_red):
        roi.name = "{}_{}".format(roi.name, idx)
        roi.tofile(temp_roi_folder / "{}.roi".format(roi.name))

    shutil.make_archive(folder / "lowres" / "{}_userdefined_ROIs{}".format(folder.name, ROI_FILE_SUFFIX), "zip", temp_roi_folder)
    shutil.rmtree(temp_roi_folder)


    