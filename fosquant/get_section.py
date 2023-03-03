import numpy as np
from skimage.util import img_as_uint
import javabridge
import bioformats as bf

myloglevel="ERROR"

def get_section_from_vsi(path, dims, chan, series_hires=8):

    dims = check_bounds(path, dims, series_hires)

    with bf.ImageReader(path) as reader:
        planes = []
        for z in range(3):
            im = reader.read(c=chan, z=z, series=series_hires, XYWH=dims)
            planes.append(im)

    img = np.dstack(planes)
    img = img_as_uint(img)

    return img

def check_bounds(path, dims, series):

    dims = list(dims)

    myXML = bf.get_omexml_metadata(path)
    o = bf.OMEXML(myXML)
    X = o.image(series).Pixels.get_SizeX()
    Y = o.image(series).Pixels.get_SizeY()

    if X < (dims[0] + dims[2]):
        dims[0] = X - dims[2]

    if Y < (dims[1] + dims[3]):
        dims[1] = Y - dims[3]

    return tuple(dims)