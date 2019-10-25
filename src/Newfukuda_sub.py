#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
#Title: トピックを購読するためのサンプルROSノード
#Author: yuki isiyama
#Data; 2019/10/5
#Memo: トピック"/test_topic"を購読して、数字が5の時ノード終了
#-------------------------------------------------------------------------


import rospy
from std_msgs.msg import String
 
 
class SubscriberClass():
    def __init__(self):
         #Subscriber
         #第一引数:トピック名 第二引数:メッセージ形名 第三引数:コールバック場所名（受け取る場所の>    こと）
         self.sub_message = rospy.Subscriber('/test_topic', String, self.messageCB)
 
    def messageCB(self, receive_msg):#<-------ここでトピックメッセージを受け取る
        self.data = receive_msg.data
        self.data = str()
        print self.data
 
    def printMessage(self):
        self.data = 'none'
        while not rospy.is_shutdown():
            if self.data == '1024':
                rospy.loginfo('Subscribe 1024')
                return 1
            else:
                pass
 

def main():
    rospy.loginfo('Start "世界のfukuda"')
    sc = SubscriberClass()
    state = 0
    while not rospy.is_shutdown():
        state = sc.printMessage()
        if state == 1:
            rospy.loginfo('Finish "世界のfukuda"')
            break
        else:
            pass
 
if __name__ == '__main__':
    rospy.init_node('Newfukuda_sub.py')
    main()

