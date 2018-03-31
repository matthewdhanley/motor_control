#!/usr/bin/env python
import serial #make sure you install pyserial
import rospy
import time
import struct
import sys
from serial.tools import list_ports
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import Joy

motorScalar=30 #change this to adjust what magnitude the serial commands are

def callback(data):
    try:
        y = data.poses[0].position.z*39.37
        x = data.poses[0].position.x*39.37
        print("(" + str(x) + "," + str(y) + ")")
    except:
        pass


def start():
    rospy.Subscriber('/tag_detections_pose', PoseArray, callback)
    rospy.init_node('pose_subscriber')
    print "Node started"
    rospy.spin()


if __name__ == "__main__":
    start()
