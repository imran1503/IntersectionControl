import sys
import math
import glob
import os
import numpy as np
import queue
import random


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

def get_speed(vehicle):
    vel = vehicle.get_velocity()
    return 3.6*math.sqrt(vel.x**2 + vel.y**2 + vel.z**2)

class VehiclePIDController():
    
    def __init__(self, vehicle, args_lateral, args_longitudinal, max_throttle=45, max_break=10, max_steering=10):
        self.max_break = max_break
        self.max_steering = max_steering
        self.max_throttle = max_throttle

        self.vehicle = vehicle
        self.world = vehicle.get_world()
        self.past_steering = self.vehicle.get_control().steer
        self.long_controller = PIDLongitudinalControl(self.vehicle, **args_longitudinal)
        self.lat_controller = PIDLateralControl(self.vehicle, **args_lateral)

    def run_step(self, target_speed, waypoint):
        acceleration = self.long_controller.run_step(target_speed)
        current_steering = self.lat_controller.run_step(waypoint)
        control = carla.VehicleControl()

        if acceleration>=0.0:
            control.throttle = min(abs(acceleration),self.max_throttle)
            control.brake = 0.0
        else:
            control.throttle = 0.0
            control.brake = min(abs(acceleration),self.max_break)

        if current_steering > self.past_steering+0.1:
            current_steering = self.past_steering+0.1

        elif current_steering<self.past_steering-0.1:
            current_steering = self.past_steering-0.1

        if current_steering>=0:
            steering = min(self.max_steering ,current_steering)
        else:
            steering = max(-self.max_steering, current_steering)

        control.steer = steering
        control.handle_brake = False
        control.manual_gear_shift = False
        self.past_steering = steering
            

        return control

class PIDLongitudinalControl():

    def __init__(self, vehicle, K_P=1.0, K_D=0.0, K_I=0.0, dt=0.03):
        self.vehicle = vehicle
        self.K_P = K_P
        self.K_D = K_D
        self.K_I = K_I
        self.dt = dt
        self.errorBuffer = queue.deque(maxlen = 10)

    def pid_controller(self,target_speed, current_speed):
        error = target_speed - current_speed

        self.errorBuffer.append(error)

        if len(self.errorBuffer)>=2:
            de = (self.errorBuffer[-1]-self.errorBuffer[-2])/self.dt
            ie = sum(self.errorBuffer)*self.dt

        else:
            de =0.0
            ie =0.0
        
        return np.clip(self.K_P*error+self.K_D*de+self.K_I*ie,-1.0,1.0)

    def run_step(self, target_speed):
        current_speed = get_speed(self.vehicle)
        return self.pid_controller(target_speed, current_speed)


class PIDLateralControl():

    def __init__(self, vehicle, K_P=1.0, K_D=0.0, K_I=0.0, dt=0.03):
        self.vehicle = vehicle
        self.K_P = K_P
        self.K_D = K_D
        self.K_I = K_I
        self.dt = dt
        self.errorBuffer = queue.deque(maxlen = 10)

    def pid_controller(self,waypoint, vehicle_transform):
            v_begin = vehicle_transform.location
            v_end = v_begin+carla.Location(x=math.cos(math.radians(vehicle_transform.rotation.yaw)),y=math.sin(math.radians(vehicle_transform.rotation.yaw)))
            v_vec = np.array([v_end.x - v_begin.x, v_end.y - v_begin.y,0.0])

            w_vec = np.array([waypoint.transform.location.x - v_begin.x, waypoint.transform.location.y - v_begin.y, 0.0])

            dot = math.acos(np.clip(np.dot(w_vec,v_vec)/np.linalg.norm(w_vec)*np.linalg.norm(v_vec), -1.0, 1.0))

            cross = np.cross(v_vec,w_vec)

            if cross[2]<0:
                dot*=-1

            self.errorBuffer.append(dot)

            if len(self.errorBuffer)>=2:
                de = (self.errorBuffer[-1]-self.errorBuffer[-2])/self.dt
                ie = sum(self.errorBuffer)*self.dt

            else:
                de = 0.0
                ie = 0.0

            return np.clip((self.K_P*dot)+(self.K_I*ie)+(self.K_D*de),-1.0,1.0)

    def run_step(self, waypoint):
        return self.pid_controller(waypoint,self.vehicle.get_transform())


def main():
    actorList = []
    try:
        #Connect to carla server and load map
        client = carla.Client('localhost', 2000)
        client.set_timeout(50.0)
        world = client.get_world()

        #Spawn Cybertruck Vehicle actor, add to actorList
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('cybertruck')[0]
        if not world.get_map().get_spawn_points():
            print('There are no spawn points available in your map/town.')
            print('Please add some Vehicle Spawn Point to your UE4 scene.')
            sys.exit(1)
        spawn_points = world.get_map().get_spawn_points()
        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        actorList.append(vehicle)

        args_Lateral = {'K_P': 1, 'K_D': 0.0, 'K_I': 0.0}
        args_Longitudinal = {'K_P': 1, 'K_D': 0.0, 'K_I': 0.0}
        control_vehicle = VehiclePIDController(vehicle,args_Lateral,args_Longitudinal)

        waypoints = world.get_map().generate_waypoints(1000)
        for w in waypoints:
            world.debug.draw_string(w.transform.location, 'O', draw_shadow=False,
                                          color=carla.Color(r=0, g=0, b=255), life_time=120.0,
                                          persistent_lines=True)

        while True:
            waypoints = world.get_map().get_waypoint(vehicle.get_location())
            waypoint = np.random.choice(waypoints.next(10))
            world.debug.draw_string(waypoint.transform.location, 'O', draw_shadow=False,
                                    color=carla.Color(r=255, g=0, b=0), life_time=120.0,
                                    persistent_lines=True)
            control_signal = control_vehicle.run_step(25,waypoint)
            vehicle.apply_control(control_signal)

            depth_camera_bp = blueprint_library.find('sensor.camera.semantic_segmentation')
            depth_camera_transform = carla.Transform(carla.Location(x=1.5,z=2.4))
            depth_camera = world.spawn_actor(depth_camera_bp,depth_camera_transform,attach_to=vehicle)
            #Save images from camera to output folder
            #depth_camera.listen(lambda image: image.#save_to_disk('output/%.6d.png'%image.frame,carla.ColorConverter.LogarithmicDepth))

    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in actorList])


if __name__ == '__main__':
    main()