#!/usr/bin/env python
# license removed for brevity

# [LIBRARIES IMPORT] -------------------------------------------------------------------------


## System imports 
import sys
import time
import rospy

## Kinematics imports 
from actionlib import SimpleActionClient, GoalStatus
from play_motion_msgs.msg import PlayMotionAction, PlayMotionGoal

## Navigation imports
from std_msgs.msg import String
from std_msgs.msg import Empty
from pal_navigation_msgs.msg import GoToPOIActionGoal,GoToPOIActionResult
from pal_navigation_msgs.msg import GoToPOIGoal


## Text to Speech 
from actionlib import SimpleActionClient
from pal_interaction_msgs.msg import TtsAction, TtsGoal

## Speech Recognition

#----------------------------------------------------------------------------------------------


# [ GLOBAL VARIABLES ]-------------------------------------------------------------------------
global atWaypoint, movementDone, speechDone
atWaypoint = False
movementDone = False
speechDone =  False
#----------------------------------------------------------------------------------------------



# [Functions declaration] --------------------------------------------------------------------

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





## [Call back functions] -----------------------------------------------------------------------


# Kinematics Call back function triggered when action 
def callbackKin(state, result):
    rospy.loginfo(result)
    rospy.loginfo("Kinematics finished with State:" + str(get_status_string(state)) + ", Result: " + str(result))


# Navigation Call back function triggered when subscriber node message is received
def callbackNav(state): 

    global atWaypoint 
    atWaypoint = True
    rospy.loginfo("I just arrived to the waypoint! ")


# TTS Call back function triggered when action 
def callbackTts(state, result):
    rospy.loginfo(result)
    rospy.loginfo("Text to Speech just finished with State::" + str(get_status_string(state)) + ", Result: " + str(result))

## Call back functions -----------------------------------------------------------------------



## [Wait function] -----------------------------------------------------------------------
def wait2Finish(client_kin, client_tts,time2break):
    # Get intial state of the action interfaces to compare
    state_kin = client_kin.get_state()
    state_tts = client_tts.get_state()

    # Display intial state of the actions
    rospy.loginfo("Wait2Finish Fucntion. State Kinematics:")
    rospy.loginfo(state_kin)
    rospy.loginfo("Wait2Finish Fucntion. State TTS:")
    rospy.loginfo(state_tts)

    # Timeout limit declaration
    timeout = rospy.get_time() + time2break
    timeoutFlag = 0
    count = 0

    while not (state_kin == 3 and state_tts == 3 ):
        # Refresh action states to compare
        state_kin = client_kin.get_state()
        state_tts = client_tts.get_state()
	
        #display message every other time
	if count > 50000:
        	rospy.loginfo("waiting for actions to finish ...")
		count = 0
	count = count + 1
        
        #time out to get out of loop
        now = rospy.get_time()
        #rospy.loginfo(now)
        #rospy.loginfo(timeout)
	if  now > timeout:
           rospy.loginfo("Timeout Exception!")
           timeoutFlag = 1
	   break
    if timeoutFlag != 1:
        rospy.loginfo("Actions just finished, What's next????")

        rospy.loginfo("Wait2Finish Fucntion_After! State Kinematics:")
        rospy.loginfo(state_kin)
        rospy.loginfo("Wait2Finish Fucntion_After! State TTS:")
        rospy.loginfo(state_tts)

## -----------------------------------------------------------------------


## [Subsystems Functions] -----------------------------------------------------------------------


# Kinematics Function
def doKinematics(movement,client_kin):

        #Create a action goal object based upon the action definition
	goal_kin = PlayMotionGoal() 
    	goal_kin.motion_name = movement
    	goal_kin.skip_planning = False
    	goal_kin.priority = 0  # Optional

        # [Kinematics]  Send action goal
    	rospy.loginfo("Sending goal with motion: " + movement)
    	client_kin.send_goal(goal_kin, callbackKin)



# Text to Speech Function
def doTts(phrase, waitTime,client_tts):

        # Create a goal to say our sentence
        goal_tts = TtsGoal()
        goal_tts.rawtext.text = phrase
        goal_tts.rawtext.lang_id = "en_GB"
        goal_tts.wait_before_speaking = waitTime

        # [TTS] Send the goal and wait
        rospy.loginfo("I'll say: " + phrase)        
        client_tts.send_goal(goal_tts, callbackTts)


## -----------------------------------------------------------------------




def integrated():

    global atWaypoint
    
    # Node initialization
    rospy.init_node('OneWay', anonymous=True) #this node

    #Log info application
    rospy.loginfo("Starting TIAGo Integrated application...") #Write info to log file and command line
    rate = rospy.Rate(1) # Hz rate
    wait_for_valid_time(10.0) 


    # [Kinematics] --> Connect to the play motion action server
    client_kin = SimpleActionClient('/play_motion', PlayMotionAction) # create an Action Client. Arguments ( [client name] , [Action server] )
    rospy.loginfo("Waiting for play_motion Action Server...") #Write info to log file and command line while waiting 
    client_kin.wait_for_server()

    # [Navigation] --> Nodes initialization
    pub_wp = rospy.Publisher('/poi_navigation_server/go_to_poi/goal', GoToPOIActionGoal, queue_size=1, latch=True) #POI pusblisher node
    pub_st = rospy.Subscriber('/poi_navigation_server/go_to_poi/result', GoToPOIActionResult, callbackNav) # subscriber POI_goal node
    #   --> Action objects creation
    my_wp = GoToPOIActionGoal() #Action goal object creation
    my_st = GoToPOIActionResult() #Action result object creation

    # [Text To Speech] --> Connect to the text-to-speech action server
    client_tts = SimpleActionClient('/tts', TtsAction)
    rospy.loginfo("Waiting for TTS Action Server...") #Write info to log file and command line while waiting 
    client_tts.wait_for_server()






    ## [Data Definition] ---------------------------------------------------------------------
       
    # Define movements list
    #movements = ["home","open_hand","wave","thumb_up","wave","look_dt_2","home","point_elevator"]
    #movements = ["close_hand", "open_hand"]
    movements = ["wave"]
    
    # Define messages list
    phrases = ["phrase_1","phrase_2"]

    # Define waypoint list
    # XXXXXX

    ## ---------------------------------------------------------------------



    for j in range (0, len(movements)):
        
        #Send out Kinematics action Goal
	doKinematics(movements[j],client_kin)

        #Send out Text to speech action Goal
	doTts(phrases[j],0,client_tts)

        #Wait for action goals to finish
    	rospy.loginfo("Waiting for result...")
        wait2Finish(client_kin,client_tts, 10)


    rospy.spin()


if __name__ == '__main__':
    try:
	integrated()
    except rospy.ROSInterruptException:
	pass

	
