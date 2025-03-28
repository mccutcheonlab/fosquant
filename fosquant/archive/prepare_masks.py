import os
import numpy as np

def prepare_masks():

    list_of_npy_files = [file for file in os.listdir("cellcounts") if "seg.npy" in file]
    print(list_of_npy_files)
    mask_data = {}
    # data = np.load("..\\data\\Untitled-4_seg.npy", allow_pickle=True).item()

    # masks = data["masks"]

    # cells = []
    # for val in range(1, masks.max()+1):
    #     cells.append(masks == val)

#     # work out overlaps between fos and trapped cells and create three mask files, save in nutil folder

if __name__ == "__main__":
    prepare_masks()