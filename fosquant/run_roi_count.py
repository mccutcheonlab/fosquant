import sys
import getopt
import os
import json
from pathlib import Path

from read_roi import read_roi_zip
import numpy as np
from skimage.draw import polygon2mask
from skimage.io import imread, imshow, imsave
from skimage.measure import find_contours
import pandas as pd
from multiprocessing import Pool, cpu_count

from helper_fx import *
from check_integrity import *

def parse_args(argv, config_data):
    args_dict = config_data
    args_dict["animals"] = ""
    args_dict["skip_integrity_check"] = False
    args_dict["verbose"] = False
    args_dict["overwrite"] = False
    args_dict["threaded"] = False
    args_dict["fos_threshold"] = 0
    args_dict["region"] = ""
    args_dict["dummy_run"] = False
    args_dict["save_suffix"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "a:ivotf:r:ds:")
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
        elif opt in ("-v", "--verbose"):
            args_dict["verbose"] = True
        elif opt in ("-o", "--overwrite"):
            args_dict["overwrite"] = True 
        elif opt in ("-t", "--threaded"):
            args_dict["threaded"] = True 
        elif opt in ("-f", "fos_threshold"):
            args_dict["fos_threshold"] = float(arg)
        elif opt in ("-r", "region"):
            args_dict["region"] = arg
        elif opt in ("-d", "dummy_run"):
            args_dict["dummy_run"] = True
        elif opt in ("-s", "save_suffix"):
            args_dict["save_suffix"] = str(arg)
    
    print("Arguments parsed successfully")
    
    return args_dict

def parse_roi_name(roiname):
    
    section = roiname.split("_")[0]
    region = "".join(roiname.split("_")[1:]).split("-")[0]
    
    return section, region

def get_sections_from_rois(roidata):
    sections = []
    for roi in roidata.keys():
        sections.append(roi.split("_")[0])
 
    return list(set(sections))

def get_roi_coords(roi, scale_factor):

    if roi["type"] == "polygon":
        x = [int(i*scale_factor) for i in roi["x"]]
        y = [int(i*scale_factor) for i in roi["y"]]
        xy = [(x,y) for x,y in zip(x,y)]

    elif roi["type"] == "rectangle":
        
        x1, x2 = [int(i*scale_factor) for i in (roi["left"], roi["left"]+roi["width"])]
        y1, y2 = [int(i*scale_factor) for i in (roi["top"], roi["top"]+roi["height"])]

        xy = [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]

    return xy

def count_neurons(im, roi_coords, verbose=False):

    mask = polygon2mask(im.shape, [(y,x) for x,y in roi_coords])
    masked_image = im * mask
    
    ncells = len(np.unique(masked_image)) - 1

    if verbose: print("The number of neurons is", ncells)
    
    return ncells, masked_image

def get_coloc(im1, im2, area_threshold = 8, verbose=False):
    binary_1 = np.where(im1 > 0, 1, 0)
    binary_2 = np.where(im2 > 0, 1, 0)
    coloc = binary_1 * binary_2

    contours = find_contours(coloc, 0.8)
    areas = [np.sum(polygon2mask(coloc.shape,c)) for c in contours]
    ncoloc = len([a for a in areas if a > area_threshold])

    if verbose: print("The number of colocalised neurons is", ncoloc)
    
    return ncoloc

def get_clipped_im(im, xy):

    x = [x for x, y in xy]
    y = [y for x, y in xy]

    roi_min_x, roi_max_x = np.min(x), np.max(x)
    roi_min_y, roi_max_y = np.min(y), np.max(y)

    print(roi_min_x, roi_max_x, roi_min_y, roi_max_y)

    im_out = im[roi_min_y:roi_max_y, roi_min_x:roi_max_x]

    x_rescaled = [x - roi_min_x for x in x]
    y_rescaled = [y - roi_min_y for y in y]

    xy_rescaled = [(x,y) for x,y in zip(x_rescaled, y_rescaled)]

    return im_out, xy_rescaled

def process_rois(folder, animal, rois=[], verbose=False):

    # set folder names
    hirespath = folder / animal / "hires"
    lowrespath = folder / animal / "lowres"
    roipath = lowrespath / "{}_userdefined_ROIs_cleaned.zip".format(animal)

    for path in [hirespath, lowrespath, roipath]:
        if not path.exists(): return
    
    # load in roi file
    roidata = read_roi_zip(roipath)   
    
    features = []
    
    for section in get_sections_from_rois(roidata):
        print(f"Analyzing section {section} for {animal}")

        png = [im for im in os.listdir(hirespath / "chan1") if (section in im) and ("masks" in im)][0]
        lowres = [im for im in os.listdir(lowrespath) if (section in im)][0]
        im_fos = imread(hirespath / "chan1" / png)
        im_trap = imread(hirespath / "chan2" / png)
        im_low = imread(lowrespath / lowres)

        if args_dict["fos_threshold"] > 0:
            print("reading in raw fos image")
            im_fos_raw = imread(hirespath / "chan1" / "{}.png".format(png.split("_cp")[0]))

        scale_factor = int(im_fos.shape[0] / im_low.shape[0])

        for roi in roidata:
            roi_section, region = parse_roi_name(roi)
            if args_dict["region"] not in region:
                continue
            if roi_section != section:
                continue
            print(animal, section, region)

            xy = get_roi_coords(roidata[roi], scale_factor)

            im_fos_rescaled, xy_rescaled = get_clipped_im(im_fos, xy)
            im_trap_rescaled, _ = get_clipped_im(im_trap, xy)

            if args_dict["fos_threshold"] > 0:
                im_fos_raw_rescaled, _ = get_clipped_im(im_fos_raw, xy)

                im_fos_rescaled = make_thresholded_mask(im_fos_raw_rescaled, im_fos_rescaled, xy_rescaled, threshold=args_dict["fos_threshold"])
            
            nfos, masked_fos = count_neurons(im_fos_rescaled, xy_rescaled, verbose=verbose)
            ntrap_old, _ = count_neurons(im_trap, xy, verbose=verbose)
            ntrap, masked_trap = count_neurons(im_trap_rescaled, xy_rescaled, verbose=verbose)

            print(ntrap, "should match", ntrap_old)
            ncoloc = get_coloc(masked_fos, masked_trap, verbose=verbose)

            area = np.sum(polygon2mask(im_fos.shape, xy))

            section_data = {"animal": [animal], "section": [section], "region": [region], "area": [area], "nfos": [nfos], "ntrap": [ntrap], "ncoloc": [ncoloc]}
            features.append(pd.DataFrame(section_data))
   
    df = pd.concat(features, ignore_index=True)

    df.to_csv(lowrespath / "user_rois_{}.csv".format(animal))

    print(f"Finished analyzing {animal}")

    return df

if __name__ == "__main__":
    config_file = Path("../config.json").resolve()
    f = open(config_file)
    config_data = json.load(f)
    args_dict = parse_args(sys.argv, config_data)

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

    list_of_dfs = []
    animals_to_process = []

    for animal in args_dict["animals"]:
        existing_csv_path = folder / animal / "lowres" / "user_rois_{}.csv".format(animal)

        if existing_csv_path.exists():
            if not args_dict["overwrite"]:
                df = pd.read_csv(existing_csv_path)
                if "mouse" in df.columns:
                    df.rename({"mouse": "animal"}, inplace=True)
                list_of_dfs.append(df)
                continue
            else:
                print("Overwriting existing csv file for {}".format(animal))
        if not args_dict["skip_integrity_check"]:
            check = Check(folder / animal, logger)
            if not check.check_all():
                logger.warning("Integrity check not passed. Not analysing {}".format(animal))
                continue
        else:
            logger.warning("Skipping integrity check for {}. Could be issues with analysis.".format(animal))
        
        animals_to_process.append(animal)

    logger.info("Animals being processed are: {}".format(animals_to_process))

    if args_dict["dummy_run"]:
        print("This is a dummy run to check arguments etc")
        sys.exit(2)

    if len(animals_to_process) > 0:
        if args_dict["threaded"]:
            pool_args = [(folder, animal) for animal in animals_to_process]

            pool_size = cpu_count()
            with Pool(processes=pool_size) as pool:
                list_of_pooled_dfs = pool.starmap(process_rois, pool_args)
        else:
            list_of_pooled_dfs = []
            for animal in animals_to_process:
                list_of_pooled_dfs.append(process_rois(folder, animal, verbose=args_dict["verbose"]))

        df_main = pd.concat(list_of_dfs+list_of_pooled_dfs)
    else:
        try:
            df_main = pd.concat(list_of_dfs)
        except:
            print("Failed to concatenate. Maybe no dataframes. Exiting.")
            sys.exit(2)


    results_folder = folder / "results"
    if not results_folder.exists():
        os.mkdir(results_folder)

    df_main.to_csv(results_folder / "df_user_counts{}.csv".format(args_dict["save_suffix"]))

    print(df_main.head())

    print("Finished running script successfully")
