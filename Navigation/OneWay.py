#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from pal_navigation_msgs.msg import GoToPOIActionGoal
from pal_navigation_msgs.msg import GoToPOIGoal
import time


def OneMove():
    pub_wp = rospy.Publisher('/poi_navigation_server/go_to_poi/goal', GoToPOIActionGoal, queue_size=1)
      
    rospy.init_node('OneWay', anonymous=True)

    rospy.loginfo("Starting run_motion_python application...") #Write info to log file and command line
    rate = rospy.Rate(1) # Hz
    my_wp = GoToPOIActionGoal()
    #while not rospy.is_shutdown():
    my_wp.header.seq = 3
    my_wp.goal.poi.data = 'Team'
    rospy.loginfo(my_wp)
    my_wp.header.stamp = rospy.Time.now()
    pub_wp.publish(my_wp)
    rate.sleep()

    

if __name__ == '__main__':
    try:
	OneMove()
    except rospy.ROSInterruptException:
	   pass



