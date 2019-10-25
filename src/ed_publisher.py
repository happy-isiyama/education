#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------------
#Title
#Author: yuki isiyama
#data 2019/10/2
#Memo: 数字を1~10まで配布する
#---------------------------------------------------------------------------------------------

#ROS関数ライブラリ
import rospy
from std_msgs.msg import String


class PublishClass():
    def __init__(self):
        #Publisher
        self.pub_message = rospy.Publisher('/test_topic', String, queue_size = 1)
        self.count = 1

    def publishMessage(self):
        while not rospy.is_shutdown() and self.count <= 10:
            data = str(self.count)
            rospy.loginfo('Publish message: ' + data)
            rospy.sleep(1.0)
            self.pub_message.publish(data)
            self.count +=1
        return 1


def main():
    rospy.loginfo('start "ed_publisher"')
    pc = PublishClass()
    state = 0
    while not rospy.is_shutdown():
        state = pc.publishMessage()
        if state == 1:
            rospy.loginfo('Finish "ed_publisher"')
            break
        else:
            pass

if __name__== '__main__':
    rospy.init_node('ex_publisher')
    main()
