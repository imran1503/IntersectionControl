from PIL import Image

# Open the image
image = Image.open('./data/segmentation/24635001.png')

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
      image.putpixel((x, y), (0, 255, 0))  # Green
    else:
        image.putpixel((x, y), (0, 0, 0))  # Black

# Save the modified image
image.save('driveSpace1.png')
print("Success in creating new image!")