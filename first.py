import glob
import os
import sys
import random
import time
import numpy as np

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
        world = client.get_world()
        print(client.get_available_maps())

        #Spawn Cybertruck Vehicle actor, add to actorList
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

        #Add Camera sensor to Vehicle
        camera_bp = blueprintLibrary.find('sensor.camera.rgb')
        camera_bp.set_attribute("image_size_x", str(800))
        camera_bp.set_attribute("image_size_y", str(600))
        camera_bp.set_attribute("fov", str(90))
        camera_transform = carla.Transform(carla.Location(x=1.5,z=2.4))
        camera = world.spawn_actor(camera_bp,camera_transform,attach_to=vehicle)
        #Save images from camera to output folder
        camera.listen(lambda image: image.save_to_disk('output/%d064.png'%image.frame))

        #Spawn multiple random vehicles with autopilot
        for _ in range(0,20):
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
                print('created%s'%npc.type_id)

        #Wait 120 seconds
        time.sleep(120)
    
    finally:  
        #Destory all the actors  
        print('delete actorList')
        if (len(actorList) != 0):
            client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    main()
