import sys

import numpy as np
import cv2
from matplotlib import pyplot as plt
from m6bk import *

np.random.seed(1)
np.set_printoptions(precision=2, threshold=sys.maxsize)

dataset_handler = DatasetHandler()
dataset_handler.current_frame
image = dataset_handler.image
plt.imshow(image)

k = dataset_handler.k
depth = dataset_handler.depth
plt.imshow(depth, cmap='jet')
segmentation = dataset_handler.segmentation
plt.imshow(segmentation)
plt.show()
colored_segmentation = dataset_handler.vis_segmentation(segmentation)
plt.imshow(colored_segmentation)
plt.show()



dataset_handler.set_frame(2)
dataset_handler.current_frame


image = dataset_handler.image
plt.imshow(image)



# xy_from_depth
def xy_from_depth(depth, k):
    """
    Computes the x, and y coordinates of every pixel in the image using the depth map and the calibration matrix.

    Arguments:
    depth -- tensor of dimension (H, W), contains a depth value (in meters) for every pixel in the image.
    k -- tensor of dimension (3x3), the intrinsic camera matrix

    Returns:
    x -- tensor of dimension (H, W) containing the x coordinates of every pixel in the camera coordinate frame.
    y -- tensor of dimension (H, W) containing the y coordinates of every pixel in the camera coordinate frame.
    """

    # Get the shape of the depth tensor
    H, W, channels = depth.shape
    print ("H= "+str(H))
    print("W= "+str(W))

    # Grab required parameters from the K matrix
    f, cu, cv = k[0, 0], k[0, 2], k[1, 2]

    # Generate a grid of coordinates corresponding to the shape of the depth map
    x = np.zeros((H, W))
    y = np.zeros((H, W))

    # Compute x and y coordinates
    xa = np.arange(1, W + 1, 1)
    ya = np.arange(1, H + 1, 1)
    u, v = np.meshgrid(xa, ya)

    x = (u - cu).dot(depth) / f
    y = (v - cv).dot(depth) / f

    return x, y


dataset_handler.set_frame(0)
k = dataset_handler.k

z = dataset_handler.depth

print("K: " + str(k))
#print("xy_from_depth(z, k): " + str(xy_from_depth(z, k)))
x, y = xy_from_depth(z, k)

print('x[599, 799] = ' + str(x[599, 599,2]))
print('y[599, 799] = ' + str(y[599, 599,2]))
print('z[599, 799] = ' + str(z[599, 599,2]) + '\n')

print('x[400,500] = ' + str(x[400, 500,2]))
print('y[400,500] = ' + str(y[400, 500,2]))
print('z[400,500] = ' + str(z[400, 500,2]) + '\n')

# Get road mask by choosing pixels in segmentation output with value 7
road_mask = np.zeros(segmentation.shape)
road_mask[segmentation == 7] = 1

# Show road mask
plt.imshow(road_mask)
plt.show()

# Get x,y, and z coordinates of pixels in road mask
x_ground = x[road_mask == 1]
y_ground = y[road_mask == 1]
z_ground = dataset_handler.depth[road_mask == 1]
xyz_ground = np.stack((x_ground, y_ground, z_ground))