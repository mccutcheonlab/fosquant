# %%
import PIL as pil
from PIL import Image

import numpy as np
import javabridge
import bioformats as bf
javabridge.start_vm(class_path=bf.JARS)

path = "/mnt/d/TestData/fostrap/FTIG/FT108/rawdata/FT108_1A.vsi"
roipath = "/mnt/d/TestData/fostrap/FTIG/FT108/rawdata/FT108_1A_ROIs.zip"
# path = "/mnt/c/Github/fosquant/fosquant/result.tif"

path ="/data_temp/FT151/rawdata"

# %%
reader = bf.ImageReader(path)
omeMeta = bf.metadatatools.createOMEXMLMetadata()

reader.rdr.setId(path)
reader.rdr.setSeries(13)

im = reader.read(c=1, series=13, XYWH=(0,0,100,100))

# im = reader.rdr.openBytesXYWH(0,100, 100, 100, 100)
print(np.shape(im))
# image.shape=(3, 512, 512)
# image=image.transpose(1,2,0)
# img = Image.fromarray(image,'RGB')
# img.show(image)



javabridge.kill_vm()

# %%

img = Image.fromarray(im)
img.save("result2.png")
# %%

# with bf.ImageReader(path) as reader:
# # # reader.rdr.setFlattenedResolutions(False)
# # # get = reader.rdr.getSeriesCount(path)
#     im = reader.read()
#     print(type(im))
# # # im = reader.read(c=1, series=13, XYWH=(0,0,100,100))
#     print(type(reader))

#     print(np.shape(im))
# # your program goes here



