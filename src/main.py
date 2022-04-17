
import os
from PIL import Image, ImageOps, ImageEnhance

import cellpose

def make_folder(foldername, parent_directory):
    try:
        path = os.path.join(parent_directory, foldername)
        os.mkdir(path)
    except FileExistsError:
        print("{} already exists!".format(path))

def convert_to_lowres(image_file):
        image_file_gray = ImageOps.grayscale(image_file)
        image_file_invert = ImageOps.invert(image_file_gray)
        image_file_contrast = ImageEnhance.Contrast(image_file_invert).enhance(10)

        return image_file_contrast

def project_setup():
    # maybe don't ask for folder or if folder not given just run in the current directory
    current_working_directory = os.getcwd()
    print("Setting up project in {}".format(current_working_directory))

    basename = os.path.split(current_working_directory)[-1]

    # check if folder has rawdata folder, examine files and print message. if not exit.
    filenames = os.listdir()
    if "rawdata" in filenames:
        rawdatafiles = os.listdir("rawdata")
        print(rawdatafiles)
        # TODO examine files, print how many
    else:
        print("Cannot find folder with rawdata.")
        return

    make_folder("lowres", current_working_directory)

    # TODO convert rawdata files to lowres
    for file in rawdatafiles:
        image_in = os.path.join(current_working_directory, "rawdata", file)
        image_out = os.path.join(current_working_directory, "lowres", "LR_{}".format(file))

        converted_image = convert_to_lowres(Image.open(image_in))
        converted_image.save(image_out, quality=2)

    make_folder("cellcounts", current_working_directory)

    make_folder("nutil", current_working_directory)

# def cell_counts():
    
#     # use cellpose to do cell counts

# def prepare_masks():

#     # work out overlaps between fos and trapped cells and create three mask files, save in nutil folder

# def run_nutil():

#     # create .nut files
#     # use subprocess to run nutil from command line

#     # have option to create plots by calling separate plotting function

if __name__ == "__main__":
    project_setup()
