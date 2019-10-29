#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------
#Title: ドアが開いてる時に進むROSノード
#Author: Ishiyama Yuki
#Data: 2019/10/29
#Memo:
#----------------------------------------------------------

#ROS関係ライブラリ
import rospy
from sensor_msgs.msg import Leaserscan
from geometry_msg.msg import Twist

class DoorOpne():
    def __init__(self):
        self.ranges_message = rospy.Subscriber('/scan', LaserScan, messageCB)
        self.pub_message = rospy.Pubulisher('/cmd_vel_mux/input/teleop', Twist, queue_size =1)
        self.laser = LaserScan()
        self.flg = False

     def linerContorol(self, value):
         twist_cmd = Twist()
         twis_cmd.linear.x = value
         rospy.sleep(0.1)
         self.pub_message.publish(twist_cmd)
       
    def messageCB(self, receive_msg):
        self.laser = receive_msg.ranges 
        self.forward = self.laser[359]
        self.flg = True 

    def wait_message(self):#正面に値を受け取るまで待つ関数
        while not ropy.is_shutdown() and not self.flg == True:
            print "wating for topic..."
            rospy.sleep(2.0)
        self.flg == False
        return 1

    def progress_condition(self):
        safty_distance = 2.0 #安全距離の基準
        if self.forward => safty.distance:
            return 2
        elif:
            return 0

    def advance_mimi:
        for i in range(10):
            self.linerContorol(0.2)
        return 3

def main():
    dp = DoorOpeen()
    state = 0
    rospy.loginfo('start "state_transition"')
    while not rospy.is_shutdown and not state == 3:#最後の状態遷移のステイタス番号を書く。
        if state == 0:
            state = dp.wait_message #メッセージが入るまで待機する関数
        if state == 1:              
            state = dp.progress_condition#正面に障害物がないか判断する関数
        if state == 2:
            state = dp.advance_mimi#mimiを前進させるプログラム
    rospy.loginfo('Finis "state_transition"')


if __name__ == '__main__':
    rospy.init_node('state_transition')
    main()
