# IntersectionControl

This is our 4th year project: Intersection Control: Yellow means Go Faster!

This repository holds all of the files that were used to make progress as well as some files provided from our simulator of choice: CARLA as test files we could run and learn from.

In this repository, there are python files used for both CARLA, MATLAB RoadRunner as well as ROS packages. 

Here is some of the key files that we made and learned from:
- first.py is just spawning our vehicle with a camera, lidar, and segmentation camera sensor attached. And spawn 20 other vehicles.
- second.py is adding a controller to our vehicle that we can send control to move our vehicle forward or steer or break
- driveSpaceTestAll.py should use the segmentation camera input images to convert them to black and white images where white is driveable space.
- carla_SLAM_ROS/src/createGloablMap.launch is a ROS launch file that is used to create a global occupancy grid map using ROS gmapping SLAM package.
- carla_SLAM_ROS/src/navigation.launch is a ROS launch file that was started to load our saved global map and attempt to localize that map with new lidar data using AMCL package.
