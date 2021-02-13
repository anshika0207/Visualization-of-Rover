#! /usr/bin/env python3

import math
from math import sin, cos, pi

import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from geometry_msgs.msg import Twist
import sys, select, termios, tty

x = 0.0
y = 0.0
th = 0.0

def getKey(key_timeout):
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key
    
    
if __name__ == '__main__':

	settings = termios.tcgetattr(sys.stdin)

	rospy.init_node('odometry_publisher')

	odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
	odom_broadcaster = tf.TransformBroadcaster()

	while(1):
		print("take the input")
		p=getKey(10)
		if p=='6':
			th+=0.5
		if p=='4':
			th-=0.5
		if p=='8':
			x-=0.1*cos(th)
			y-=0.1*sin(th)
		if p=='2':
			x+=0.1*cos(th)
			y+=0.1*sin(th)

	
		odom_quat = tf.transformations.quaternion_from_euler(0,0,th)
	 	
		odom_broadcaster.sendTransform(
		(x, y, 0.),odom_quat,rospy.Time.now(),"base_link","odom")
		odom = Odometry()
		odom.header.stamp = rospy.Time.now()
		odom.header.frame_id = "odom"
		odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
		odom.child_frame_id = "base_link"

		odom_pub.publish(odom)

