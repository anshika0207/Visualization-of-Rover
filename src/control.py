#!/usr/bin/env python3
import sys, select, termios, tty
import rospy
from sensor_msgs.msg import JointState
from tf import TransformBroadcaster
from tf.transformations import quaternion_from_euler as q2e
from math import sin,cos,pi

joint_state = JointState()
odom_broadcaster = TransformBroadcaster()

angle =0
if __name__ == "__main__":
    rospy.init_node("controller")
    robot_control = rospy.Publisher('/joint_states',JointState,queue_size=10)
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['base_to_wheel1','base_to_wheel2','base_to_wheel3','base_to_wheel4']
        joint_state.position = [0,0,0,0,0]

        x,y,z = cos(angle),sin(angle),0
        odom_quat = q2e(0,0,angle)
        print('%d','%d',x,y)
        robot_control.publish(joint_state)
        odom_broadcaster.sendTransform((x,y,z),odom_quat,rospy.Time.now(),'base_link','odom')

       

        rate.sleep()



