import os
from urllib.error import HTTPError

from cellpose import io, models

def get_masks(image_files, model_type, channels, diameter, suffix):
    imgs = [io.imread(f) for f in image_files]
    channels = channels
    try:    
        model = models.Cellpose(gpu=False, model_type=model_type)
        masks, flows, styles, diams = model.eval(imgs, channels=channels, diameter=diameter, resample=False)  
    except HTTPError:
        model = models.CellposeModel(gpu=False, model_type=model_type)
        masks, flows, styles, = model.eval(imgs, channels=channels, diameter=diameter, resample=False)  
        diams = [diameter]*len(imgs)

    print(diams)
    base = [os.path.splitext(f)[0] for f in image_files]
    filenames = ["{}_{}.jpg".format(f, suffix) for f in base]

    io.masks_flows_to_seg(imgs, masks, flows, diams, filenames, channels)
    io.save_to_png(imgs, masks, flows, filenames)

def cell_counts():
    image_files = [os.path.join("cellcounts", f) for f in os.listdir("cellcounts") if ".jpg" in f]
    
    get_masks(image_files, "cyto", [1,0], 15, "trap")
    get_masks(image_files, "tissuenet", [2,0], 9, "fos")

if __name__ == "__main__":
    cell_counts()