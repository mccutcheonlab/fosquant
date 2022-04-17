import os

import cellpose

def project_setup():
    # maybe don't ask for folder or if folder not given just run in the current directory
    current_working_directory = os.getcwd()
    print("Setting up project in {}".format(current_working_directory))

    # check if folder has rawdata folder, examine files and print message. if not exit.
    # create variable for naming files based on folder name

    # make folder for lowres
    # fill with converted lowres images
    # write separate function to do this

    # make folder for cell counts

    # make folder for nutil

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
