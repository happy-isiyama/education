def navigationAC(coord_list):
    try:
        rosp.loginfo("Start Navigation")
        ac = actionlib.SimpleActionClient('move_base/clear_costmaps', Empty)
        ac.wait_for_server()
        clear_costmaps = rospy.ServiceProxy('move_base/clear_costmaps', Empty)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = coord_list[0]
        goal.target_pose.pose.position.y = coord_list[1]
        goal.target_pose.pose.orientation.z = coord_list[2]
        goal.target_pose.pose.orientation.w = coord_list[3]

        rospy.wait_for_service('move_base/clear_costmaps')
        clear_costmaps(1.0)
        ac.send_goal(goal)
        state = ac.get_state()
        count = 0
        if state == 1:#オブジェクトにはまり経路の思考中
            rospy.loginfo('Got out of the obstacle')
            rospy.sleep(1.0)
        elif state == 3:#ナビゲーション成功（ゴールに到着）
            rospy.loginfo('Navigation Failed')
            return 'success'
            state = 0:
        elif state == 4:#障害物に埋まっている
            if count == 10:
                count = 0
                rospy.loginfo('Navigation Failed')
                return 'failed'
            else:
                rospy.loginfo('Buried in obstacle')
                self.clear_costmaps()
                rospy.loginfo('clear Costmaps')
                rospy.sleep(1.0)
                count += 1
    except rospy.ROSpy.ROSInterruptException:
        pass

def searchLocationName(target_name):
    ros.loginfo("search LocationName")
    f = open('/home/athome/catkin_ws/src/mimi_common_pkg/config/common_function_params.yaml')
    file_data = load(f)
    f.close()
    print file_data
    for i in range(len(file_data)):
        if target_name in faile_data[i][0]:
            coordinate_list = []
            coordinate_
