import glob
import os
import sys
import random
import matplotlib.pyplot as plt
import time
import numpy as np
import argparse

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


def main():
    actorList = []
    try:
        #Connect to carla server and load Town01 map
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.load_world('Town01')
        print(client.get_available_maps())

        #Spawn Cybertruck Vehicle actor, add to actorList
        blueprintLibrary = world.get_blueprint_library()
        vehicle_bp = blueprintLibrary.filter('cybertruck')[0]
        transform = carla.Transform(carla.Location(x=200, y=195, z=10), carla.Rotation(yaw=0))
        vehicle = world.try_spawn_actor(vehicle_bp, transform)
        print("Len pre Append" , (len(actorList)))
        actorList.append(vehicle)
        print("Len post Append" , len(actorList))

        #Add Camera sensor to Vehicle
        camera_bp = blueprintLibrary.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=1.5,z=2.4))
        camera = world.spawn_actor(camera_bp,camera_transform,attach_to=vehicle)
        #Save images from camera to output folder
        camera.listen(lambda image: image.save_to_disk('output/%d064.png'%image.frame))

        #Spawn multiple random vehicles with autopilot
        for _ in range(0,100):
            transform.location.x += 8.0
            bp = blueprintLibrary.filter('vehicle.*')[0]
            npc = world.try_spawn_actor(bp,transform)

            if npc is not None:
                actorList.append(npc)
                npc.set_autopilot(True)
                print('created%s'%npc.type_id)

        #Wait 15 seconds
        time.sleep(15)
    
    finally:  
        #Destory all the actors  
        print('delete actorList')
        if (len(actorList) != 0):
            client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    main()
