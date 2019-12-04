#!/usr/bin/env python

import roslib; roslib.load_manifest('my_pkg_name')
import rospy 
import actionlib

from chores.mag import *

class DodishesServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('do_dishes', DodishesAction, self.execute, False)
        self.server.start()

    def execute(self, goal):
        self.server.set_succeded()

if __name__ == '__main':
    rospy.init_node('do_dishes_server')
    server = DoDishesServer()
    rospy.spin()
