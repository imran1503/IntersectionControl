from PIL import Image

class driveableSpaceTest2:
    # Open the image
    image = None;
    imageID = None;
    def __init__(self, imageID):
        self.image = Image.open('./data/segmentation/' + imageID +'.png')
        self.image = imageID

    def changeImage(self, imageID):
        self.image = Image.open('./data/segmentation/' + imageID +'.png')
        self.image = imageID

    def analyse(self):
        # Get the width and height of the image
        width, height = self.image.size
        image = self.image.convert('RGB')

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
                    self.image.putpixel((x, y), (0, 255, 0))  # Green
                else:
                    self.image.putpixel((x, y), (0, 0, 0))  # Black

        # Save the modified image
        image.save('driveSpace_'+ self.imageID + '.png')
        print("Success in creating new image!")
