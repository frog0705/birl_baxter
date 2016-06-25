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
# Requires the installation of baxter_PyKDL found at: http://sdk.rethinkrobotics.com/wiki/Baxter_PyKDL
# Example class on how to compute Jacobians.

#-----------------------------------------
# Imports
#-----------------------------------------
# To enable debug, uncomment the next line.
import pdb
import os                                          # used to clear the screen
import math
import rospy
import baxter_interface
from baxter_interface import CHECK_VERSION
from baxter_pykdl import baxter_kinematics
from rbx1_nav.transform_utils import quat_to_angle # Convert quaternions to euler

#-----------------------------------------
# Local Methods
#-----------------------------------------
def enable_Baxter():
    # Enable the robot's arms
    print("Getting robot state...")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state=rs.state().enabled
        
    print("Enabling robot...")
    rs.enable() 

    return rs

def shutdown():
    rospy.loginfo("Node has been terminated. Closing gracefully.")
    rospy.sleep(10)

def main():

    # If you want to debug, uncomment the next line.
    # pdb.set_trace()

    # Initialize node
    rospy.init_node('example_kdl')

    # Call routine to enable the robot
    rs=enable_Baxter()
    
    # Set a ROS Rate for the while loop at 1Hz
    loop=rospy.Rate(5) 

    # Create Limb Objects
    rLimb=baxter_interface.Limb('right')
    lLimb=baxter_interface.Limb('left')

    # Create Kinematic Objects
    rKin = baxter_kinematics('right')
    lKin = baxter_kinematics('left')

    # Angles and Kinematics
    print 'Computing the Jacobian...'
    
    # Right Arm
    while not rospy.is_shutdown():
        print 'Right Arm'.center(35,'*')    

        print 'Pose from FKins...'
        pose=rKin.forward_position_kinematics() # Fkine
        print (
            '[',round(pose[0],2),round(pose[1],2),round(pose[2],2),
            '],[', round(pose[3],2),round(pose[4],2),round(pose[5],2),round(pose[6],2),']'
            )
        print ''

        print 'Joint Angles from IKins...'
        # Get End pose, without orientation
        print 'Cartesian End-Effector Pose'

        rPose = rLimb.endpoint_pose()
        rIKin=rKin.inverse_kinematics(rPose['position'],rPose['orientation']) 
        print round(rIKin[0],4),round(rIKin[1],4),round(rIKin[2],4),round(rIKin[3],4),round(rIKin[4],4),round(rIKin[5],4),round(rIKin[6],4)
        print ''

        # Jacobian
        print 'Jacobian:\n'
        print rKin.jacobian()

        # Jacobian Transpose
        print 'Jacobian Transpose:\n'
        print rKin.jacobian_transpose()

        # Jacobian Pseudo-Inverse (Moore-Penrose)
        print '\n*** Baxter Jacobian Pseudo-Inverse (Moore-Penrose Inverse)\n'
        print rKin.jacobian_pseudo_inverse()
   

        # Set the loop speed
        loop.sleep()

        # Clear the screen for easier reading
        os.system('clear')

    # Set rospy to execute a shutdown function when exiting
    rospy.on_shutdown(shutdown)
    return rs                                                 


 
if __name__ == "__main__":
    try:
        main()
    except:
        rospy.loginfo("example_baxter_kins_right node terminated.")        
