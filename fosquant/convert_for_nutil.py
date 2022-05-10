# %%
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from PIL import Image

folder = "D:\\Test Data\\histology\\demo_FT122\\test_crops_for_coloc\\"
file = "crop_trap_vp_cp_masks.png"
original = np.array(Image.open(folder+file), dtype="int8")

nutil_masks = np.where(original > 0, 255, 0)
# masks_8bit = np.array(nutil_masks, dtype="int8")

# print(type(masks_8bit))

savefile = Image.fromarray(nutil_masks)
savename = folder + file.split(".")[0] + "_nutil.png"
savefile.save(savename, format="png", bits="I;8")

# mpl.image.imsave(savename, nutil_masks)

f, ax = plt.subplots(ncols=2)
ax[0].imshow(original)
ax[1].imshow(nutil_masks)



# %%
