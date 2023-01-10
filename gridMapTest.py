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

#plt.show()
#print("Success in creating new plot!")

def driveForward(image):
    canDriveForward = True

    # Get the width and height of the image
    width, height = image.size
    image = image.convert('RGB')
    buffer = 50
    interable = 20
    multiplier = 0

    while(canDriveForward):
        x = int(width/2)
        y = int(height - (multiplier*interable) - buffer)
        pixel = image.getpixel((x, y))

        white = (255, 255, 255)

        # Check if the pixel matches the specific RGB value
        if (pixel == white) or (y < 0):
            for i in range(5):
                for j in range(5):
                    image.putpixel((x+i, y+j), (255, 0, 0))  # convert pixel to red

            multiplier += 1
        else:
            canDriveForward = False
    
    print("Moved Forward "+str(i)+" times. Can Not drive more forward.")
    image.save('driveSpace2.png')

########################################################################
image = Image.open("driveSpace1.png")
driveForward(image)
# Create a 2D numpy array
data = np.array(image)

# Plot the array using imshow
plt.imshow(data, cmap='gray')

# Add axis labels and tick marks
plt.xlabel("X")
plt.ylabel("Y")

plt.show()
print("Success in creating new plot!")    