#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------
#Title: ドアが開いてる時に進むactionlibのクライアント
#Author:Ishiyama Yuki
#Data: 2019/11/29
#Memo:
#----------------------------------------------------

import rospy
import actionlib
from education.msg  import OpenDoorAction
from education.msg import OpenDoorGoal

def door():
    ac = actionlib.SimpleActionClient('door_action', OpenDoorAction)
    ac.wait_for_server()
    goal = OpenDoorGoal()
    goal.open_door ='null'  
    
    ac.send_goal(goal)
    ac.wait_for_result()
    result = ac.get_result()
    if result.data == True:
        rospy.loginfo('succece!!')
        return True
    else:
        print result
        rospy.loginfo('failed')

if __name__ == '__main__':
    try:
        rospy.init_node('door_action_client')
        door()
    except rospy.ROSInterruptException:
        pass

