#!/usr/bin/env python


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
global atWaypoint, movementDone, speechDone, NavCondition
atWaypoint = False
movementDone = False
speechDone =  False
NavCondition = " "
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
    rospy.loginfo("Navigation Callback: I just arrived to the waypoint! ")


# TTS Call back function triggered when action 
def callbackTts(state, result):
    rospy.loginfo(result)
    rospy.loginfo("Text to Speech just finished with State::" + str(get_status_string(state)) + ", Result: " + str(result))
    check = str(result)
    if check == "error_code: -42" :
	rospy.loginfo("I cannot move my head. Please turn off the head manager!")
       

## Call back functions -----------------------------------------------------------------------



## [Wait functions] -----------------------------------------------------------------------
def wait2FinishHRI(client_kin, client_tts,time2break):
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


def wait2FinishNav(time2break):
    global atWaypoint

    # Timeout limit declaration
    timeout = rospy.get_time() + time2break
    timeoutFlag = 0
    count = 0

    rospy.loginfo("Entered the waiting loop")

    count = 0

    while atWaypoint == False:
        if count > 50000:
            rospy.loginfo("On my way there ...")
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
        rospy.loginfo("Out of the waiting loop")
    atWaypoint = False


## ---------------------------------------------------------------------------------------------


## [Subsystems Functions] -----------------------------------------------------------------------


# Kinematics Function
def doKinematics(movement,client_kin):
        global NavCondition

        #Create a action goal object based upon the action definition
	goal_kin = PlayMotionGoal() 
    	goal_kin.motion_name = movement
    	goal_kin.skip_planning = False
    	goal_kin.priority = 0  # Optional

        # [Kinematics]  Send action goal
    	rospy.loginfo("Sending goal with motion: " + movement)
    	client_kin.send_goal(goal_kin, callbackKin)
        
        #Update position navigation condition
        NavCondition = movement



# Speaking Function
def doTts(phrase, waitTime,client_tts):

        # Create a goal to say our sentence
        goal_tts = TtsGoal()
        goal_tts.rawtext.text = phrase
        goal_tts.rawtext.lang_id = "en_GB"
        goal_tts.wait_before_speaking = waitTime

        # [TTS] Send the goal and wait
        rospy.loginfo("I'll say: " + phrase)        
        client_tts.send_goal(goal_tts, callbackTts)


# Navigation Function
def doNavigation(waypoint, my_wp, pub_wp, rate):

        # Create a goal for the waypoint
	my_wp.header.seq = 3
	my_wp.header.frame_id = 'map'
	my_wp.goal.poi.data = waypoint
	rospy.loginfo(my_wp)
	my_wp.header.stamp = rospy.Time.now()

        # [Navigation] Send the goal
        rospy.loginfo("I'll go to: " + waypoint)        
        pub_wp.publish(my_wp)
	rate.sleep()

## -----------------------------------------------------------------------




def integrated():

    global atWaypoint, NavCondition
    count = 0
    
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
    #movements = ["open_hand","wave","wave","look_dt_2","home","thumb_up","close_hand","home"]
    movements_1 = ["open_hand","wave","thumb_up","wave","look_dt_2","close_hand","home"]
    movements_2 = ["chin_up","point_elevator","search_below","chin_up","home","close_hand","chin_up"]
    #movements = ["look_dt_2"]

    # Define time Exceptions
    timeExceptions_1 = [20, 30, 4, 20, 30, 4, 30]
    timeExceptions_2 = [6, 40, 40, 10, 30, 5, 10]

    
    # Define messages list

    #phrases = ["phrase 1","phrase 2","phrase 3","phrase 4","phrase 5","phrase 6"]
    #phrases = ["phrase 1"]

    phrases_1 = ["Hello everybody! It's a pleasure to meet you",
                 "It is great to see you here.......How are you today?",
                 "My name is TIAGo",
                 "I am a Robot",
                 "Welcome to the Double tree Hotel by Hilton",
                 "Would you like a drink?",
                 "Let me get ready to walk you to the Red dot Bar, it'll take just a second"]

    phrases_nav_1 = ["OK", "Please follow me. I will show you the way","Almost there guys"]

    phrases_2 = [ "Okay, we are here",
                 "This is the Bar. Here you can get a nice drink, ................ I wish I could take a pint of pale oil, but I am not allowed to drink while working",
                 "Please, get yourselves confortable. One of my robot friends will bring you a drink. Humn? Where is this little guy? It should be around here",
                 "Anyways, I hope you have a good time",
                 "I'll just get ready to get back to the reception",
                 "see you all later",
		  " "]


    phrases_nav_2 = ["OK", "I am going back to work","Almost there"]


    # Phrase timings
    phraseTime_1 = [3, 3, 5, 3, 3, 3, 3]
    phraseTime_2 = [3, 3, 0, 1, 0, 0, 0]
    #phraseTime = [3]

    # Define waypoint list

    #waypoints = ["Home","A","B","Home"]
    waypoints_1 = ["Reception","RedDot"]
    waypoints_2 = ["RedDot","Reception"]

    ## --------------------------------------------------------------------------------------


    ## [Data Execution] ---------------------------------------------------------------------

    #Movements_1
    if len(movements_1)==len(phrases_1) and len(phraseTime_1)==len(phrases_1) and len(timeExceptions_1)==len(phrases_1):
	    for j in range (0, len(movements_1)):
		
		#Send out Kinematics action Goal
		doKinematics(movements_1[j],client_kin)

		#Send out Text to speech action Goal
		doTts(phrases_1[j],phraseTime_1[j],client_tts)

		#Wait for action goals to finish
	    	rospy.loginfo("Waiting for result...")
		wait2FinishHRI(client_kin, client_tts, timeExceptions_1[j])
    else:
            rospy.loginfo("Number of phrases not equal to number of movements!")
    
    #Navigation_1
    if NavCondition == "home": # Only move if it is at home position, for safety.

	    for i in range (0, len(waypoints_1)):
		    doTts(phrases_nav_1[i],1,client_tts)
		    doNavigation(waypoints_1[i], my_wp, pub_wp, rate)
		    wait2FinishNav(60)
            NavCondition == " "
    else:
            rospy.loginfo("Not in Home (body position), I am not moving man. It is dangerous!")
            rospy.loginfo(NavCondition)

    #Movements_2
    if len(movements_2)==len(phrases_2) and len(phraseTime_2)==len(phrases_2) and len(timeExceptions_2)==len(phrases_2):
	    for j in range (0, len(movements_2)):
		
		#Send out Kinematics action Goal
		doKinematics(movements_2[j],client_kin)

		#Send out Text to speech action Goal
		doTts(phrases_2[j],phraseTime_2[j],client_tts)

		#Wait for action goals to finish
	    	rospy.loginfo("Waiting for result...")
		wait2FinishHRI(client_kin, client_tts, timeExceptions_2[j])

    else:
            rospy.loginfo("Number of phrases_2 not equal to number of movements!")


    #Navigation_2

    NavCondition = "home"
    if NavCondition == "home": # Only move if it is at home position, for safety.


	    for i in range (0, len(waypoints_2)):
		    doTts(phrases_nav_2[i],1,client_tts)
		    doNavigation(waypoints_2[i], my_wp, pub_wp, rate)
		    wait2FinishNav(60)
            NavCondition == " "
    else:
            rospy.loginfo("Not in Home (body position), I am not moving man. It is dangerous!")
            rospy.loginfo(NavCondition)



    rospy.loginfo("Program finished successfully")
    rospy.spin()


if __name__ == '__main__':
    try:
	integrated()
    except rospy.ROSInterruptException:
	pass

	
