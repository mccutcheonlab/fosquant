import os

import numpy as np
from cellpose import io, models
from PIL import Image

def process_large_images(filename, model, diameter):
    img = Image.open(filename)
    width, height = img.size

    img1_crop = img.crop((0, 0, int(width/2), height))
    if width % 2:
        img2_crop = img.crop((int(width/2)+1, 0, width, height))
    else:
        img2_crop = img.crop((int(width/2), 0, width, height))

    imgs = [np.array(im) for im in [img1_crop, img2_crop]]

    pretrained_model = model
    channels = [0,0]
    diameter = diameter
    resample=True

    model = models.CellposeModel(gpu=True, model_type=pretrained_model)
    masks, _, _, = model.eval(imgs, channels=channels, diameter=diameter, resample=False)  

    masks1, masks2 = masks

    max_masks = np.max(masks1)
    masks2_scaled = np.where(masks2>0, masks2+max_masks, 0)

    masks_merged = np.concatenate([masks1, masks2_scaled], axis=1)

    io.imsave("{}_cp_masks.png".format(filename.split(".")[0]), masks_merged)

# folder="D:\\Test Data\\histology\\demo_FT122\\test_crops_for_coloc\\single_image\\"

if __name__ == "__main__":

    folder = os.getcwd()

    image_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith("jpg")]
    model = "/home/jaime/Data/cellpose_models/CP_20220504_fos"
    diameter = 10

    for filename in image_files:

        print(filename)
        process_large_images(filename, model, diameter)








# %%
