#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------
#Title: mimiを目的地にナビゲーションするノード
#Author: Ishiyama Yuki
#Data: 2019/11/5
#Memo
#---------------------------------------------------

#ROS 関係ライブラリ
import rospy
import sys
from std_msgs.msg import String
from yaml import load
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from std_srvs.srv import Empty


class Navigation():
    def __init__(self):
        self.coord_list = []
        self.sub_message = rospy.Subscriber('/input_target', String, self.messageCB)
        self.target_name = String()
        self.flg = False
        self.coord_list = [] 

    def messageCB(self,receive_msg):
        self.target_name = receive_msg.data
        self.flg = True

    def input_value(self):
        while not rospy.is_shutdown() and self.flg == False:
            print "wait for topic..."
            rospy.sleep(2.0)
        self.flg == False
        return 1

    def searchLocationName(self):
        rospy.loginfo("search LocationName")
        f = open('/home/athome/catkin_ws/src/mimi_common_pkg/config/location_dict.yaml')
        location_dict = load(f)
        f.close()
        print self.target_name
        rospy.sleep(2.0)
        if self.target_name in location_dict:
            print location_dict[self.target_name]
            rospy.loginfo("Return location_dict")
            self.coord_list = location_dict[self.target_name]
            return 2 #一致する目的地がある場合、次のアクションクライアントへの送信へ
        else:
            rospy.loginfo("NOT found<" + str(self.target_name) + "> in LocationDict")
            return 0 #目的地がLocation_dictにない場合、無い事を伝え最初に戻る

    def navigationAC(self):
        try:
            rospy.loginfo("Start Navigation")
            ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
            ac.wait_for_server()
            clear_costmaps = rospy.ServiceProxy('move_base/clear_costmaps', Empty)
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = 'map'
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = self.coord_list[0]
            goal.target_pose.pose.position.y = self.coord_list[1]
            goal.target_pose.pose.orientation.z = self.coord_list[2]
            goal.target_pose.pose.orientation.w = self.coord_list[3]
            rospy.wait_for_service('move_base/clear_costmaps')
            clear_costmaps()
            rospy.sleep(1.0)
            ac.send_goal(goal)
            state = ac.get_state()
            count = 0
            if state == 1:
                rospy.loginfo('Got out of the obstacle')
                rospy.sleep(1.0)
            elif state == 3:
                rospy.loginfo('Navigation success!!')
                return 3
                state = 0
            elif state == 4:
                if count == 10:
                    count = 0
                    rospy.loginfo('Navigation Failed')
                    rospy.sleep(1.0)
                    count += 1
        except rospy.ROSInterruptException:
            pass        


def main():
    nv = Navigation()
    state = 0
    rospy.loginfo('start "navigation"')
    while not rospy.is_shutdown() and not state == 3:
        if state == 0:
            state = nv.input_value()#メッセージを受信するまで待機 
        if state == 1:
            state = nv.searchLocationName() #パラメータと入力値を比較
        if state == 2:
            state = nv.navigationAC()#アクションクライアントの実行
    rospy.loginfo('Finish "Navigation"')


if __name__ == '__main__':
    rospy.init_node('navigation_tut')
    main()

