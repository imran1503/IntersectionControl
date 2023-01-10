from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import io

# Open the image
image = Image.open('./data/segmentation/24630001.png')

# Get the width and height of the image
width, height = image.size
image = image.convert('RGB')

# Iterate over all pixels in the image
for x in range(width):
  for y in range(height):
    # Get the pixel at the current position
    pixel = image.getpixel((x, y))

    roadColor = (128, 64, 128)
    laneColor = (157, 234, 50)
    
    # Check if the pixel matches the specific RGB value
    if (pixel == roadColor) or (pixel == laneColor):
      # Convert the pixel to a different color
      if(pixel == roadColor):
        image.putpixel((x, y), (255, 255, 255))  # White
    else:
        image.putpixel((x, y), (0, 0, 0))  # Black

# Save the modified image
image.save('driveSpace1.png')
print("Success in creating new image!")

def driveForward(image):
    canDriveForward = True

    # Get the width and height of the image
    width, height = image.size
    image = image.convert('RGB')
    buffer = 50
    interable = 10
    multiplier = 0
    x = int(width/2)
    vehicleWidth = 100
    i = 0
    plt.figure()
    plt.imshow(image)

    while(canDriveForward):
            y = int(height - (multiplier*interable) - buffer)
            pixel = image.getpixel((x, y))
            pixel2 = image.getpixel((x, (y - (multiplier*interable+1))))
            pixel3 = image.getpixel((x, (y - (multiplier*interable+2))))
            white = (255, 255, 255)
            laneColor = (157, 234, 50)

            #Check a row of pixels from the middle of the image using half of vehicle width
            clearRow = True
            halfWidth = int(vehicleWidth/2)
            for j in range(-halfWidth,halfWidth):
                pixel = image.getpixel((x+j, y))
                pixel2 = image.getpixel((x+j, (y - (multiplier*interable+1))))
                pixel3 = image.getpixel((x+j, (y - (multiplier*interable+2))))
                if(((pixel != white) and (pixel != laneColor)) or ((pixel2 != white) and (pixel2 != laneColor)) or ((pixel3 != white) and (pixel3 != laneColor))):
                    clearRow = False
                
            # Check if the pixel matches the specific RGB value
            if ((y - (multiplier*interable+2))<0) and clearRow :
                plt.scatter(x, y, s=10, c='red', marker='x')
                multiplier += 1
            else:
                canDriveForward = False

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')

    image = Image.open(img_buf)
    print("Moved Forward "+str(i)+" times. Can Not drive more forward.")
    image.save('driveSpace2.png')
    #plt.show()

image = Image.open("driveSpace1.png")
driveForward(image)