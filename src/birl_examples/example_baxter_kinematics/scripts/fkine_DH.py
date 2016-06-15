# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:38:54 2015
@author: 
"""
import rospy
import math
import numpy as np
import baxter_interface

# Initialize node
rospy.init_node('fkine_r')

# Right Arm
limb   = baxter_interface.Limb('right')
angles = limb.joint_angles()
pose   = limb.endpoint_pose()

angles['right_s0']=0.0
angles['right_s1']=0.0
angles['right_e0']=0.0
angles['right_e1']=0.0
angles['right_w0']=0.0
angles['right_w1']=0.0
angles['right_w2']=0.0

limb.move_to_joint_positions(angles) # moving right arm to all 0 joint angles 

# General Definition of a transfrom from joint i_1 to joint 1, per Peter Corke's book
def _j_1_T_j(alpha,a,d,theta):
    T=[
        [math.cos(theta),  -math.sin(theta)*math.cos(alpha),  math.sin(theta)*math.sin(alpha),  a*math.cos(theta)],
        [math.sin(theta),  math.cos(theta)*math.cos(alpha),  -math.cos(theta)*math.sin(alpha),  a*math.sin(theta)],
        [0,                math.sin(alpha),                   math.cos(alpha),                  d                ],
        [0,                0,                                 0,                                1                ],
    ]
    return T

# Joint Angles: zero configuration
s0=0;s1=0;e0=0;e1=0;w0=0;w1=0;w2=0;eefa=0;

wPe=0 # w2 to end effector link length

#DH (alpha_i, a_i,   d_i,    theta_i)
DH=[
    [-1.571,  0.069, 0.2703, s1],
    [1.571,   0,     0,      e0],
    [-1.571,  0.069, 0.3644, e1],
    [1.571,   0,     0,      w0],
    [-1.571,  0.01,  0.3743, w1],
    [1.571,   0,     0,      w2],
    [0,       0,     wPe,    eefa],
]

# Create a List of 7 transformation. Assumes shoulder is the base and that we have an end-effector.
T=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Fill in the Transformation List from 0 to 6
for i in range (0,7):
    T[i]=_j_1_T_j(DH[i][0],DH[i][1],DH[i][2],DH[i][3])

# Assign unit transformations to a joint transformation
s0_T_s1=T[0]    # shoulder 0 to shoulder 1
s1_T_e0=T[1]    # shoulder 1 to elbow 0    
e0_T_e1=T[2]    # elbow 0 to elbow 1
e1_T_w0=T[3]    # elbow 1 to wrist 0
w0_T_w1=T[4]    # wrist 0 to wrist 1
w1_T_w2=T[5]    # wrist 1 to wrist 2
w2_T_eef=T[6]    # wrist 2 to end effector

# Transformation from shoulder 0 to wrist 2
s0_T_w2=np.mat(T[0])*np.mat(T[1])*np.mat(T[2])*np.mat(T[3])*np.mat(T[4])*np.mat(T[5])

# Add base to shoulder transform: body to right shoulder 0
b_T_rs0=[
    [math.cos(s0), -math.sin(s0), 0,  0.064027],
    [math.sin(s0),  math.cos(s0), 0, -0.25903],
    [0,             0,            1,  0.12963],
    [0,             0,            0,        1]
]

# Transformation from base to right wrist 2
b_T_rw2=np.mat(b_T_rs0)*np.mat(s0_T_w2)

# Set a point at the origin of the w2 frame
w2P=np.mat([0,0,0,1])  

# Transform w2p with respect to body frame: gives a displacement from base to point at wrist. 
bP=np.mat(b_T_rw2)*np.mat(w2P.transpose())  

# Get the Robot's Right Arm Joint Angles
angles = limb.joint_angles() 

# Get actual pose for right arm
pose=limb.endpoint_pose()
print pose['position'] # actual position of right arm end point

# Compare to the one we computed from our forward Kinematics
print bP # position of w2 origin from Forward Kinematics

# I am getting different bP and pose['position']
# ASSUMPTION: I dont have any gripper attached to w2, therefore assuming origin of w2 = limb.endpoint_pose()
