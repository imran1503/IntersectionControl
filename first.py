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


    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town01')
    print(client.get_available_maps())

    blueprintLibrary = world.get_blueprint_library()
    vehicle_bp = blueprintLibrary.filter('cybertruck')[0]
    transform = carla.Transform(carla.Location(x=200, y=195, z=200), carla.Rotation(yaw=0))
    vehicle = world.spawn_actor(vehicle_bp, transform)
    print("Len pre Append" , (len(actorList)))
    actorList.append(vehicle)
    print("Len post Append" , len(actorList))

    time.sleep(15)


    print('delete actorList')
    if (len(actorList) != 0):
        client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    main()
