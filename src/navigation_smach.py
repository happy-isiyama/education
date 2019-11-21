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
                outcomes=['outcome1','outcome2'],
                             output_keys=['sub_target_out'])
        self.sub_message = rospy.Subscriber('/input_target', String, self.messageCB)
        self.message = String()

    def messageCB(self, receive_msg):
        self.message = receive_msg.data

    def execute(self, userdata):
        self.message = 'NULL'
        while not rospy.is_shutdown() and self.message == 'NULL':
            print "wait for topic..."
            rospy.sleep(2.0)
        userdata.sub_target_out = self.message
        rospy.loginfo("search LocationName")
        f = open('/home/athome/catkin_ws/src/mimi_common_pkg/config/location_dict.yaml')
        location_dict = load(f)
        f.close()
        print userdata.seaech_target_out
        rospy.sleep(2.0)
        if userdata.sub_target_out in location_dict:
            print location_dict[userdata.sub_target_out]
            return 'outcome2'
        else:
            rospy.loginfo("NOT fount" + str(userdata.seaech_target_in) + "> in LocationDict")
            return 'outcome1'

class NavigationAC(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                outcomes=['outcome1','outcome3'],
                input_keys=['nav_target_in'])
        self.coord_list = []

    def execute(self, userdata):
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
                        return 'outcome1'
                    else:
                        rospy.loginfo('Buried in obstacle')
                        self.clear_costmaps()
                        rospy.loginfo('Clear Costmaps')
                        rospy.sleep(1.0)
                        count += 1
            rospy.sleep(2.0)
        except rospy.ROSInterruptException:
            pass


def main():
    sm = smach.StateMachine(outcomes=['outcome3'])#最終的に行き着く結果
    sm.userdata.sm_target = 'NULL'
    with sm:
        smach.StateMachine.add('SUB', Subscription(),
                transitions={'outcome1':'NAV',
                    'outcome2':'SUB'},
                remapping={'sub_target_out':'sm_target'})
        smach.StateMachine.add('NAV', NavigationAC(),
                transitions={'outcome1':'SUB',
                    'outcome3':'SUB'},
                remapping={'nav_target_in':'sm_target'})
    outcome = sm.execute()
    rospy.loginfo('Finish "Navigation"')


if __name__ == '__main__':
    rospy.init_node('navigation_smach')
    main()

