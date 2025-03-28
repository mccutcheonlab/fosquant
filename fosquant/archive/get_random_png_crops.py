import os
import sys
from pathlib import Path
import random
import numpy as np
from PIL import Image

seed = random.randrange(sys.maxsize)
sh_seed = str(seed)[-5:]
print("Seed was:", seed, "Short seed", sh_seed)


def get_random_png_crops(folder, chan=1, n=20, dims=(500,500)):

    crops_folder = Path(folder) / "cropped" / "chan{}".format(chan)
    if not os.path.exists(crops_folder):
        os.makedirs(crops_folder)
        
    animal_dirs = [d for d in Path(folder).iterdir() if d.is_dir() and d.name.startswith("F")]
    random.shuffle(animal_dirs)
    print(animal_dirs)

    if len(animal_dirs) < n:
        n = len(animal_dirs)

    for i in range(n):
        hires_folder = Path(folder) / animal_dirs[i] / "hires" / "chan{}".format(chan)
        try:
            pngs = [png for png in os.listdir(hires_folder) if png.endswith(".png") and not png.endswith("masks.png")]
            random.shuffle(pngs)
            print(pngs[0])
            im = Image.open(hires_folder / pngs[0])
            h, w = np.shape(im)
            x0, y0 = random.randint(0, w-dims[0]), random.randint(0, h-dims[1])
            bbox = (x0, y0, x0+dims[0], y0+dims[1])
            im2 = im.crop(bbox)
            crop_name = pngs[0].split(".")[0] + "_" + sh_seed + ".png"
            print(crop_name)
            im2.save(crops_folder / crop_name)
            im.close()
        except FileNotFoundError:
            print("failed")
            pass

if __name__ == "__main__":
    project_dir = "/mnt/d/TestData/fostrap/will/"
    project_dir = "/data/FTIG/"
    project_dir = Path("D:/TestData/fostrap/will/")

    get_random_png_crops(project_dir, chan=1, n=100)