#!/usr/bin/python

# Copyright (c) 2013-2014, Rethink Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Rethink Robotics nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------
# Overview:
#-----------------------------------------
# Learn to move arm with force control.
#
# TODO:
#
# Requirements:
# baxter_PyKDL is needed and found at: http://sdk.rethinkrobotics.com/wiki/Baxter_PyKDL
# Using the Jacobian to move the arm to desired pose. 

#-----------------------------------------
# Imports
#-----------------------------------------
import pdb                                          # To enable debug, uncomment the next line.
import os                                           # used to clear the screen

## ROS
import rospy
## Baxter Interface
import baxter_interface
from baxter_interface import CHECK_VERSION
from baxter_pykdl import baxter_kinematics
#from rbx1_nav.transform_utils import quat_to_angle # Convert quaternions to euler // found in BaxterPyKDL
## Linear Algebra
from numpy import *
from numpy.linalg import *
from scipy import linalg, matrix
#-----------------------------------------
# Global Variables
#-----------------------------------------
## IK Modes
null_space_comp = 1 	# Compute the null-space and update the joint angles
pos_mode        = 1 	# Compute the Jacobian using delta_p vs dp (vel)

## Within Null Space, Secondary Goal Mode
single_joint_update_mode = 0
dq_to_ctr_mode           = 1

## Gains
Kp = 1.00             	# Set gain for multiplying error with Jacobian. 1 seems to work the best
Kv = 1.00		# Set gain for use with velocities.
Kq = 0.01		# Set gain for use with angle errors.

## Rates
rate = 1.0          	# Set a ROS Rate for the while loop at 1Hz. make it a float. If =1 same as pos_mode
dt   = 1/rate   
#-----------------------------------------
# Local Methods
#-----------------------------------------
# On how to compute the null space from SVD: 
# http://en.wikipedia.org/wiki/Singular_value_decomposition
# http://www.ecse.rpi.edu/~qji/CV/svd_review.pdf  
    
def null(A, eps=1e-12):
     u, s, vh = linalg.svd(A)                       # Capute the nullspace in vh
     padding = max(0,shape(A)[1]-shape(s)[0])       # shape: numpy class. Compute padding to aid appearance
     null_mask = concatenate(((s <= eps), ones((padding,),dtype=bool)),axis=0)
     null_space = compress(null_mask, vh, axis=0)   # Return slice of null matrix. http://docs.scipy.org/doc/numpy/reference/generated/numpy.compress.html
     return transpose(null_space)

def enable_Baxter():
    # Enable the robot's arms
    print("Getting robot state...")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    rs.state().enabled
        
    print("Enabling robot...")
    rs.enable() 

    return rs

def shutdown():
    rospy.loginfo("Node has been terminated. Closing gracefully.")
    rospy.sleep(5)

def main():

    # # If you want to debug, uncomment the next line.
    # #pdb.set_trace()

    # # Initialize node
    # rospy.init_node('example3_kdl')

    # # Call routine to enable the robot
    # rs=enable_Baxter()
    
    # ## Params
    # loop=rospy.Rate(rate)
    # dp=zeros((3,1))

    # # Create Limb Objects
    # rLimb=baxter_interface.Limb('right')
    # #lLimb=baxter_interface.Limb('left')

    # # Create Kinematic Objects
    # rKin = baxter_kinematics('right')
    # #lKin = baxter_kinematics('left')

    # # Get Joint names 
    # #jNamesR_ordrered=rLimb.joint_names()
    # jNamesR=['right_s0','right_s1','right_w0','right_w1','right_w2','right_e0','right_e1']


    # # Set rospy to execute a shutdown function when exiting
    # rospy.on_shutdown(shutdown)
    # return rs  
    


 
if __name__ == "__main__":
    try:
        main()
    except:
        rospy.loginfo("example_baxter_kins_right node terminated.")        
