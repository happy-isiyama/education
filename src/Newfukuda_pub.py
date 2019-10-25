#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------------
#Title
#Author: yuki isiyama
#data 2019/10/4
#Memo: ２の１０乗まで１つづつ配布する
#---------------------------------------------------------------------------------------------

#ROS関数ライブラリ
import rospy
from std_msgs.msg import String


def publishMessage():
    pub_message = rospy.Publisher('/test_topic', String, queue_size = 10)
    num_int = 2
    num_str = 0
    count = 1
    while not rospy.is_shutdown() and count <= 10:
        num_str = str(num_int)
        rospy.loginfo(num_str)
        rospy.sleep(1.0)
        pub_message.publish(num_str)
        num_int = num_int * 2
        count += 1


def main():
    rospy.loginfo('Start "世界のfukuda"')
    publishMessage()
    rospy.loginfo('Finish "世界のfukuda"')


if __name__ == '__main__':
    rospy.init_node('Newfukuda_pub.py')
    main()
