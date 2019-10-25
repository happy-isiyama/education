#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
#Title:トピックを購読するためのサンプルROSノード
#Author: Yuki isiyama
#Data: 2019/10/03
#Memo: トピック"/sample_topic"を購読して、数字が5の時ノード終了
#----------------------------------------------------------------------

#ROS関連ライブラリ
import rospy
from std_msgs.msg import String


class SubscriberClass():
    def __init__(self):
        #subscriber
        self.sub_message = rospy.Subscriber('/test_topic', String, self.messageCB)
        self.data = String()

    def messageCB(self, receive_msg):
        self.data = receive_msg.data

    def printMessage(self):
        self.data = 'none'
        while not rospy.is_shutdown():
            if self.data == '5':
                rospy.loginfo('Subscribe 5')
                return 1
            else:
                pass


def main():
    rospy.loginfo('start "ed_subscriber"')
    sc = SubscriberClass()
    state = 0
    while not rospy.is_shutdown():
        state = sc.printMessage()
        if state == 1:
            rospy.loginfo('Finish "ed_subscriber"')
            break
        else:
            pass

if __name__ == '__main__':
    rospy.init_node('ed_subscriber')
    main()

