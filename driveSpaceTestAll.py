import glob
import os
import sys
import random
import time
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import cv2

try:
    sys.path.append(glob.glob('../../../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


class driveSpaceTestAll():
    def __init__(self):
        self.IM_HEIGHT = 800
        self.IM_WIDTH = 600
        self.FOV = 110
        self.StoredImage = None
        self.firstImage = True
        self.fig = None
        self.ax = None
        self.myPlot = None

    def processImage(self, image):
        i = np.array(image.raw_data)
        i2 = i.reshape((self.IM_HEIGHT, self.IM_WIDTH, 4))
        i3 = i2[:, :, :3]
        cv2.imshow("", i3)
        cv2.waitKey(1)
        image.save_to_disk('data/rgb/%d001.png' % image.frame)
        return i3 / 255.0

    def driveForward(self, image):
        canDriveForward = True

        # Get the width and height of the image
        width, height = image.size
        image = image.convert('RGB')
        vehicleWidth = 50
        buffer = 50
        interable = 10
        multiplier = 0
        x = int(width/2)
         # get a drawing context
        d = ImageDraw.Draw(image)

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
                    d.text((x, y), "x", font=fnt, fill=(255, 0, 0, 255))
                    multiplier += 1
               
                else:
                    canDriveForward = False
                    
            out = Image.alpha_composite(base, txt)
            return out

    def plotGrid(self):
        #Add trajectory on image for driving forward
        image = self.driveForward(self.StoredImage)

        # Convert the image to grayscale
        image = image.convert("L")

        # Threshold the image to create a binary map
        threshold = 0.2
        image = np.array(image)
        image[image > threshold] = 1
        image[image <= threshold] = 0

        # Create a 2D numpy array
        data = np.array(image)

        if self.firstImage:
            # Set up figure and 2D axis

            self.fig, self.ax = plt.subplots()

            # Plot the array using imshow
            self.myPlot = self.ax.imshow(data, cmap='gray')

            # Add axis labels and tick marks
            plt.xlabel("X")
            plt.ylabel("Y")

            plt.ion()
            plt.pause(0.1)
            self.firstImage = False
            print("Plot created!")

        else:
            # Update plot data
            self.myPlot.set_data(data)
            plt.pause(0.1)

    def driveSpaceConversion(self):
        width, height = self.StoredImage.size
        image = self.StoredImage.convert('RGB')

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
                    image.putpixel((x, y), (255, 255, 255))  # White
                else:
                    image.putpixel((x, y), (0, 0, 0))  # Black

        # Save the modified image
        self.StoredImage = image
        # image.save('D:/CARLA_0.9.13/WindowsNoEditor/PythonAPI/examples/IntersectionControlSystemGit/IntersectionControlSystem/data/driveSpace/%d001.png' % frameNumber)

    def processSegmentedImage(self, image):
        frameNumber = image.frame
        image.save_to_disk('data/segmentation/%d001.png' % frameNumber, carla.ColorConverter.CityScapesPalette)
        self.StoredImage = Image.open(
            'D:/CARLA_0.9.13/WindowsNoEditor/PythonAPI/examples/IntersectionControl/data/segmentation/%d001.png' % frameNumber)

        self.driveSpaceConversion()
        self.plotGrid()

    def main(self):
        actorList = []
        try:
            # Connect to carla server and load Town01 map
            client = carla.Client('localhost', 2000)
            client.set_timeout(10.0)
            world = client.get_world()

            # Spawn Cybertruck Vehicle actor, add to actorList
            blueprintLibrary = world.get_blueprint_library()
            vehicle_bp = blueprintLibrary.filter('model3')[0]
            if not world.get_map().get_spawn_points():
                print('There are no spawn points available in your map/town.')
                print('Please add some Vehicle Spawn Point to your UE4 scene.')
                sys.exit(1)
            spawn_points = world.get_map().get_spawn_points()
            spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
            vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
            vehicle.set_autopilot(True)
            actorList.append(vehicle)

            # Add Camera rgb sensor to Vehicle
            camera_bp = blueprintLibrary.find('sensor.camera.rgb')
            camera_bp.set_attribute("image_size_x", f"{self.IM_HEIGHT}")
            camera_bp.set_attribute("image_size_y", f"{self.IM_WIDTH}")
            camera_bp.set_attribute("fov", f"{self.FOV}")
            camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
            rgbCamera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
            # Save images from camera to output folder
            rgbCamera.listen(lambda image: self.processImage(image))

            # Add Camera depth sensor to Vehicle
            camera_bp = blueprintLibrary.find('sensor.camera.depth')
            camera_bp.set_attribute("image_size_x", f"{self.IM_HEIGHT}")
            camera_bp.set_attribute("image_size_y", f"{self.IM_WIDTH}")
            camera_bp.set_attribute("fov", f"{self.FOV}")
            camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
            depthCamera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
            print("\nAdded depth sensor\n")
            # Save images from camera to output folder
            depthCamera.listen(
                lambda image: image.save_to_disk('data/depth/%d001.png' % image.frame, carla.ColorConverter.Depth))

            # Add Camera segmentation sensor to Vehicle
            camera_bp = blueprintLibrary.find('sensor.camera.semantic_segmentation')
            camera_bp.set_attribute("image_size_x", f"{self.IM_HEIGHT}")
            camera_bp.set_attribute("image_size_y", f"{self.IM_WIDTH}")
            camera_bp.set_attribute("fov", f"{self.FOV}")
            camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
            segmentationCamera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
            print("\nAdded segmentation sensor\n")

            # Save images from camera to output folder

            segmentationCamera.listen(lambda image: self.processSegmentedImage(image))

            # Spawn multiple random vehicles with autopilot
            for _ in range(0, 10):
                bp = blueprintLibrary.filter('vehicle.*')[0]
                if not world.get_map().get_spawn_points():
                    print('There are no spawn points available in your map/town.')
                    print('Please add some Vehicle Spawn Point to your UE4 scene.')
                    sys.exit(1)
                spawn_points = world.get_map().get_spawn_points()
                spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
                npc = world.try_spawn_actor(bp, spawn_point)
                actorList.append(vehicle)

                if npc is not None:
                    actorList.append(npc)
                    npc.set_autopilot(True)
                    print('created%s' % npc.type_id)

            # Wait 10 seconds
            time.sleep(60)
            plt.ioff()

        finally:
            # Destory all the actors
            print('delete actorList')
            if (len(actorList) != 0):
                client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    driveSpaceTestAll().main()
