# TIAGo - Navigation

This document describes the TIAGo performing navigation function. 



## Sensor Visuaization

Initially, the map should be built by Rviz, 

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.129
rosrun rviz rviz -d `rospack find tiago_bringup`/config/tiago.rviz
```

Moving the robot by the controller to detect the boundary and build the map

## SLAM

On the development computer, change the navigation mode to MAP

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.129
rosservice call /pal_navigation_sm "input: 'MAP'"
```

Visualizing the map in Rviz, run

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.129
rosrun rviz rviz -d `rospack find tiago_2dnav`/config/rviz/navigation.rviz
```

Then save the map by command

```
rosrun map_server map_saver
rosservice call /pal_map_manager/save_map "directory: ''"
```

Change the navigation model to Localization

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.129
rosservice call /pal_navigation_sm "input: 'LOC'"
```



## Localization and Path Planning 

```
export ROS_MASTER_URI=http://tiago-146c:11311
export ROS_IP=10.68.0.129
rosrun rviz rviz -d `rospack find tiago_2dnav`/config/rviz/navigation.rviz
```



## Pal_waypoint

```
Node [/pal_waypoint]
Publications: 
 * /diagnostics [diagnostic_msgs/DiagnosticArray]
 * /pal_waypoint/navigate/feedback [pal_waypoint_msgs/DoWaypointNavigationActionFeedback]
 * /pal_waypoint/navigate/result [pal_waypoint_msgs/DoWaypointNavigationActionResult]
 * /pal_waypoint/navigate/status [actionlib_msgs/GoalStatusArray]
 * /poi_navigation_server/go_to_poi/cancel [actionlib_msgs/GoalID]
 * /poi_navigation_server/go_to_poi/goal [pal_navigation_msgs/GoToPOIActionGoal]
 * /rosout [rosgraph_msgs/Log]

Subscriptions: 
 * /pal_waypoint/navigate/cancel [actionlib_msgs/GoalID]
 * /pal_waypoint/navigate/goal [pal_waypoint_msgs/DoWaypointNavigationActionGoal]
 * /poi_navigation_server/go_to_poi/feedback [pal_navigation_msgs/GoToPOIActionFeedback]
 * /poi_navigation_server/go_to_poi/result [pal_navigation_msgs/GoToPOIActionResult]
 * /poi_navigation_server/go_to_poi/status [actionlib_msgs/GoalStatusArray]

Services: 
 * /pal_waypoint/get_loggers
 * /pal_waypoint/set_logger_level


contacting node http://tiago-146c:39803/ ...
Pid: 23163
Connections:
 * topic: /rosout
    * to: /ros_fluentd_logger
    * direction: outbound (51741 - 10.68.0.1:35088) [12]
    * transport: TCPROS
 * topic: /rosout
    * to: /rosout
    * direction: outbound (51741 - 10.68.0.1:35136) [10]
    * transport: TCPROS
 * topic: /diagnostics
    * to: /pal_diagnostic_aggregator
    * direction: outbound (51741 - 10.68.0.1:35134) [13]
    * transport: TCPROS
 * topic: /pal_waypoint/navigate/result
    * to: /rviz_1651579996763492890
    * direction: outbound (51741 - 10.68.0.131:48790) [23]
    * transport: TCPROS
 * topic: /pal_waypoint/navigate/feedback
    * to: /rviz_1651579996763492890
    * direction: outbound (51741 - 10.68.0.131:48788) [17]
    * transport: TCPROS
 * topic: /pal_waypoint/navigate/status
    * to: /rviz_1651579996763492890
    * direction: outbound (51741 - 10.68.0.131:48782) [16]
    * transport: TCPROS
 * topic: /poi_navigation_server/go_to_poi/goal
    * to: /poi_navigation_server
    * direction: outbound (51741 - 10.68.0.1:35182) [14]
    * transport: TCPROS
 * topic: /poi_navigation_server/go_to_poi/cancel
    * to: /poi_navigation_server
    * direction: outbound (51741 - 10.68.0.1:35188) [11]
    * transport: TCPROS
 * topic: /pal_waypoint/navigate/goal
    * to: /rviz_1651579996763492890 (http://10.68.0.131:42951/)
    * direction: inbound (44130 - 10.68.0.131:47391) [18]
    * transport: TCPROS
 * topic: /pal_waypoint/navigate/cancel
    * to: /rviz_1651579996763492890 (http://10.68.0.131:42951/)
    * direction: inbound (44136 - 10.68.0.131:47391) [25]
    * transport: TCPROS
 * topic: /poi_navigation_server/go_to_poi/status
    * to: /poi_navigation_server (http://tiago-146c:45127/)
    * direction: inbound (57544 - tiago-146c:39125) [19]
    * transport: TCPROS
 * topic: /poi_navigation_server/go_to_poi/feedback
    * to: /poi_navigation_server (http://tiago-146c:45127/)
    * direction: inbound (57548 - tiago-146c:39125) [21]
    * transport: TCPROS
 * topic: /poi_navigation_server/go_to_poi/result
    * to: /poi_navigation_server (http://tiago-146c:45127/)
    * direction: inbound (57546 - tiago-146c:39125) [20]
    * transport: TCPROS

```



rosmsg show DoWaypointNavigationActionGoal

```
[pal_waypoint_msgs/DoWaypointNavigationActionGoal]:
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
actionlib_msgs/GoalID goal_id
  time stamp
  string id
pal_waypoint_msgs/DoWaypointNavigationGoal goal
  string group
  uint32 first_wp
  int32 num_wp
  bool continue_on_error

```

rostopic echo /poi_navigation_server/go_to_poi/goal   (You need to open the Rviz first, then run the group of waypoint, the goal of waypoint will be displayed)

```
header: 
  seq: 3
  stamp: 
    secs: 1651581513
    nsecs: 390239512
  frame_id: ''
goal_id: 
  stamp: 
    secs: 1651581513
    nsecs: 390239626
  id: "/pal_waypoint-4-1651581513.390239626"
goal: 
  poi: 
    data: "Home"
---
header: 
  seq: 4
  stamp: 
    secs: 1651581513
    nsecs: 494033853
  frame_id: ''
goal_id: 
  stamp: 
    secs: 1651581513
    nsecs: 494034024
  id: "/pal_waypoint-5-1651581513.494034024"
goal: 
  poi: 
    data: "Team"
---
header: 
  seq: 5
  stamp: 
    secs: 1651581524
    nsecs: 298608868
  frame_id: ''
goal_id: 
  stamp: 
    secs: 1651581524
    nsecs: 298609048
  id: "/pal_waypoint-6-1651581524.298609048"
goal: 
  poi: 
    data: "Home"
```

rostopic info /poi_navigation_server/go_to_poi/goal

```
Type: pal_navigation_msgs/GoToPOIActionGoal

Publishers: 
 * /pal_waypoint (http://tiago-146c:36649/)

Subscribers: 
 * /poi_navigation_server (http://tiago-146c:36547/)
 * /rostopic_5858_1651581701085 (http://10.68.0.131:35223/)
```

/pal_waypoint     is a node



Publish a topic:

rostopic pub /poi_navigation_server/go_to_poi/goal pal_navigation_msgs/GoToPOIActionGoal:

```
rostopic pub -1 /poi_navigation_server/go_to_poi/goal pal_navigation_msgs/GoToPOIActionGoal "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
goal_id:
  stamp:
    secs: 0
    nsecs: 0
  id: ''
goal:
  poi:
    data: 'Home'" 
```







