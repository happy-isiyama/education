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
        self._action_server = SimpleActionServer('door_action',
                OpenDoorAction, 
                execute_cb = self.execute,
                auto_start=False)
        self.flg= False
        self._action_server.start()
        self.result = OpenDoorResult()

    def laserscanCB(self, receive_msg):
        self.front_value = receive_msg.ranges[359]
        self.flg = True

    def linerContorol(self, value):
        twist_cmd = Twist()
        twist_cmd.linear.x = value
        rospy.sleep(0.1)
        self.pub.publish(twist_cmd)

    def execute(self, goal):
        try:
            rospy.loginfo('start"door_action"')
            while not rospy.is_shutdown() and self.flg == False:
                rospy.loginfo('wait for laserscan ...')
                rospy.sleep(2.0)
            self.flg = False
            if self.front_value > 2.0:
                self.result = True
        #    for i in range(10):
                self.linerContorol(0.1)
            else:
                self.result = False
            self._action_server.set_succeeded(self.result)
        except rospy.ROSInterruptException:
            rospy.loginfo('Interrupted')
            pass

            
if __name__ == '__main__':
    try:
        rospy.init_node('door_action')
        OpenDoor()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo('Interrupted')
        pass
