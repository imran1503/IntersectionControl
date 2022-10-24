import glob
import os
import sys
import cv2
import random
import matplotlib.pyplot as plt
import time
import numpy as np
import argparse

try:
  sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' %(
    sys.version_info.major,
    sys.version_info.minor,
    'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
  pass

import carla 

def main():
  actorList = []
  try:

    client = carla.Client('localhost',2000)
    client.set_timeout(10.0)
    world = client.load_world('Town01')
    print(client.get_available_maps())

    blueprintLibrary = world.get_blueprint_library()
    vehicle_bp = blueprintLibrary.filter('cybertruck')[0]
    transform = carla.Transform(carla.Location(x=130,y=195,z=40),carla.Rotation(yaw=0))
    vehicle = world.spawn_actor(vehicle_bp,transform)
    actorList.append(vehicle)

  finally:
    print('delete actorList')
    client.applybatch([carla.command.DestroyActor(x) for x in actorList])


if _name_ == '_main_':
  main()