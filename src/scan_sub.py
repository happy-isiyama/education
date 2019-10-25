#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------
#Title: /scanのrangesの値を購読し表示するROSノード
#Author: Yuki isiyama
#Data 2019/10/09
#Memo: トピック”/scanを購読して、rangesの値のみを表示する
#------------------------------------------------------------------

#ROS関連ライブラリ
import rospy
from sensor_msgs.msg import LaserScan


class SubscriberClass():
    def __init__(self):
        #subscriber
        self.ranges_message = rospy.Subscriber('/scan', LaserScan, self.messageCB)
        self.laser  = LaserScan()

    def messageCB(self, receive_msg):
        self.laser = receive_msg
#        print(self.laser.ranges)

    def printMessage(self):
        print(self.laser.ranges)



def main():
    rospy.loginfo('start "scan_sub"')
    sc = SubscriberClass()
    state = 0
    while not rospy.is_shutdown():
        sc.printMessage()
#        if state == 1:
#            rospy.loginfo('Finish "scan_sub"')
#            break
#        else:
#            pass

if __name__ == '__main__':
    rospy.init_node('scan_sub')
    main()
