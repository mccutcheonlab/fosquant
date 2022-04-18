import os

from cellpose import io, models

def cell_counts():
    image_files = [os.path.join("rawdata", f) for f in os.listdir("rawdata")]

    model = models.Cellpose(gpu=False, model_type='cyto')

    channels = [1,0] # IF YOU HAVE GRAYSCALE
    imgs = [io.imread(filename) for filename in image_files]

    masks, flows, styles, diams = model.eval(imgs, diameter=30, channels=channels, resample=False)
    io.masks_flows_to_seg(imgs, masks, flows, diams, image_files, channels)
    io.save_to_png(imgs, masks, flows, image_files)

if __name__ == "__main__":
    cell_counts()