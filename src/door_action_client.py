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
    action_client = actionlib.SimpleActionClient('door_action', OpenDoorAction)
    action_client.wait_for_server()
    goal = OpenDoorGoal()
    goal.open_door = 'null'
    
    action_client.send_goal(goal)
    action_client.wait_for_result()
    result = action_client.get_result()
    if result == True:
        rospy.loginfo('succece!!')
    else:
        rospy.loginfo('failed')

if __name__ == '__main__':
    try:
        rospy.init_node('door_action_client')
        door()
    except rospy.ROSInterruptException:
        pass
