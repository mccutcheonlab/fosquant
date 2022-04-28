# %%

import imagej
ij = imagej.init()

image_url = 'https://imagej.net/images/clown.jpg'
jimage = ij.io().open(image_url)

# Convert the image from ImageJ2 to xarray, a package that adds
# labeled datasets to numpy (http://xarray.pydata.org/en/stable/).
image = ij.py.from_java(jimage)

# Display the image (backed by matplotlib).
ij.py.show(image, cmap='gray')
# %%

# ij.py.run_macro("D://Test Data//histology//fostrappilot//fistrapmacro.ijm")
# %%

macro = """
file = "D:/Test Data/histology/fostrappilot/FTP01_A2.vsi"
run("Bio-Formats", "open=[file] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_5");
"""

ij.py.run_macro(macro)
# %%
import imagej
ij = imagej.init('sc.fiji:fiji:2.0.0-pre-10', mode=imagej.Mode.GUI)
ij.getVersion()

#%%

from jnius import autoclass
WindowManager = autoclass('ij.WindowManager')
ij.ui().showUI()

# https://github.com/uw-loci
# https://forum.image.sc/t/implementing-bio-formats-importer-with-pyimagej/62425
# %%
file = "D:/Test Data/histology/fostrappilot/FTP01_A2.vsi"
# Open the image using ImageJ (more precisely: Bio-Formats via SCIFIO).
ijImage = ij.io().open(file)
# Slice out the Z=37 plane.
# ijSlice = ij.op().transform().hyperSliceView(ijImage, 2, 37)
# # What kind of thing is this?
# type(ijSlice)
# %%
image_url = 'https://imagej.net/images/clown.jpg'
jimage = ij.io().open(image_url)
# %%
