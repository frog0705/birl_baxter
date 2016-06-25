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
# In this program we implement a numerical approach to inverse kinematics by using the Jacobian manipulator.
# In addition, we also make use of redundancy and the null space to achieve secondary goals in our solution.
# So, a reference cartesian location is given to the program. The error is computed and converted into a 
# joint angle perturbation that is added to the current joint angles. The error direction moves the joint angles
# towards the goal position. Further, we create a secondary goal, there are many possibilities:
# 	i) Move a single joint angle in a particular direction to avoid reaching a limit, or 
# 	ii) Move all joints towards the center of their joint motion range. This can be done by computing those center 
# 	positions and subtracting the current joint angles. This gives an error measure in joint angles.
# 
# About the Jabocian:
# The use of the Jaobian is not always evident. It works best with certain size perturbations. If the perturbations are
# too large the motions are uncontrolled. If the motions are too small, one may never reach the desired goal.
#
# About the null space and projections:
# After calculating the null space N, we will obtain a non-square matrix. This is in-effect a set of column vectors of joint
# angles whose linear combination will always result (when multiplied by the Jacobian) in a zero vector. 
# This non-square matrix can be turned into a projection matrix by multiplying the the null space times its inverse 
# (since this is not a square matrix, we multiply times the pseudo-inverse). The projection matrix can then be used to
# project any other joint-angle column vector into the null-space. This joint-angle vector actually represents dq, a
# joint angle velocity or perturbation. It is best represented by an error measure. If you have a desired joint angle state
# then subtract the current joint angle state to compute an error. This error should then be scaled to a size that works 
# well with the jacobian (otherwise it will result in an unstable motion). It is important to explicitly check to make sure
# the update is small. If it is not, it should not be used to move the joints.
#
# TODO:
# We have not yet checked for singularity conditions in the Jacobian. This can be done by studying the size of the determinant.
# If we are reaching a singularity condition, a recovery behavior should be effected. The motion path of the robot should be modified.
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

    # If you want to debug, uncomment the next line.
    #pdb.set_trace()

    # Initialize node
    rospy.init_node('example3_kdl')

    # Call routine to enable the robot
    rs=enable_Baxter()
    
    ## Params
    loop=rospy.Rate(rate)
    dp=zeros((3,1))

    # Create Limb Objects
    rLimb=baxter_interface.Limb('right')
    #lLimb=baxter_interface.Limb('left')

    # Create Kinematic Objects
    rKin = baxter_kinematics('right')
    #lKin = baxter_kinematics('left')

    # Get Joint names 
    #jNamesR_ordrered=rLimb.joint_names()
    jNamesR=['right_s0','right_s1','right_w0','right_w1','right_w2','right_e0','right_e1']

    # Set Vector to some goal to exploit redundancy.
    # A. Vector pointing to mid-range of joint angles
    if dq_to_ctr_mode:
         upper_limits=[0.890, 1.047, 3.028, 2.618, 3.059, 2.094, 3.059] 		# s0s1e0e1w0w1w2
         lower_limits=[-2.461, -2.147, -3.028, -0.052, -3.059, -1.571, -3.059]
         mid_range=[(upper_limits[i]-lower_limits[i])/2 for i in range(7)]
         q_red=matrix([upper_limits[i]-mid_range[i] for i in range(7)]).T		# This is in effect a q_dot, a velocity of joint angles. 
    else: 
         # B. Vector with a simple 
         q_red=matrix('0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0').T				# Select the joint you want to update in this 7x1 col vector
         for i in range(len(q_red)):							# Identify the joint that is non-zero and save that index.
              if q_red[i,0]!=0.0:
                   idx=i 								# Matrix indeces start from zero

    # Set a reference pose: [x,y,z,vx,vy,vz,w]. This one is near the home position of arm.
    # Home joint angle position for baxter_world_home.launch is approximately: [0.58,-0.19,0.23,-0.11,0.99,0.01,0.02]
    ref_pose={'position':[0.70,-0.2, 0.23],'orientation':[-0.12,0.99,0.01,0.01]}
    ref_pos=matrix(ref_pose['position']).T
    #ref_rot=matrix(ref_pose['orientation'])
    print 'The reference pos is: ' 
    print(ref_pos)

    # Right Arm
    while not rospy.is_shutdown():
        print 'example3_kdl for the right arm...'    

        # 1. Get the current angles and jacobian as numpy matrices
        rAngles=rLimb.joint_angles() # returns as s0s1w0w1w2e0e1
        rAnglesM=matrix(rAngles.values()).T
        jac=rKin.jacobian()

        # 2. Compute the forward Kinematics using the Jacobian: del_p=J(q)del_q
        curr_pos=rLimb.endpoint_pose()
        curr_pos=matrix(curr_pos['position']).T
        print 'The current position is:\t\t The reference positions is:' 
        for i in range(len(curr_pos)):
             print repr(curr_pos[i,0]).rjust(10),repr(ref_pos[i,0]).rjust(40)

        # Position Mode
        if pos_mode:
            # 3. Compute the error between reference and current positions
            del_p_error=Kp*(ref_pos-curr_pos[0:3])

            # 4. Get a scalar distance (vector norm) to more easily interpret the error
            dp_norm=norm(del_p_error)
            print 'the dpnorm is %f' %dp_norm
            
            # 5. Extract the translation Jacobian
            jTrans=jac[0:3,0:7] # when slicing go one dim past end 
    
            # 6. Compute the dq using dp_error
            del_q=(pinv(jTrans))*del_p_error    # in terms of dp change
    
            # 7. Add this dq to current joint Angles
            ref_anglesM=del_q+rAnglesM
    
            ref_angles=ref_anglesM.ravel().tolist()[0]  # change back to list.[0] b/c it returns nested list.
            ref_angles=dict(zip(jNamesR,ref_angles))
            
            # 8. Move the Limb wout working with the null space
            #rLimb.move_to_joint_positions(ref_angles) # need to check that indeces are in the right order
            rLimb.set_joint_positions(ref_angles)
            
        # Velocity Mode 
        else:            
            # 3. Compute the error between reference and current positions
            del_p_error=Kv*(ref_pos-curr_pos[0:3])
            for i in range(len(del_p_error)):
                 dp[i]=del_p_error[i]/dt
                 
            # 4. Get a scalar distance (vector norm) to more easily interpret the error
            dp_norm=norm(del_p_error)
            print 'the dpnorm is %f' %dp_norm
            
            # 5. Extract the translation Jacobian
            jTrans=jac[0:3,0:7] # when slicing go one dim past end 
    
            # 6. Compute the dq using dp_error
            #del_q=(pinv(jTrans))*del_p_error    # in terms of dp change
            dq=(pinv(jTrans))*dp                # in terms of velocity 
    
            # 7. Add this dq to current joint Angles
            ref_anglesM=(dt*dq)+rAnglesM # Covert from speed to distance
    
            ref_angles=ref_anglesM.ravel().tolist()[0]  # change back to list.[0] b/c it returns nested list.
            ref_angles=dict(zip(jNamesR,ref_angles))
            
            # 8. Move the Limb wout working with the null space
            #rLimb.move_to_joint_positions(ref_angles) # need to check that indeces are in the right order
            rLimb.set_joint_positions(ref_angles)
        
        
        if null_space_comp:
            # 9. Compute the kernel (null space) for the translational Jacobian of Baxter (3x6) and the pseudo-inverse
            jNull=matrix(null(jTrans))
            jNull_inv=matrix(pinv(jNull))
            
            # Test to make sure that the output of the translational Jacobian(3,7) times the kernel(7,4) is the zero matrix(3,4):
            z=jTrans*jNull
            print '\nTest to make sure that the output of the translational Jacobian(3,7) times the kernel(7,4), is the zero matrix(3,4):\njTrans*jNull is: '
            print z
    
            # 10. Compute direction of motion.
            # If dqt_to_ctr, then compute error from center of joint range: desired - actual
            # Scale the error so that it is appropriate for the Jacobian Null Space.
            if dq_to_ctr_mode:
                 dq_ref=Kq*(q_red - ref_anglesM)
                 print '\nCenter Angles\t\t Current Angles\t\t\t Error'
                 for i in range(len(q_red)):
                      print repr(q_red[i,0]).rjust(7),repr(ref_anglesM[i,0]).rjust(33),repr(dq_ref[i,0]).rjust(29)
            else:
                 dq_ref=q_red            
                 print '\nThe error vector in radians is:'
                 print(dq_ref)
            
            # Compute the norm
            dq_ref_norm=norm(dq_ref)
            print 'And, the norm of our error reference is: '
            print(dq_ref_norm)        
            
            # 11. Project this error to the nullspace via NN*dq_to_ctr
            null_proj=jNull*jNull_inv
            
            dq_null=null_proj*dq_ref
            print '\nThen, this error vector, projected unto the nullspace dq_null is:'
            print dq_null
            print ''

            # 12. Scale dq_null.
            # If you are only changing a single joint, the projection will modify that dimensions of that joint. 
            # We can do a scaling mechanism to reset that specific joint value to our original goal.
            if single_joint_update_mode:
                 for i in range(len(dq_null)):
                      dq_null[i,0]=(dq_null[i,0]/dq_null[idx,0])*q_red[idx,0] # for loop index starts at 1 but the matrix index at 0

            # 13. If norm is less than 0.00001 then add
            print 'If we multipy dq_null x Jacobian and compute the norm, it should be zero...'
            zero=norm(jTrans*dq_null)
            print(zero)
                       
            # 14. Only move the joints if the computed dq_null in fact gives a small (near zero) output. Otherwise
            # do not move the joint angles. This results in a much more stable motion. 
            if zero < 0.00001:
                ref_null_anglesM=ref_anglesM+dq_null
            
                # 12. Convert back to list and move
                ref_null_angles=ref_null_anglesM.ravel().tolist()[0]  # change back to list.[0] b/c it returns nested list.
                ref_null_angles=dict(zip(jNamesR,ref_null_angles)) 
                #rLimb.set_joint_positions(ref_null_angles)
                rLimb.move_to_joint_positions(ref_null_angles)
        
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
