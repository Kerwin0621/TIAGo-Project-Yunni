# TIAGo

# Reboot

## ssh connection

All changes done outside of / home will only take effect until the robot is rebooted. In order to do permanent changes, we need to connect the TIAGo robot.

```
ssh pal@tiago-0c
Password: pal
su (get into the root) 
Password: palroot
```

## Source

```
source /opt/pal/ferrum/setup.bash
```

## IP Address

```
ip r (to get the ip-address)
```

## ROS IP & Master URI

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.1
```

ping to check the network IP response. 

```
ping 10.68.0.1
```



## Web command

```
http://10.68.0.1:8080
```



## Update

```
pal_upgrade
```



Firmware Update

```
rosrun firmware_update_robot update_firmware.sh
```





# ROS Package

## Environment

```
source /opt/pal/ferrum/setup.bash

# Create a work space
mkdir -p ~/example_ws/src
cd example_ws/src

# Create a catkin package
catkin_create_pkg hello_world roscpp
```

## CPP file

```c++
//ROS headers
#include<ros/ros.h>
#include <std_msgs/String.h>

// C++ std headers
#include <iostream>

nt main(int argc, char** argv)
{
	ros::init(argc, argv, "hello_world");
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<std_msgs::String>(“hello”, 10);
    std_msgs::String msg;
	ros::Rate rate(1.0); //1 Hz rate
    while ( ros::ok() )
	{
		msg.data = “hello world”;
		pub.publish(msg);
		rate.sleep();
	}
return 0;
}
```

## CMakeList file

```
cmake_minimum_required(VERSION 2.8.3)
project(hello_world)

find_package(catkin REQUIRED COMPONENTS roscpp)

catkin_package()

include_directories(
${catkin_INCLUDE_DIRS}
)

## Declare a C++ executable
add_executable(hello_world_node src/hello_world_node.cpp)
target_link_libraries(hello_world_node ${catkin_LIBRARIES})

## Mark executables and/or libraries for installation
install(TARGETS hello_world_node
RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
```



## Build & Execution

```
cd example_ws
catkin build

# Open a new terminal
roscore

# Run the node in the former terminal
source devel/setup.bash
rosrun hello_world hello_world_node

# Run a new terminal
rostopic echo /hello
```



## Deploy the package

```
cd example_ws
rosrun pal_deploy deploy.py --user pal tiago-146c
```





## PY file

```python
#!/usr/bin/env python
# license removed for brevity

import rospy
from ros_basics_tutorials.msg import SensorIO
import random

#creating a new publisher(we specify the topic name, then type of message then the queue size)
pub = rospy.Publisher('sensor_io_topic', SensorIO, queue_size=10)

#we need to initialize the node
rospy.init_node('sensor_io_publisher_node', anonymous=True)

#set the loop rate
rate = rospy.Rate(1) #1hz 1 message per second

#keep publishing until a Ctrl-C is pressed
i = 0

while not rospy.is_shutdown():
	sensor_io = SensorIO()
	sensor_io.id = 1
	sensor_io.name = "io_parking_01"
	sensor_io.temperature = 24.33 + (random.random()*2)
	sensor_io.humidity = 33.41 + (random.random()*2)
	rospy.loginfo("I publish: ")
	rospy.loginfo(sensor_io)
	pub.publish(sensor_io)
	rate.sleep()
	i = i + 1
```

### PY Hello_world

```python
import rospy
from std_msgs.msg import String

def talker():
    
   # chatter (Topic name) String (String type defined in ROS) queue_size =10(buffer for waiting until u get 10 msgs)
    pub = rospy.Publisher('chatter', String, queue_size=10) 
    
    # Initilisation of the ros node talker (name of the node) anonymous=True (every node created with unique ID for each node)
    rospy.init_node('talker', anonymous=True)
    
    rate = rospy.Rate(1) # 1hz 1 message per second
    
    i = 0
    while not rospy.is_shutdown(): 
        hello_str = "Hello World %s " %i
        rospy.loginfo(hello_str)
        pub.publish(hello_str) #publishing the message
        rate.sleep() # To sleep for 1 second
        i = i + 1
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
```





# Moving the Robot

## Key board

Moving with key board

```
rosrun key_teleop key_teleop.py
```



## Velocity command

Moving with velocity command

```
rostopic pub /mobile_base_controller/cmd_vel geometry_msgs/Twist "linear:
  x: 0.5
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0" -r 3
```

```
rostopic pub /mobile_base_controller/cmd_vel geometry_msgs/Twist -r 3 -- '[0.5,0.0,0.0]' '[0.0, 0.0, 0.0]'
```





# Functions

## Motion Planning

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.1 
roslaunch tiago_moveit_config moveit_rviz.launch config:=true
```



## Text-to-Speech

```
rostopic pub /tts/goal pal_interaction_msgs/TtsActionGoal "header: {}
goal_id: {}
goal:
	text: {}
	rawtext:
		text: 'Hello world'
		lang_id: 'en_GB'
	speakerName: ''
	wait_before_speaking: 0.0" --once
```

### Python Scripts

```python
#!/usr/bin/env python
import sys
import rospy
from actionlib import SimpleActionClient
from pal_interaction_msgs.msg import TtsAction, TtsGoal
if __name__ == '__main__':
rospy.init_node('say_something')
if len(sys.argv) > 1:
text = ""
for arg in sys.argv[1:]:
text += arg + " "
else:
text = "I like talking to people"
rospy.loginfo("I'll say: " + text)
# Connect to the text-to-speech action server
client = SimpleActionClient('/tts', TtsAction)
client.wait_for_server()
# Create a goal to say our sentence
goal = TtsGoal()
goal.rawtext.text = text
goal.rawtext.lang_id = "en_GB"
# Send the goal and wait
client.send_goal_and_wait(goal)
```









# Navigation

```
rostopic pub -r 5 /mobile_base_controller/cmd_vel geometry_msgs/Twist '{linear::{x: 0.1, y:0.0, z: 0.0}, angular:{x: 0.0, y: 0.0, z: 0.5}}'
```





## Rviz

 Most of TIAGo ’s sensor readings can be visualised in rviz. In order to start the rviz GUI with a pre-defined configuration, execute the following from the development computer:

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.1 
rosrun rviz rviz -d `rospack find tiago_bringup`/config/tiago.rviz
```



## Laser Range-Finder

```
rostopic hz /scan
subscribed to [/scan]
average rate: 14.992
	min: 0.064s max: 0.069s std dev: 0.00105s window: 15
```

Inspecting the topic message

```
rostopic echo -n 1 /scan --noarr
```

## Sonars

TIAGo is equipped with 3 rear ultrasonic sensors Devantech SRF05 

Frequency 40 kHz

Measuring Distance 0.03 - 4 m



To get the information sonar_base topic

```
rostopic echo /sonar_base
```



## IMU

TIAGo is equipped with a InvenSense 6-axis MPU-6050 IMU

IMU measurements are published in /base_imu topic:

```
rostopic echo /base_imu
```



## RGB-D Camera

TIAGo is equipped with an Orbbec Astra RGB-D camera



Visualization from command line (from a development computer):

```
rosrun image_view image_view image:=/xtion/rgb/image_raw _image_transport:=compressed
```

Visualization using rqt GUI:

```
rosrun rqt_image_view rqt_image_view
```

NP: select the image topic to visualise. It is recommended to select compressed image transport to reduce bandwidth and latency

It also can be visualise in Rvize



### Image Subscriber

Ref:http://wiki.ros.org/image_transport/Tutorials/SubscribingToImages

​	  http://wiki.ros.org/image_transport/Tutorials/ExaminingImagePublisherSubscriber#Running_the_Subscriber



## Point Cloud Processing

Ref: http://wiki.ros.org/pcl/Tutorials



## Stereo Microphones

Two sound cards can be detected in TIAGo

```
arecord -I
```

For test the Andrea Stereo Microphones

```
arecord -f cd -d 10 -D hw:1,0 micro.wav
```

10 seconds of audio will be recorded. In order to playback the wav file:

```
aplay micro.wav
```



## Force Torque Sensor 

Check sensor reading 

```
rostopic echo /wrist_ft
```

To visualize the sensor reading in Rviz you must add a WrenchStamped visualizer





# Topics

In Rviz

Laser Scan : /scan

RGBD: /xtion/rgb/image_rect_color

Point CLoud: /throttle_filtering_points/filtered_points

Depth Image: /xtion/depth/image_raw

Sonar: /sonar_base





# Error

```
PluginlibFactory: The plugin for class 'pal-waypoint_rviz_plugins/Point of Interest' failed to load.  Error: According to the loaded plugin descriptions the class pal-waypoint_rviz_plugins/Point of Interest with base class type rviz::Tool does not exist. Declared types are  rviz/FocusCamera rviz/Interact rviz/Measure rviz/MoveCamera rviz/PublishPoint rviz/Select rviz/SetGoal rviz/SetInitialPose rviz_plugin_tutorials/PlantFlag
```



asdsadasd

