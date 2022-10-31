import sys
import math
import glob
import os
import numpy as np
import cv2
import queue


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

class VehiclePIDController():
    
    def __init__(self, vehicle, args_lateral, args_longitudinal, max_throttle=0.75, max_break=0.3, max_steering=0.8):
        self.max_break = max_break
        self.max_steering = max_steering
        self.max_throttle = max_throttle

        self.vehicle = vehicle
        self.world = vehicle.get_world()
        self.long_controller = PIDLongitudinalControl(self.vehicle, **args_longitudinal)
        self.lat_controller = PIDLateralControl(self, **args_lateral)

class PIDLongitudinalControl():

    def __init__(self, vehicle, K_P=1.0, K_D=0.0, K_I=0.0, dt=0.03):
        self.vehicle = vehicle
        self.K_P = K_P
        self.K_D = K_D
        self.K_I = K_I
        self.errorBuffer = queue.deque(maxLen = 10)

class PIDLateralControl():

    def __init__(self, vehicle, K_P=1.0, K_D=0.0, K_I=0.0, dt=0.03):
        self.vehicle = vehicle
        self.K_P = K_P
        self.K_D = K_D
        self.K_I = K_I
        self.errorBuffer = queue.deque(maxLen = 10)

def main():
    actorList = []
    try:
        #Connect to carla server and load map
        client = carla.Client('localhost', 2000)
        client.set_timeout(50.0)
        world = client.get_world()

        #Spawn Cybertruck Vehicle actor, add to actorList
        blueprintLibrary = world.get_blueprint_library()
        vehicle_bp = blueprintLibrary.filter('cybertruck')[0]
        spawnpoint = carla.Transform(carla.Location(x=-75.4, y=-1.0, z=15), carla.Rotation(pitch=0,yaw=0))
        vehicle = world.try_spawn_actor(vehicle_bp, spawnpoint)
        actorList.append(vehicle)

        control_vehicle = VehiclePIDController(vehicle,args_latera={'K_P':1, 'K_D':0.0})

        while True:
            waypoints = world.get_map().get_waypoints(vehicle.get_location())
            waypoint = np.random.choice(waypoints(0.3))
            #control_signal = 

    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    main()