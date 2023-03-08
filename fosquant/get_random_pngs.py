import os
import random
import subprocess

def get_random_pngs(folder, chan=1, n=20):

    crops_folder = os.path.join(folder, "cropped", "chan{}".format(chan))
    if not os.path.exists(crops_folder):
        os.makedirs(crops_folder)
        
    animal_dirs = [d for d in os.listdir(folder) if d.startswith("FT")]
    random.shuffle(animal_dirs)
    print(animal_dirs)

    if len(animal_dirs) < n:
        n = len(animal_dirs)

    for i in range(n):
        hires_folder = os.path.join(folder, animal_dirs[i], "hires", "chan{}".format(chan))
        try:
            pngs = [png for png in os.listdir(hires_folder) if png.endswith(".png")]
            random.shuffle(pngs)
            subprocess.call("cp {} {}".format(os.path.join(hires_folder, pngs[0]), crops_folder), shell=True)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    project_dir = "/mnt/d/TestData/fostrap/FTIG/"
    project_dir = "/data/FTIG/"

    get_random_pngs(project_dir, chan=1, n=9)