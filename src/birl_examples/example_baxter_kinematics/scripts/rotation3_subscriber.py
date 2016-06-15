#!/usr/bin/python
# -*- coding: utf-8 -*-

#jacobian column s0 s1 e0 e1 w0 w1 w2


#-----------------------------------------
# Imports
#-----------------------------------------
import pdb
import os                                          # used to clear the screen
import math
from numpy import *
from numpy.linalg import *
import rospy
import baxter_interface
from baxter_interface import CHECK_VERSION
from baxter_pykdl import baxter_kinematics
from rbx1_nav.transform_utils import quat_to_angle # Convert quaternions to euler
import geometry_msgs
import PyKDL
from std_msgs.msg import String

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

def dquat_to_dangle4(quat_now,quat_ref,K_inter):
    quat_ref1x=(quat_ref.x-quat_now.x)/K_inter+quat_now.x
    #print 'cal'
    #print 'quat_ref.x', quat_ref.x
    #print 'quat_now.x', quat_now.x
    #print '(quat_ref.x-quat_now.x)/K_inter', (quat_ref.x-quat_now.x)/K_inter
    #print 'quat_ref1x', quat_ref1x
    quat_ref1y=(quat_ref.y-quat_now.y)/K_inter+quat_now.y
    quat_ref1z=(quat_ref.z-quat_now.z)/K_inter+quat_now.z
    quat_ref1w=(quat_ref.w-quat_now.w)/K_inter+quat_now.w
    #print 'interpolation target quaternion', quat_ref1x, quat_ref1y, quat_ref1z, quat_ref1w
    rot_now=PyKDL.Rotation.Quaternion(quat_now.x,quat_now.y,quat_now.z,quat_now.w)
    rot_ref1=PyKDL.Rotation.Quaternion(quat_ref1x,quat_ref1y,quat_ref1z,quat_ref1w)
    trans_rot=rot_ref1*rot_now.Inverse()
    dvec=matrix([[trans_rot[2,1]],[trans_rot[0,2]],[trans_rot[1,0]]])
    return dvec

def dquat(quat_now,quat_ref):
    x=quat_ref.x-quat_now.x
    y=quat_ref.y-quat_now.y
    z=quat_ref.z-quat_now.z
    w=quat_ref.w-quat_now.w
    dvec0=matrix([w,x,y,z]).T
    dquat_error=norm(dvec0)
    return dquat_error

def get_ref_pose(Pose):
    global ref_pos
    global ref_quaternion
    global ref_pose
    ref_pose=Pose
    ref_pos=matrix([Pose['position'].x, Pose['position'].y, Pose['position'].z]).T
    ref_quaternion=Pose['orientation']
    #rostopic pub -r 100 /hly_ref_pose_xyzxyzw geometry_msgs/Pose '{position: {x: 4, y: -0.4, z: -0.2}, orientation: {x: -0.18301, y: 0.68301, z: 0.18301, w: 0.68301}}'
    #rostopic pub /hly_ref_pose_xyzxyzw geometry_msgs/Pose '{position: {x: 4, y: -0.4, z: -0.2}, orientation: {x: -0.18301, y: 0.68301, z: 0.18301, w: 0.68301}}'


def main():

    # If you want to debug, uncomment the next line.
    # pdb.set_trace()

    # Initialize node
    rospy.init_node('example_kdl_hly_rotation')

    rospy.Subscriber("hly_ref_pose_xyzxyzw",geometry_msgs.msg.Pose,get_ref_pose)

    # Call routine to enable the robot
    rs=enable_Baxter()

    loop=rospy.Rate(100)

    # Set gain for multiplying error
    Kang=1
    K_inter=100
    Kpos=0.1
    global ref_pose
    global ref_pos
    global ref_quaternion

    rLimb=baxter_interface.Limb('right')

    rKin = baxter_kinematics('right')

    # Get Joint names
    jNamesR_ordrered=rLimb.joint_names()
    jNamesR=['right_s0','right_s1','right_w0','right_w1','right_w2','right_e0','right_e1']

    # Set a reference pose: [x,y,z,vx,vy,vz,w]. This one is near the home position of arm.
    # Home joint angle position for baxter_world_home.launch is approximately:
    # [0.58,-0.19,0.23,-0.11,0.99,0.01,0.02]
    #   p: x       y         z   q:   x       y      z       w
    #0.19609, 0.98019, -0.0020525,0.027838     good    *rotz(pi/5)
    #0.43821 < -0.34115, -0.80712, -0.20036 >   bad     *rotz(pi/3)*roty(pi/3)
    #0.2612 < 0.38292, 0.88049, -0.099468 >   good  *rotz(pi/3)*roty(-pi/6)
    #0.56242, 0.35355, 0.14645,0.73296    good    *rotx(pi/3)*roty(pi/4)*rotx(pi/12)   xyz 0.54671443, -0.65902167 , 0.22243689
    #0.4890, 0.2499,-0.0031,0.8356  good 0.6, -0.7 , -0.1
    #-0.18301, 0.68301, 0.18301 ,0.68301  good  0.4, -0.5 , -0.1

    ref_pose={'position':geometry_msgs.msg.Point(0.3, -0.5 , -0.1), \
    'orientation':geometry_msgs.msg.Quaternion(-0.18301, 0.68301, 0.18301 ,0.68301)}
    ref_pos=matrix([ref_pose['position'].x, ref_pose['position'].y, ref_pose['position'].z]).T
    ref_quaternion=ref_pose['orientation']

    print 'The reference pose is: '
    print(ref_pose)

    while not rospy.is_shutdown():
        print 'example3_kdl for the right arm...'

        # 1. Get the current angles and jacobian as numpy matrices
        rAngles=rLimb.joint_angles() # returns as s0s1w0w1w2e0e1
        rAnglesM=matrix(rAngles.values()).T
        jac=rKin.jacobian()
        print jac

        # 2. Compute the forward Kinematics using the Jacobian: del_p=J(q)del_q
        curr_pose=rLimb.endpoint_pose()
        curr_pos=matrix(curr_pose['position']).T
        curr_quaternion=curr_pose['orientation']


        print 'The current position is: '
        print(curr_pose)
        print 'The reference pose is: '
        print(ref_pose)

        # 3. Compute the error between reference and current positions
        dp_error=Kpos*(ref_pos-curr_pos)
        dangle=Kang*dquat_to_dangle4(curr_quaternion, ref_quaternion, K_inter)
        da_error=bmat('dp_error; dangle')

        # 4. Get a scalar distance (vector norm) to more easily interpret the error
        dp_norm=norm(dp_error)
        d_quat=dquat(curr_quaternion,ref_quaternion)
        print 'the dpnorm is %f' %dp_norm
        print 'the dquat is %f' %d_quat


        # 5. Extract the translation Jacobian
        jTrans=jac# when slicing go one dim past end

        # 6. Compute the dq using dp_error
        dq=(pinv(jTrans))*da_error
        dq0=dq.tolist()
        dq=matrix([dq0[0],dq0[1],dq0[4],dq0[5],dq0[6],dq0[2],dq0[3]])
        # 7. Add this dq to current joint Angles
        ref_anglesM=dq+rAnglesM
        ref_angles=ref_anglesM.ravel().tolist()[0]  # change back to list.[0] b/c it returns nested list.
        ref_angles=dict(zip(jNamesR,ref_angles))

        # 8. Move the Limb
        #rLimb.move_to_joint_positions(ref_angles) # need to check that indeces are in the right order
        rLimb.set_joint_positions(ref_angles)
        #print 'forward_position_kinematics', rKin.forward_position_kinematics()

        # Set the loop speed
        loop.sleep()
        # Clear the screen for easier reading
        os.system('clear')

    rospy.on_shutdown(shutdown)
    return rs



if __name__ == "__main__":
    try:
        #pdb.set_trace()
        main()
    except:
        rospy.loginfo("example_baxter_kins_right node terminated.")



