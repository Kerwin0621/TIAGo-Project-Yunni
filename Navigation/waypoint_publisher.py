#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
import time
import tf
from std_msgs.msg import Empty

"""
user:~$ rosmsg show geometry_msgs/PoseWithCovarianceStamped                                                                                                               
std_msgs/Header header                                                                                                                                                    
  uint32 seq                                                                                                                                                              
  time stamp                                                                                                                                                              
  string frame_id                                                                                                                                                         
geometry_msgs/PoseWithCovariance pose                                                                                                                                     
  geometry_msgs/Pose pose                                                                                                                                                 
    geometry_msgs/Point position                                                                                                                                          
      float64 x                                                                                                                                                           
      float64 y                                                                                                                                                           
      float64 z                                                                                                                                                           
    geometry_msgs/Quaternion orientation                                                                                                                                  
      float64 x                                                                                                                                                           
      float64 y                                                                                                                                                           
      float64 z                                                                                                                                                           
      float64 w                                                                                                                                                           
  float64[36] covariance 
"""

def talker():
    pub_wp = rospy.Publisher('/my_tiago_waypoints', PoseWithCovarianceStamped, queue_size=1)
    
    pub_init_wp = rospy.Publisher('/path_ready', Empty, queue_size=1)
    
    rospy.init_node('waypoint_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    my_wp = PoseWithCovarianceStamped()
    my_wp.header.stamp = rospy.Time.now()
    my_wp.header.frame_id = "/map"
    
    
    init_value = 2.0
    
    roll = 0
    pitch = 0
    yaw = 0.7
    quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    #type(pose) = geometry_msgs.msg.Pose
    my_wp.pose.pose.orientation.x = quaternion[0]
    my_wp.pose.pose.orientation.y = quaternion[1]
    my_wp.pose.pose.orientation.z = quaternion[2]
    my_wp.pose.pose.orientation.w = quaternion[3]


    for i in range(5):
        rospy.loginfo(str(i))
        my_wp.pose.pose.position.x = float(i) + init_value 
        my_wp.pose.pose.position.y = float(i) + init_value
        
        while not rospy.is_shutdown():
            connections = pub_wp.get_num_connections()
            if connections > 0:
                pub_wp.publish(my_wp)
                break
            rospy.loginfo("Waiting for /my_tiago_waypoints topic")
            rate.sleep()
        rospy.loginfo("Published waypoint number ="+str(i))
        time.sleep(2)
    
    start_command = Empty()
    
    while not rospy.is_shutdown():
            connections = pub_init_wp.get_num_connections()
            if connections > 0:
                pub_init_wp.publish(start_command)
                rospy.loginfo("Sent waypoint list execution command")
                break
            rospy.loginfo("Waiting for /path_ready topic")
            rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

