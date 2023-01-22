from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import io
import math

# Open the image
image = Image.open('./data/segmentation/7107001.png')
segmentedImage = image

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

def turnRight(image):
    canDriveForward = True

    # Get the width and height of the image
    width, height = image.size
    image = image.convert('RGB')
    buffer = 50
    interable = 10
    multiplier = 0
    x = int(width-15)
    vehicleWidth = 50
    i = 0

    with image.convert("RGBA") as base:

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        # get a font
        fnt = ImageFont.truetype("arial.ttf", 20)
        # get a drawing context
        d = ImageDraw.Draw(txt)

        y = int(height - buffer)
        pixel = image.getpixel((x, y))
        pixel2 = image.getpixel((x, (y - interable)))
        roadEdgeColor = (244, 35, 232)
        roadColor = (128, 64, 128)

        #Check a row of pixels from the middle of the image using half of vehicle width
        roadEdge = True
        while(roadEdge and ((y - ((multiplier+1)*interable))<height)):
            pixel = image.getpixel((x, y))
            pixel2 = image.getpixel((x, (y - ((multiplier+1)*interable))))
            if( (pixel == roadEdgeColor) or (pixel2 == roadEdgeColor) ):
                roadEdgeFound = True
                while(roadEdgeFound and ((y - ((multiplier+1)*interable))<height)):
                    pixel = image.getpixel((x, y))
                    pixel2 = image.getpixel((x, (y - ((multiplier+1)*interable))))
                    y -= 1
                    if( (pixel == roadColor) and (pixel2 == roadColor)):
                        roadEdgeFound = False
                        roadEdge = False
                        i += 1
            y -= 1
            
        # Check if the pixel matches the specific RGB value
        trajectory = []
        pathPoints = 20
        forwardMargin = 0.25
        rightMargin = 0.25
        x1 = 0
        y1 = 0
        x2 = width/2
        y2 = height - buffer
        trajectory.append((x2,y2))

        rightLocation = (0,0)
        currentLocation = (x2, y2)
        if ((y - ((multiplier+2)*interable))>0):
            # draw text, half opacity
            x -= 10
            y -= 20
            d.text((x, y), "x", font=fnt, fill=(255, 0, 0, 255))
            x1 = x
            y1 = y
            d.text(currentLocation, "x", font=fnt, fill=(255, 0, 0, 255))

        else:
            canDriveForward = False

        if(x1 != 0):
            deltaY = y2 - y1
            deltaX = x1 - x2
            tempY = 0
            tempX = 0
            forwardMove = int(forwardMargin*pathPoints)
            rightMove = int(rightMargin*pathPoints)
            curvePoints = int( (1-(rightMargin+forwardMargin)) * pathPoints)

            x = x2 
            y = y2
            for i in range(forwardMove):
                tempY = y - ((i+1)*(deltaY/forwardMove)*(forwardMargin*2))
                d.text((x, tempY), "x", font=fnt, fill=(255, 0, 0, 255))
                trajectory.append((x,tempY))

            x3 = x
            y3 = tempY
            x = x1
            y = y1
            for i in range(rightMove):
                tempX = x - ((i+1)*(deltaX/rightMove)*(rightMargin*2))
                d.text((tempX, y), "x", font=fnt, fill=(255, 0, 0, 255))
                trajectory.append((tempX,y))

            x4 = tempX
            y4 = y

            x = x4
            y = y4
            for i in range(int(rightMove/2)):
                tempX = x - ((i+1)*(deltaX/rightMove)*(rightMargin*2))
                d.text((tempX, y), "x", font=fnt, fill=(255, 0, 0, 255))
                trajectory.append((tempX,y))

            radius = ((x4 - x3) + (y3 - y4)) / 2
            curve = int(curvePoints)
            deltaY = (y3 - y4)
            deltaX = (x4 - x3)

            y = y3
            for i in range(curve):
                tempY = y - (i+1)*(deltaY/curve)
                tempX = x4 - math.sqrt((radius*radius)-((y-tempY)*(y-tempY))) - 40 + (i*5)
                d.text((tempX, tempY), "x", font=fnt, fill=(255, 0, 0, 255))
                trajectory.append((tempX,tempY))
            
            #x = x4
            #for i in range(curve):
                #tempX = x - (i+1)*(deltaX/curve)
                #tempY = y3 - math.sqrt((radius*radius)-((x - tempX)*(x-tempX))) + 50
                #d.text((tempX, tempY), "x", font=fnt, fill=(255, 0, 0, 255))
                #trajectory.append((tempX,tempY))
            

        out = Image.alpha_composite(base, txt)
        out.show()
        out.save('driveRight1.png')

def driveForward(image):
    canDriveForward = True

    # Get the width and height of the image
    width, height = image.size
    image = image.convert('RGB')
    buffer = 50
    interable = 10
    multiplier = 0
    x = int(width/2)
    vehicleWidth = 50
    i = 0

    with image.convert("RGBA") as base:

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # get a font
        fnt = ImageFont.truetype("arial.ttf", 15)
        # get a drawing context
        d = ImageDraw.Draw(txt)

        while(canDriveForward):
            y = int(height - (multiplier*interable) - buffer)
            pixel = image.getpixel((x, y))
            pixel2 = image.getpixel((x, (y - ((multiplier+1)*interable))))
            pixel3 = image.getpixel((x, (y - ((multiplier+2)*interable))))
            white = (255, 255, 255)
            laneColor = (157, 234, 50)

            #Check a row of pixels from the middle of the image using half of vehicle width
            clearRow = True
            halfWidth = int(vehicleWidth/2)
            for j in range(-halfWidth,halfWidth):
                pixel = image.getpixel((x+j, y))
                pixel2 = image.getpixel((x+j, (y - ((multiplier+1)*interable))))
                pixel3 = image.getpixel((x+j, (y - ((multiplier+2)*interable))))
                if(((pixel != white) and (pixel != laneColor)) or ((pixel2 != white) and (pixel2 != laneColor)) or ((pixel3 != white) and (pixel3 != laneColor))):
                    clearRow = False
                
            # Check if the pixel matches the specific RGB value
            if ((y - ((multiplier+2)*interable))>0) and clearRow :
                # draw text, half opacity
                d.text((x, y), "x", font=fnt, fill=(0, 0, 0, 255))
                multiplier += 1
                i += 1
                
                
            else:
                canDriveForward = False
                

        out = Image.alpha_composite(base, txt)

        out.show()

        print("Moved Forward "+str(i)+" times. Can Not drive more forward.")
        out.save('driveSpace2.png')

image = Image.open("driveSpace1.png")
#driveForward(image)
turnRight(segmentedImage)