#!/usr/bin/env python

import rospy
import smach
import smach_ros

class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                outcomes=['outcome1'],
                output_keys=['foo_counter_out'])

    def execute(self, userdata):
        userdata.foo_counter_out = 1
        return 'outcome1'

class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                outcomes=['outcome2'],
                input_keys=['bar_counter_in'])
   
    def execute(self, userdata):
        print userdata.bar_counter_in
        return 'outcome2'

def main():
    sm = smach.StateMachine(outcomes=['outcome3'])
    with sm:
        smach.StateMachine.add('FOO', Foo(),
                transitions={'outcome1':'BAR'},
                remapping={'foo_counter_out':'sm_counter'})
        smach.StateMachine.add('BAR', Bar(),
                transitions={'outcome2':'outcome3'},
                remapping={'bar_counter_in':'sm_counter'})
    outcome = sm.execute()
    #rospy.spin()

if __name__ == '__main__':
    rospy.init_node('smach.rensyu')
    main()

