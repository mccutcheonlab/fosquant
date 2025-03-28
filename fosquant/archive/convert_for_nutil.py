# %%
import os
import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt

from PIL import Image

def convert_for_nutil(full_filename):

	original = np.array(Image.open(full_filename), dtype="int8")

	nutil_masks = np.where(original > 0, 255, 0)
	# masks_8bit = np.array(nutil_masks, dtype="int8")

	# print(type(masks_8bit))

	savefile = Image.fromarray(nutil_masks)
	savename = folder + file.split(".")[0] + "_nutil.png"
	savefile.save(savename, format="png", bits="I;8")

	# mpl.image.imsave(savename, nutil_masks)

	# f, ax = plt.subplots(ncols=2)
	# ax[0].imshow(original)
	# ax[1].imshow(nutil_masks)

if __name__ == "__main__":

    folder = os.getcwd()

    image_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith("cp_masks.png")]

    for filename in image_files:

        print(filename)
        convert_for_nutil(os.path.join(folder, filename))


# %%
