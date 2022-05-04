#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from pal_navigation_msgs.msg import GoToPOIActionGoal,GoToPOIActionResult
from pal_navigation_msgs.msg import GoToPOIGoal
import time

def callback(status):
    rospy.loginfo(status.status)

def OneMove():
    pub_wp = rospy.Publisher('/poi_navigation_server/go_to_poi/goal', GoToPOIActionGoal, queue_size=1, latch=True)
    pub_st = rospy.Subscriber('/poi_navigation_server/go_to_poi/result', GoToPOIActionResult, callback)
      
    rospy.init_node('OneWay', anonymous=True)

    rospy.loginfo("Starting run_motion_python application...") #Write info to log file and command line
    rate = rospy.Rate(1) # Hz

    my_wp = GoToPOIActionGoal()
    my_st = GoToPOIActionResult()

    #while not rospy.is_shutdown():
    my_wp.header.seq = 3
    my_wp.header.frame_id = 'map'
    my_wp.goal.poi.data = 'Home'
    rospy.loginfo(my_wp)
    my_wp.header.stamp = rospy.Time.now()
    pub_wp.publish(my_wp)
    rate.sleep()
    
    result = my_st.status.status
    #while result!=3:
    #	result = my_st.status.status
    #	rospy.loginfo("Not there yet")
    #	rospy.loginfo(result)
	#if rospy.ROSInterruptException==True:
	#	break
    #r = rospy.sleep(10)    

    result = my_st.status.status
    if result == 3:
    	rospy.loginfo("At waypoint")
    

if __name__ == '__main__':
    try:
	OneMove()
    except rospy.ROSInterruptException:
	pass
