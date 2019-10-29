#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------
#Title:　ドアが開いてる時に進むROSノード
#Author: Isiyama Yuki
#Data: 2019/10/24
#Memo: 
#-------------------------------------------------------------

#ROS関係ライブラリ
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class SubscriberClass():
    def __init__(self):
        self.ranges_message = rospy.Subscriber('/scan', LaserScan, self.messageCB)
        self.laser = LaserScan()

    def messageCB(self, receive_msg):
        self.laser = receive_msg

    def message_value(self):
        if bool(self.laser.ranges) == "True":
            value = self.laser.ranges[359]
            return value


class PublishClass():
    def __init__(self):
        self.pub_message = rospy.Publisher('cmd_vel_mux/input/teleope', Twist, queue_size = 1)
        self.count = 1

    def linerContorol(self, value):
        twist_cmd = Twist()
        twist_cmd.linear.x = value
        rospy.sleep(0.1)
        self.pub_message.publish(twist_cmd)

def main():
    safety_distance = 1.0           #安全に進める距離の基準を入れた定数
    rospy.loginfo('start "open_door"')
    sc = SubscriberClass()
    pc = PublishClass()
    while not rospy.is_shutdown():
        state = sc.message_value()
        if state >= safety_distance:
            rospy.loginfo("start forward")
            for i in range(10):
                pc.linerContorol(0.1)
                break
        else:
            pass


if __name__ == '__main__':
    rospy.init_node('opne_door')
    main()
