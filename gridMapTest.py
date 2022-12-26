import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Capture the RGB camera sensor data
image = Image.open('driveSpace1.png')
image = image.convert('RGB')

# Convert the image to grayscale
image = image.convert("L")

# Threshold the image to create a binary map
threshold = 0.2
image = np.array(image)
image[image > threshold] = 1
image[image <= threshold] = 0

# The image is now a 2D numpy array representing the grid map

# Create a 2D numpy array
data = np.array(image)

# Plot the array using imshow
plt.imshow(data, cmap='gray')

# Add axis labels and tick marks
plt.xlabel("X")
plt.ylabel("Y")

plt.show()
print("Success in creating new plot!")

