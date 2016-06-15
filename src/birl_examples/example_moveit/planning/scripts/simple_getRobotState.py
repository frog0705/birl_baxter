#!/usr/bin/env python
import sys

import rospy 
import baxter_interface
import moveit_commander

# Initialize rospy and moveit_commander
rospy.init_node("baxter_tests")    
moveit_commander.roscpp_initialize([s for s in sys.argv if not s.startswith("__name:=")])

# Create baxter_interface and MoveGroupCommander objects
baxter_limb=baxter_interface.Limb("right")
moveit_limb=moveit_commander.MoveGroupCommander("right_arm")
rospy.sleep(2)

# Which is our End-Effector? right_gripper?
print "EEF link for MoveIt: "+moveit_limb.get_end_effector_link()

# Get pose from both baxter_interface and from moveit. 
baxter_pose=baxter_limb.endpoint_pose()["position"]
moveit_pose=moveit_limb.get_current_pose().pose.position

# Print data to screen
print "Baxter end_point:  %f , %f , %f"%(baxter_pose.x,baxter_pose.y,baxter_pose.z)
print "MoveIt end_point:  %f , %f , %f"%(moveit_pose.x,moveit_pose.y,moveit_pose.z)
    
# Terminate node
moveit_commander.roscpp_shutdown()
