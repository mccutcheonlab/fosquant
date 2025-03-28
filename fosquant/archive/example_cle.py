import pyclesperanto_prototype as cle
from skimage.io import imread, imsave

# initialize GPU
device = cle.select_device("Quadro")
print("Used GPU: ", device)

import pyclesperanto_prototype as cle
from skimage.io import imread, imsave
import numpy as np

image = np.asarray(imread("..//data//multichannel3.tif"))

# image = np.transpose(image, (2, 0, 1)) #transpose so that Z is first dimension
print(image.shape)

image = image[:,:,:,1]

result_image = None
test_image = cle.push(image)
result_image = cle.extended_depth_of_focus_variance_projection(test_image, result_image, radius_x=2, radius_y=2, sigma=10)

print(result_image.shape)

cle.imshow(result_image)
# imsave("result.tif", result_image)

# # # process the image
# # inverted = cle.subtract_image_from_scalar(image, scalar=255)
# # blurred = cle.gaussian_blur(inverted, sigma_x=1, sigma_y=1)
# # binary = cle.threshold_otsu(blurred)
# # labeled = cle.connected_components_labeling_box(binary)

# # # The maxmium intensity in a label image corresponds to the number of objects
# # num_labels = cle.maximum_of_all_pixels(labeled)

# print(result_image.shape)


# cle.imshow(result_image)
# # print out result
# print("Num objects in the image: " + str(num_labels))

# save image to disc
# imsave("result_image.tif", labeled)