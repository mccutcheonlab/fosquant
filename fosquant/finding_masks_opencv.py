# %%
import cv2

import numpy as np
# from scipy import ndimage
import matplotlib.pyplot as plt

# %%

folder = "D:\\Test Data\\histology\\demo_FT122\\test_crops_for_coloc\\"

trap_png = folder + "crop_trap_hyp_cp_masks.png"
trap_jpg = folder + "crop_trap_hyp.jpg"

from skimage import io
folder = "D:\\Test Data\\histology\\demo_FT122\\test_crops_for_coloc\\"

fos_png = folder + "crop_fos_hypo_cp_masks.png"
im = io.imread(fos_png)

fos_array = np.zeros(np.shape(im))
regions = regionprops(im)
for props in regions:
    y0, x0 = props.centroid
    fos_array[int(y0), int(x0)] = 1

trap_png = folder + "crop_trap_hyp_cp_masks.png"
im = io.imread(trap_png)
n_trap_cells = np.max(im)
trap_array = im*10

combined_array = fos_array + trap_array

trap_output = np.zeros(np.shape(im))
coloc_output = np.zeros(np.shape(im))

regions = regionprops(im)
for trap_cell_idx in range(1,n_trap_cells):
  i = trap_cell_idx
  c = combined_array
  res = c[ (c>=i*10) & (c<(i+1)*10)]
  print(np.mean(res))
  if np.mean(res) % 10:
    print("double")
    x, y = np.where(c==np.max(res))
    coloc_output[int(y), int(x)] = 1

  else:
    print("trap")
    y, x = regions[i].centroid
    print(y, x)
    trap_output[int(y), int(x)] = 2

fos_output = (fos_array - (coloc_output)) * 3


io.imsave(folder + "fos_output.png", fos_output)
