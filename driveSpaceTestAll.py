import glob
import os
import sys
import random
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import threading


try:
    sys.path.append(glob.glob('../../../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

IM_HEIGHT = 800
IM_WIDTH = 600
FOV = 110



def processImage(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    image.save_to_disk('data/rgb/%d001.png' % image.frame)
    return i3 / 255.0


def gridPlot(image):
    image = image.convert('RGB')


def processSegmentedImage(image):
    frameNumber = image.frame
    image.save_to_disk('data/segmentation/%d001.png' % frameNumber, carla.ColorConverter.CityScapesPalette)
    image = Image.open('D:/CARLA_0.9.13/WindowsNoEditor/PythonAPI/examples/IntersectionControlSystemGit/IntersectionControlSystem/data/segmentation/%d001.png' % frameNumber)
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
    #image.save('D:/CARLA_0.9.13/WindowsNoEditor/PythonAPI/examples/IntersectionControlSystemGit/IntersectionControlSystem/data/driveSpace/%d001.png' % frameNumber)

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

def main():
    actorList = []
    try:
        # Connect to carla server and load Town01 map
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()

        # Spawn Cybertruck Vehicle actor, add to actorList
        blueprintLibrary = world.get_blueprint_library()
        vehicle_bp = blueprintLibrary.filter('cybertruck')[0]
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
        camera_bp.set_attribute("image_size_x", f"{IM_HEIGHT}")
        camera_bp.set_attribute("image_size_y", f"{IM_WIDTH}")
        camera_bp.set_attribute("fov", f"{FOV}")
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        rgbCamera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        # Save images from camera to output folder
        rgbCamera.listen(lambda image: processImage(image))

        # Add Camera depth sensor to Vehicle
        camera_bp = blueprintLibrary.find('sensor.camera.depth')
        camera_bp.set_attribute("image_size_x", f"{IM_HEIGHT}")
        camera_bp.set_attribute("image_size_y", f"{IM_WIDTH}")
        camera_bp.set_attribute("fov", f"{FOV}")
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        depthCamera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        print("\nAdded depth sensor\n")
        # Save images from camera to output folder
        depthCamera.listen(
            lambda image: image.save_to_disk('data/depth/%d001.png' % image.frame, carla.ColorConverter.Depth))


        # Add Camera segmentation sensor to Vehicle
        camera_bp = blueprintLibrary.find('sensor.camera.semantic_segmentation')
        camera_bp.set_attribute("image_size_x", f"{IM_HEIGHT}")
        camera_bp.set_attribute("image_size_y", f"{IM_WIDTH}")
        camera_bp.set_attribute("fov", f"{FOV}")
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        segmentationCamera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        print("\nAdded segmentation sensor\n")
        # Save images from camera to output folder

        segmentationCamera.listen(lambda image: processSegmentedImage(image))

        # Spawn multiple random vehicles with autopilot
        for _ in range(0, 5):
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
        time.sleep(20)

    finally:
        # Destory all the actors
        print('delete actorList')
        if (len(actorList) != 0):
            client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    main()