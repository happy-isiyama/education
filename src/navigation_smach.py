#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
#Author: Ishiyama Yuki
#Data: 2019/11/16
#Memo
#-----------------------------------------------------

import rospy
import sys
from std_msgs.msg import String
from yaml import load
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from std_srvs.srv import Empty
import smach
import smach_ros

class Subscription(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['outcome1'],
                             output_keys=['sub_target_out'])
        self.sub_message = rospy.Subscriber('/input_target', String, self.messageCB)
        
    def messageCB(self, receive_msg, userdata):
        userdata.sub_target = receive_msg.data

    def excute(self, userdata):
        userdata.sub_target = 'NULL'
        while not rospy.is_shutdown() and userdata.sub_target == 'NULL':
            print "wait for topic..."
            rospy.sleep(2.0)
        return 'outcome1'

class SearchLocationName(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                outcomes=['outcome0','outcome2']
                input_keys=['seaech_target_in']
                output_keys=['seach_taeget_out'])

    def excute(self, userdata):
        rospy.loginfo("search LocationName")
        f = open('/home/athome/catkin_ws/src/mimi_common_pkg/config/location_dict.yaml')
        location_dict = load(f)
        f.close()
        print userdata.seaech_target_in
        rospy.sleep(2.0)
        if userdata.seaech_target_in in location_dict:
            print location_dict[userdata.seaech_target_in]
            userdata.seaech_target_out = userdata.seaech_target_in
            return 'outcome2'
        else:
            rospy.loginfo("NOT fount" + str(userdata.seaech_target_in) + "> in LocationDict")
            return 'outcome0'

class NavigationAC(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                outcomes=['outcome0,outcome3']
                input_keys=['nav_target_in'])
        self.coord_list = []

    def excute(self, userdata):
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
            rospy.wait_for_server('move_base/clear_costmaps')
            clear_costmaps()
            rospy.sleep(1.0)
            ac.send_goal(goal)
            count = 0
            while not rospy.is_shutdown():
                state = ac.get_state()
                if state == 1:
                    rospy.loginfo('Got out of the obstacle')
                    rospy.sleep(1.0)
                elif state == 3:
                    rospy.loginfo('Navigation success!!')
                    return 'outcome3'
                elif state == 4:
                    if count == 10:
                        count = 0
                        rospy.loginfo('Navigation Failed')
                        self.clear_costmaps()
                        rospy.loginfo('Clear Costmaps')
                        rospy.sleep(1.0)
                        count += 1
            rospy.sleep(2.0)
        except rospy.ROSInterruptException:
            pass






def main():
    rospy.init_node('navigation_smach')
    sm = smach.StateMachine(outcomes=['outcome', ''])#最終的に行き着く結果
    with sm:
        smach.StateMachine.add('SUB', Subscription(),
                transition={'outcome1':'SEARCH'})
                remapping={'sub_target':'target_name'}
        smach.StateMachine.add('SEARCH', SearchLocationName(),
                transition={'outcome0':'SUB','outcome2':'NAV'}
                remapping={'seaech_target_in':'target_name'}
        smach.StateMachine.add('NAV', NavigationAC(),
                transition={'outcome0':'SUB','outcome3':'SUB'}
    outcome = sm.excute()
    rospy.loginfo(('Finish "Navigation"')

if __name__ == '__main__':
    main()

