#!/usr/bin/env python
# Sample moveit_Code to test moving the arm to a goal pose.

# Imports
import rospy
import geometry_msgs.msg
import moveit_commander
from geometry_msgs.msg import *

# Init ROS Node
rospy.init_node("baxter_moveit")
rospy.sleep(0.5)

# Move Right Arm
group = moveit_commander.MoveGroupCommander("right_arm")
rospy.sleep(0.5)

# Createa  pose object and populate it.
p = geometry_msgs.msg.Pose()

# Position
p.position.x = 0.133
p.position.y = -0.598
p.position.z = 0.012

# Orientation w Quaternion
p.orientation.x = -0.008
p.orientation.y = 0.707
p.orientation.z = -0.062
p.orientation.w = 0.704

# Set target pose to right arm and move
group.set_pose_target(p)
group.go()
