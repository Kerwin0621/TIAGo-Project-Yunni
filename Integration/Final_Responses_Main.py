# Developers: Kshitij Raje(S372042) ; Sudhanshu Upadhye (S376055), Msc Robotics 2021-22 Cranfield University
#!/usr/bin/env python2

import sys
import rospy
from actionlib import SimpleActionClient
from pal_interaction_msgs.msg import TtsAction, TtsGoal
import speech_recognition as sr

assistant = ["hello", "hi", "hola", "hey"]
reception = ["reservation", "booking", "room"]
bar = ["bar", "drink", "food"]
timing = ["open", "close", "opening", "closing"]
connection = ["Wi-Fi"]
thanking = ["thank you", "thanks"]
laugh = ["joke"]
farewell = ["bye", "see you", "smell you later"]
information = ["more", "information"]
name = ["name"]
location = ["location"]
mexican = ["loco", "espanol", "Gracias"]
directions = ["elevator"]
counter = 29

r = sr.Recognizer()
m = sr.Microphone()

rospy.init_node('say_something')
try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        counter = 29
        print("Say something!")
        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))

                for item in name:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "My name is Yuuni."
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in assistant:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "Hello. How  can i help? You can ask me about booking, direction, location, more informatiom about the hotel, or i can even tell you a joke"
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in directions:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "The elevator is just down the lobby to the right side of the reception"
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in farewell:
                    if item in value:
                        counter = counter - 1
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "See you later. Enjoy the rest of your day."
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in reception:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "Thank you for choosing Double Tree by Hilton. Please talk to one of our receptionists to get more details."
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in bar:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "Please head over to the Red Dot Bar located just beside the honors check-in counter for ordering drinks and food."
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in timing:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "The red dot bar is open for food and drinks from 9 a m in the morning until midnight. The reception is manned 24 hours a day for providing you any assistance required."
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in connection:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "The wifi name is Double Tree Public. Please ask a staff member for the password"
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in thanking:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "Thank you for talking to me. Hope you have a comfortable stay"
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in laugh:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "Why was the robot angry? Because someone keeps pushing its buttons"
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
                    else:
                        counter = counter - 1
                        print(counter)

                for item in information:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "The double tree by hilton is a 4 star hotel built in a unique location, which gives guests panoramic views of the M K Stadium. Fancy watching football? Just take a peek outside your hotel window I hope yu enjoy your stay"
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

                    else:
                        counter = counter - 1
                        print(counter)

                for item in location:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "We are in Bletchley Milton Keynes right now. About 10 minutes away from the Bletchley railway station"
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

                    else:
                        counter = counter - 1
                        print(counter)

                for item in mexican:
                    if item in value:
                        if len(sys.argv) > 1:
                            text = ""
                            for arg in sys.argv[1:]:
                                text += arg + " "
                        else:
                            text = "K Taal Hoy, No Habla Ingles"
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

                    else:
                        counter = counter - 1
                        print(counter)

                if counter == 0:
                    text = "Pardon, could you please repeat?"
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

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
