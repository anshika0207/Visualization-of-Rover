#!/usr/bin/python3

import rospy, tf, math

import roslib; roslib.load_manifest('teleop_twist_keyboard')
from geometry_msgs.msg import Twist
import sys, select, termios, tty

from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from std_msgs.msg import Float64

[j1,j2,j3,j4,j5]=[0,0,0,0,0]


def getKey(key_timeout):
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key
    
    
def pyfun(j,h,l):
	print("inside pyfun")
	y=getKey(10)
	if y=='+':
		if j<=h:
			j+=0.1
		else:
			j=h
	if y=='-':
		if j>=l:
			j-=0.1
		else:
			j=l
			
	return j

def afterPress():
	global j1,j2,j3,j4,j5
	t=getKey(10)
	if t=='a':
		j1=pyfun(j1,0.15,-0.20)
	if t=='b':
		j2=pyfun(j2,0.07,-0.17)
	if t=='c':
		j3=pyfun(j3,3.14,-3.14)
	if t=='d':
		j4=pyfun(j4,0.0,-3.14)
	if t=='e':
		j5=pyfun(j5,3.14,-3.14)
		
	print("function complete")
	return j1,j2,j3,j4,j5
	
if __name__ == '__main__':
	settings = termios.tcgetattr(sys.stdin)
	rospy.init_node('joint_state_publisher')
	pub=rospy.Publisher('joint_states', JointState, queue_size=10)
	joint=JointState()

	
	while(1):
		print("take the input")
		joint.header.stamp = rospy.Time.now()
		joint.name=['prism1','prism2','rot1','rot2','cont']
		joint.header.frame_id = 'base_link'
		[j1,j2,j3,j4,j5]= afterPress()
		joint.position=[j1,j2,j3,j4,j5]
		pub.publish(joint)

