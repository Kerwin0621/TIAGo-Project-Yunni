#!/usr/bin/env python
# license removed for brevity

# System imports
import sys
import time
# ROS imports
import rospy
from actionlib import SimpleActionClient, GoalStatus
from play_motion_msgs.msg import PlayMotionAction, PlayMotionGoal
#-----------------------------------------------------------------------

from std_msgs.msg import String
from std_msgs.msg import Empty
from pal_navigation_msgs.msg import GoToPOIActionGoal,GoToPOIActionResult
from pal_navigation_msgs.msg import GoToPOIGoal
import time



global atWaypoint
atWaypoint = False

def wait_for_valid_time(timeout):
    """Wait for a valid time (non-zero), this is important
    when using a simulated clock"""
    # Loop until:
    # * ros master shutdowns
    # * control+C is pressed (handled in is_shutdown())
    # * timeout is achieved
    # * time is valid
    start_time = time.time()
    while not rospy.is_shutdown():
        if not rospy.Time.now().is_zero():
            return
        if time.time() - start_time > timeout:
            rospy.logerr("Timed-out waiting for valid time.")
            exit(0)
        time.sleep(0.1)
    # If control+C is pressed the loop breaks, we can exit
    exit(0)


def get_status_string(status_code):
    return GoalStatus.to_string(status_code)



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

    WP = ["Team"]



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


    rospy.loginfo("Starting run_motion_python application...") #Write info to log file and command line
    wait_for_valid_time(10.0) 

    client = SimpleActionClient('/play_motion', PlayMotionAction) # create an Action Client. Arguments ( [client name] , [Action server] )

    rospy.loginfo("Waiting for Action Server...") #Write info to log file and command line
    client.wait_for_server()

    #nombres = ["open_hand","wave","thumb_up","wave","look_dt_2","close_hand","home"]
    nombres = ["wave"]

    for j in range (0, len(nombres)):
    	movimiento = nombres[j]
    	goal = PlayMotionGoal() #Create a action goal object based upon the action definition
    	#goal.motion_name = sys.argv[1]
    	goal.motion_name = movimiento
    	goal.skip_planning = False
    	goal.priority = 0  # Optional

    	rospy.loginfo("Sending goal with motion: " + movimiento)
    	client.send_goal(goal)

    	rospy.loginfo("Waiting for result...")
    	action_ok = client.wait_for_result(rospy.Duration(30.0))

    	state = client.get_state()

    	if action_ok:
        	rospy.loginfo("Action finished succesfully with state: " + str(get_status_string(state)))
    	else:
        	rospy.logwarn("Action failed with state: " + str(get_status_string(state)))

#--------------------------------------------------------------------------
        if len(sys.argv) > 1:
		text=""
		for arg in sys.argv[1:]:
			text += arg + " "
	else:
		text = "Hello I am Yunni welcome to double tree hilton"
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



	
    rospy.spin()


    

if __name__ == '__main__':
    try:
	OneMove()
    except rospy.ROSInterruptException:
	pass

	
