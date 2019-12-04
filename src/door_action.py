#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
#Title: ドアが開いてる時に進むactionlib
#Author: Isiyama Yuki
#Data: 2019/11/29
#Memo:catkin_makeがうまく行っていない
#------------------------------------------------------

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import actionlib
from education.msg import OpenDoorAction
from education.msg import OpenDoorResult
from education.msg import OpenDoorFeedback

class OpneDoor():
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel_mux/input/teleope', Twist, queue_size = 10)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.messageCB)
        self.laser = LaserScan()
        self.front_value = 0.0
        self.action_server = actionlib.SimpleActionserver(
                'door_action', OpenDoorAction, execute_cd = self.door_open, auto_start=False)
        self.safe_way = False
        self.action_server.start()

    def laserscanCB(self, recive_msg):
        self.laser = receive_msg
        self.safe_way = True

    def linerContorol(self, value):
        twist_cmd = Twist()
        twist_cmd.liner.x = value
        rospy.sleep(0.1)
        self.pub.Publish(twist_cmd)

    def door_open(self):
        rospy.loginfo('start"door_action"')
        while not rospy.is_shutdown() and self.safe_way == True:
            rospy.loginfo('wait for laserscan ...')
        if self.safe_way == True:
            feedback = OpenDoorFeedback('get value')
            self.pub.publish(feedback)
        self.safe_way = False
        sel.front_value = self.ranges[359]
        if self.front_value < 2.0:
            result = OpenDoorResult('start foward')
            for i in range(10):
                self.linerContorol(0.1)
        else:
            result = OpenDoorResult('false foward')
        self.action_server.set_succeeded(result)

            
if __name__ == '__main__':
    rospy.init__node('door_action')
    door_action = OpenDoor()
    rospy.spin()
