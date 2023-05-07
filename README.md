# IntersectionControl

This is our 4th year project: Autonomous Vehicle Intersection Control: Yellow means Go Faster!

The goal of this project was to navigate an autonomous vehicle through a controlled intersection by following the calculated path. The vehicle has to determine the local and global environment which includes and is not limited to the cars, people and objects around it, the traffic light states, where we want to go (Turn left, Turn right, Go straight) and where the possible exits for the intersection are. The next step for the system is that it must create a path from the current position to the desired exit lane. After that the system must navigate the vehicle safely through the intersection.

This project heavily revolves around two primary programs. The first is CARLA https://github.com/carla-simulator/carla/releases . The other program was ROS as well as the ROS CARLA bridge. https://github.com/ros-visualization. More on how to install these programs can be found in the final report that is provided by the project coordinators. 

The project in its current state allows for a simulated vehicle in CARLA to move around and have the local and global enviroment captured in order for the system to be iterated on in order to add the next step of planning a path for the vehcile to follow. 

This repository holds all of the files that were used to make progress as well as some files provided from our simulator of choice: CARLA as test files we could run and learn from.

In this repository, there are python files used for both CARLA, MATLAB RoadRunner as well as ROS packages. 

Here is some of the key files that we made and learned from:
- first.py is just spawning our vehicle with a camera, lidar, and segmentation camera sensor attached. And spawn 20 other vehicles.
- second.py is adding a controller to our vehicle that we can send control to move our vehicle forward or steer or break
- driveSpaceTestAll.py should use the segmentation camera input images to convert them to black and white images where white is driveable space.
- carla_SLAM_ROS/src/createGloablMap.launch is a ROS launch file that is used to create a global occupancy grid map using ROS gmapping SLAM package.
- carla_SLAM_ROS/src/navigation.launch is a ROS launch file that was started to load our saved global map and attempt to localize that map with new lidar data using AMCL package.
