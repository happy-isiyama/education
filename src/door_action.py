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
from actionlib import SimpleActionServer
from education.msg import OpenDoorAction
from education.msg import OpenDoorResult
from education.msg import OpenDoorFeedback

class OpenDoor():
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel_mux/input/teleope', Twist, queue_size = 10)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.laserscanCB)
        self.laser = LaserScan()
        self.front_value = []
        self._action_server = actionlib.SimpleActionServer('door_action',
                OpenDoorAction, 
                execute_cb = self.execute_cb,
                auto_start=False)
        self.safe_way = False
        self._action_server.start()

    def laserscanCB(self, recive_msg):
        self.laser = receive_msg
        self.front_value = self.laser.ranges[359]
        self.safe_way = True

    def linerContorol(self, value):
        twist_cmd = Twist()
        twist_cmd.liner.x = value
        rospy.sleep(0.1)
        self.pub.Publish(twist_cmd)

    def execute_cb(self, goal):
        rospy.loginfo('start"door_action"')
        while not rospy.is_shutdown() and self.safe_way == True:
            rospy.loginfo('wait for laserscan ...')
        if self.safe_way == True:
            feedback = OpenDoorFeedback('get value')
            self.pub.publish(feedback)
        self.safe_way = False
        if self.front_value < 2.0:
            result = OpenDoorResult(True)
            for i in range(10):
                self.linerContorol(0.1)
        else:
            result = OpenDoorResult(False)
        self.action_server.set_succeeded(result)

            
if __name__ == '__main__':
    rospy.init_node('door_action')
    OpenDoor()
    rospy.spin()
