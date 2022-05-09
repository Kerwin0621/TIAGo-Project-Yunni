#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from pal_navigation_msgs.msg import GoToPOIActionGoal,GoToPOIActionResult
from pal_navigation_msgs.msg import GoToPOIGoal
import time



global atWaypoint
atWaypoint = False

def callback(status):

    global atWaypoint
    atWaypoint = True
    
    rospy.loginfo("I just arrived to the waypoint ")



def OneMove():

    global atWaypoint
    pub_wp = rospy.Publisher('/poi_navigation_server/go_to_poi/goal', GoToPOIActionGoal, queue_size=1, latch=True) 
    rospy.init_node('OneWay', anonymous=True)

    pub_st = rospy.Subscriber('/poi_navigation_server/go_to_poi/result', GoToPOIActionResult, callback)

    rospy.loginfo("Starting run_motion_python application...") #Write info to log file and command line
    rate = rospy.Rate(1) # Hz

    my_wp = GoToPOIActionGoal()
    my_st = GoToPOIActionResult()

    WP = ["Team","Home", "Team", "Home"]



    for j in range (0, len(WP)):
	    my_wp.header.seq = 3
	    my_wp.header.frame_id = 'map'
	    my_wp.goal.poi.data = WP[j]
	    rospy.loginfo(my_wp)
	    my_wp.header.stamp = rospy.Time.now()
	    pub_wp.publish(my_wp)
	    rate.sleep()
	    while atWaypoint == False:
		  rospy.loginfo("I am going there...")
            rospy.loginfo("Out of the waiting loop")
            atWaypoint = False
	
    rospy.spin()


    

if __name__ == '__main__':
    try:
	OneMove()
    except rospy.ROSInterruptException:
	pass

	
