# IntersectionControl

This is our 4th year project: Intersection Control: Yellow means Go Faster!

This repository holds all of the files that were used to make progress as well as some files provided from our simulator of choice: CARLA as test files we could run and learn from.

In this repository, there are python files used for both CARLA, MATLAB RoadRunner as well as ROS packages. 

Here is some of the key files that we made and learned from:
- first.py is just spawn our vehicle with camera, lidar, segmentation camera sensor attached. And spawn 20 other vehicles
- second.py is adding a controller to our vehicle that we can send control to move our vehicle forward or steer or break
- driveSpaceTestAll.py should use the segmentation camera input images on convert them to black and white images where white is driveable space.

After that is was working with ROS in order to convert the data from the sensors in the simulator into data that we can process and decide where to go on from. 
