#!/usr/bin/python

import rospy
import baxter_interface
from baxter_pykdl import baxter_kinematics
from baxter_interface import CHECK_VERSION
from numpy import (matrix,double)
import time
from numpy.linalg  import *
from numpy import *
import numpy as np

def null(A, eps=1e-3):      
    u,s,vh = np.linalg.svd(A,full_matrices=1,compute_uv=1)
    null_space = np.compress(s <= eps, vh, axis=0)
    return vh[:,6]#null_space.T

def Movejac():    
    leftangle=leftarm.joint_angles()
    leftKin=baxter_kinematics('left') 
    vel=matrix("0;0;0.1;0;0;0")
    Ljac=leftKin.jacobian_pseudo_inverse()
    dp=Ljac*vel
    cmd={}
    cmd['left_s0']=dp[0]
    cmd['left_s1']=dp[1]
    cmd['left_e0']=dp[2]
    cmd['left_e1']=dp[3]
    cmd['left_w0']=dp[4]
    cmd['left_w1']=dp[5]
    cmd['left_w2']=dp[6]
   # for i,joint in enumerate(leftarm.joint_names()):
   #     cmd[joint]=dp[i]
    leftarm.set_joint_velocities(cmd)

def nullspace():
    leftKin=baxter_kinematics('left')
    leftarm=baxter_interface.Limb('left')
    #leftangle=leftarm.joint_angles()
    Ljac=leftKin.jacobian()
    Ns=null(Ljac,0.1)
    qd_ns=np.matrix([0,0,0,0,0.5,0,0 ]).T
    dp=Ns*np.linalg.pinv(Ns)*qd_ns
    dp=dp/dp[2]*qd_ns[2]
    
    cmd={}
    cmd['left_s0']=dp[0]
    cmd['left_s1']=dp[1]
    cmd['left_e0']=dp[2]
    cmd['left_e1']=dp[3]
    cmd['left_w0']=dp[4]
    cmd['left_w1']=dp[5]
    cmd['left_w2']=dp[6]
 #   for i,joint in enumerate(leftarm.joint_names()):
 #       cmd[joint]=dp[i]
    leftarm.set_joint_velocities(cmd)
    

if __name__ == "__main__":
    rospy.init_node('baxter_kin')
    print 'initial node successd'
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    rs.enable()
    print 'enable baxter successed'
    leftarm=baxter_interface.Limb('left')
    
    
    print 'move leftarm to the initial position'
    leftarm.move_to_neutral()
    print '******  move leftarm in x direction    ******'
    count=0  
    while count<100:
        Movejac( )
        count=count+1
        
        
    print 'move leftarm to the initial position'
    leftarm.move_to_neutral()
    count=0 
    print '****** move in  Null  space   ******'
    while count<100:
        nullspace()
        #rospy.sleep(0.)
        count=count+1
    
        
   