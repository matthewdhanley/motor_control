#!/usr/bin/env python
import serial #make sure you install pyserial
import rospy
import time
import struct
import sys
from serial.tools import list_ports
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

motorScalar=30 #change this to adjust what magnitude the serial commands are

def callback(data):

    twist = Twist()
    twist.linear.x = data.linear.x
    twist.angular.z = data.angular.z

    twist.linear.z=data.linear.z
    twist.linear.y=data.linear.y
    twist.angular.x=data.angular.x

    #initialize values to zero
    xDir = 0
    thetaDir = 0

    if twist.linear.x < 0:
        #backward
        print "Going Backwards"
        xDir = twist.linear.x

    elif twist.linear.x > 0:
        #forward
        print "Going Forwards"
        xDir = twist.linear.x

    if twist.angular.x > 0:
        #left
        print "Turning Left"
        thetaDir = twist.angular.x

    elif twist.angular.x < 0:
        #right
        thetaDir = twist.angular.x

        print "Turning Right"

#Motor List:
    # frontLeft = 0
    # frontRight = 1
    # backLeft = 2
    # backRight = 3
	# linearShovel = 4
	# angularShovel = 5

	#if we want to go forward, left-CCW, right-CW
	#turning left, left motors rotate slower/reverse
	#turning right, right motors rotate slower/reverse

	#lets do some math to get pretty driving.  We don't want
	#motors to suddenly reverse when we want to turn.  They
	#should probably just go a little slower.

    if xDir == 0:
        leftOutput = thetaDir*motorScalar
        rightOutput = leftOutput
    if thetaDir == 0:
        leftOutput = -xDir*motorScalar
        rightOutput = -leftOutput

    if thetaDir > 0 and abs(xDir) > 0:
        #left
        rightOutput = xDir*motorScalar
        leftOutput = -rightOutput*(1-abs(thetaDir))

    elif thetaDir < 0 and abs(xDir) > 0:
        #right
        leftOutput = -xDir*motorScalar
        rightOutput = -leftOutput*(1-abs(thetaDir))

    robotShit=Twist()
    robotShit.linear.x = leftOutput
    robotShit.linear.y = rightOutput
    robotShit.angular.y = data.angular.y
    print(robotShit.angular.y)
    robotPub.publish(robotShit)

def start():
    global robotPub
    robotPub=rospy.Publisher('/robot/speeds',Twist,queue_size=1)
    rospy.Subscriber('/cmd_vel',Twist,callback)
    rospy.init_node('motor_control')
    print "Motor Control Started"
    rospy.spin()


if __name__ == "__main__":
    start()
