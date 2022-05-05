# %%
import os
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

folder = "D:\\Test Data\\histology\\demo_FT122\\test_crops_for_coloc\\"
trap_npy = folder + "crop_trap_hyp_seg.npy"
fos_npy = folder + "crop_fos_hypo_seg.npy"

trap_data = np.load(trap_npy, allow_pickle=True).item()
fos_data = np.load(fos_npy, allow_pickle=True).item()

trap_masks = trap_data["masks"]
fos_masks = trap_data["masks"]

# %%

n_fos_cells = np.max(fos_masks)
lbl = ndimage.label(fos_masks)[0]
fos_centers = ndimage.center_of_mass(fos_masks, lbl, range(1,n_fos_cells))

fos_center_array = np.zeros(np.shape(fos_masks))

for fos_cell_idx in range(n_fos_cells-1):
    print(fos_cell_idx)
    coords = fos_centers[fos_cell_idx]

    fos_center_array[int(coords[0]), int(coords[1])] = 1

# %%
