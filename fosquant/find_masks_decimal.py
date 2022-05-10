# %%
import cv2

import numpy as np
# from scipy import ndimage
import matplotlib.pyplot as plt

from skimage import io
from skimage.measure import regionprops

folder = "D:\\Test Data\\histology\\demo_FT122\\test_crops_for_coloc\\"

trap_png = folder + "crop_trap_hyp_cp_masks.png"
fos_png = folder + "crop_fos_hypo_cp_masks.png"

img_fos = io.imread(fos_png)

fos_array = np.zeros(np.shape(img_fos))
regions = regionprops(img_fos)
for idx, props in enumerate(regions):
    y0, x0 = props.centroid
    fos_array[int(y0), int(x0)] = idx

n_fos_cells = np.max(fos_array)
power_scale = int(np.log10(n_fos_cells))+1

img_trap = io.imread(trap_png)
# n_trap_cells = np.max(im)
# trap_array = im*10
trap_array = img_trap * 10**power_scale
print(np.max(trap_array))

comb_array = fos_array + trap_array

# %%
