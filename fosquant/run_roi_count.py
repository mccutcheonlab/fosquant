import sys
import getopt
import os
import json

from read_roi import read_roi_zip
import numpy as np
from skimage.draw import polygon, polygon2mask
from skimage.io import imread, imshow
from skimage.measure import find_contours
from matplotlib import pyplot as plt
import pandas as pd

from helper_fx import *
from check_integrity import *

def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["skip_integrity_check"] = False

    try:
        opts, args = getopt.getopt(argv[1:], "a:i")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        elif opt in ("-i", "--check_integrity"):
            args_dict["skip_integrity_check"] = True 

    print("Arguments parsed successfully")
    
    return args_dict

def parse_roi_name(roiname):
    
    section = roiname.split("_")[0]
    region = "".join(roiname.split("_")[1:]).split("-")[0]
    
    return section, region

def get_roi_coords(roi, scale_factor):

    y = [i*scale_factor for i in roi["x"]]
    x = [i*scale_factor for i in roi["y"]]
    xy = [(x,y) for x,y in zip(x,y)]
    
    return xy

def count_neurons(im, roi_coords):
    
    mask = polygon2mask(im.shape, roi_coords)
    masked_image = im * mask
    
    ncells = len(np.unique(masked_image)) - 1

    print("The number of neurons is", ncells)
    
    return ncells, masked_image

def get_coloc(im1, im2, roi_coords):
    binary_1 = np.where(im1 > 0, 1, 0)
    binary_2 = np.where(im2 > 0, 1, 0)
    coloc = binary_1 * binary_2
    
    return len(find_contours(coloc, 0.8))

def process_rois(folder, animal, rois=[]):
    # set folder names
    hirespath = os.path.join(folder, animal, "hires")
    lowrespath = os.path.join(folder, animal, "lowres")
    roipath = os.path.join(lowrespath, "{}_userdefined_ROIs.zip".format(animal))
    
    # load in roi file
    roidata = read_roi_zip(roipath)   
    
    features = []
    existing_section = ""
    for roi in roidata:
        section, region = parse_roi_name(roi)
        print(roi)
        
        if section != existing_section:
            png = [im for im in os.listdir(os.path.join(hirespath, "chan1")) if (section in im) and ("masks" in im)][0]
            lowres = [im for im in os.listdir(lowrespath) if (section in im)][0]
            im_fos = imread(os.path.join(hirespath, "chan1", png))
            im_trap = imread(os.path.join(hirespath, "chan2", png))
            im_low = imread(os.path.join(lowrespath, lowres))
    
            scale_factor = int(im_fos.shape[0]/im_low.shape[0])
            existing_section = section
            
        # make mask and get cell numbers
        xy = get_roi_coords(roidata[roi], scale_factor)
        
        nfos, masked_fos = count_neurons(im_fos, xy)
        ntrap, masked_trap = count_neurons(im_trap, xy)
        ncoloc = get_coloc(masked_fos, masked_trap, xy)
        
        area = np.sum(polygon2mask(im_fos.shape, xy))
        
        section_data = {"animal": [animal], "section": [section], "region": [region], "area": [area], "nfos": [nfos], "ntrap": [ntrap], "ncoloc": [ncoloc]}
        
        df_temp = pd.DataFrame(section_data)
 
        features.append(df_temp)
        
    df = pd.concat(features, ignore_index=True)

    df.to_csv(os.path.join(lowrespath, "user_rois_{}.csv".format(animal)))

    return df

f = open("../config.json")
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

list_of_dfs = []
for animal in args_dict["animals"]:
    existing_csv_path = os.path.join(folder, animal, "lowres", "user_rois_{}.csv".format(animal))
    if os.path.exists(existing_csv_path):
        df = pd.read_csv(existing_csv_path)
        if "mouse" in df.columns:
            df.rename({"mouse": "animal"}, inplace=True)
        list_of_dfs.append(df)
    else:
        rois = check_rawdata(os.path.join(folder, animal), logger)
        if check_masks(os.path.join(folder, animal), logger, rois=rois):
            try:
                list_of_dfs.append(process_rois(folder, animal))
            except FileNotFoundError:
                print("Files not available for {}".format(animal))

df_main = pd.concat(list_of_dfs)

results_folder = os.path.join(folder, "results")
if not os.path.exists(results_folder):
    os.mkdir(results_folder)

df_main.to_csv(os.path.join(results_folder, "df_user_counts.csv"))

# df_main = pd.read_csv(os.path.join(results_folder, "df_user_counts.csv"))

# df_meta =  pd.read_csv(os.path.join(folder, "metafile_ftig.csv"))

# df_meta.set_index("animal", inplace=True)

# df_meta.drop(["folder", "slide1A", "slide1B", "slide1C"], axis=1, inplace=True)

# df_main.join(df_meta, on="animal")

print(df_main.head())

print(df_meta.head())

print(df_main.head())
# df_main.to_csv(os.path.join(results_folder, "df_user_counts_with_groups.csv"))


# For speeding up consider processing each animal in parallel using threading / pooling
# see this thread https://stackoverflow.com/questions/19695249/load-just-part-of-an-image-in-python

# also add verbose option to silence logging and reporting on cell counts
