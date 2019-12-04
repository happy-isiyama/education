#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------
#Authonr: Ishiyama Yuki
#Dara: 2019/11/25
#Memo 
#----------------------------------------------------------

import rospy
import sys
import smach
import smach_ros

sys.path.insert(0, '/home/athome/catkin_ws/src/mimi_common_pkg/scripts')
from common_action_client import navigationAC
from common_function import *

class LocationSeach(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['outcome1'],
                            input_keys=['location_in'],
                            output_keys=['location_out','list_out'])

    def execute(self, userdata):
        userdata.list_out  = searchLocationName(userdata.location_in)
        if userdata.location_in != 'capboard':
            userdata.location_out = userdata.location_in
        return 'outcome1'


class Action(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                outcomes=['outcome2','outcome3'],
                input_keys=['target_in','list_in'],
                output_keys=['target_out'])
        self.jaj = 'failed'

    def execute(self, userdata):
        while not rospy.is_shutdown() and self.jaj == 'failed':
            self.jaj = navigationAC(userdata.list_in)
            rospy.sleep(1.0)
        if userda.target_in == 'capboard':
            userda.target_out = 'operater'
            return 'outcome2'
        else:
            return 'outcome3'


def main():
    rospy.loginfo('Start "Navigation"')
    sm = smach.StateMachine(outcomes=['outcome4'])
    sm.userdata.sm_target = 'capboard'
    with sm:
        smach.StateMachine.add('LOCATION_SEACH', LocationSeach(),
                transitions={
                    'outcome1':'ACTION'},
                remapping={
                    'location_in':'sm_target',
                    'location_out':'sm_target',
                    'list_out':'coord_list'})
        smach.StateMachine.add('ACTION', Action(),
                transitions={
                    'outcome2':'LOCATION_SEACH',
                    'outcome3':'outcome4'},
                remapping={
                    'target_in':'sm_target',
                    'target_out':'sm_target',
                    'list_in':'coord_list'})
    outcome = sm.execute()
    rospy.loginfo('Finish "Navigation"')

if __name__ == '__main__':
    rospy.init_node('Avoid_that')
    main()
