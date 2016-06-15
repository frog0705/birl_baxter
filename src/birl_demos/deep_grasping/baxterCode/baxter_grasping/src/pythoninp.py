#!/usr/bin/env python

import sys, os, time, openravepy, numpy, signal, math, random, argparse, subprocess
import roslib
roslib.load_manifest('inverse_kinematics')
roslib.load_manifest('joint_velocity')
import rospy
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header
from baxter_msgs.srv import SolvePositionIK
from baxter_msgs.srv import SolvePositionIKRequest
from std_msgs.msg import (
    UInt16,)
from sensor_msgs.msg import (
    JointState,)
from baxter_msgs.msg import (
    JointVelocities,
    JointCommandMode,)
from optparse import OptionParser
from openravepy.misc import OpenRAVEGlobalArguments
import baxter_interface
import iodevices

class Thetaposition():

    def __init__(self):
        """
        Brings left arm to the desired angles

        """
        self._pub_rate = rospy.Publisher('/robot/joint_state_publish_rate', UInt16)
        self._left_arm = baxter_interface.limb.Limb("left")
        self._joint_names = ['s0','s1','e0','e1','w0','w1','w2',]

        # set joint state publishing to 1000Hz
        self._pub_rate.publish(1000)

    def set_neutral(self):
        """
        Sets left arm back into a neutral pose

        """
        print("Moving to neutral pose...")
        self._left_arm.set_neutral_pose()

    def bringToAngles(self,lj):
        #self.set_neutral()
        """
        Brings left arm to the desired angles

        """
        rate = rospy.Rate(1000);
        start = rospy.Time.now()

        done = False
        print("Starting to move. Press red button to stop...")

        jpc = dict(zip(['e0', 'e1', 's0', 's1', 'w0', 'w1', 'w2'], [ lj['e0'], lj['e1'], lj['s0'], lj['s1'], lj['w0'], lj['w1'], lj['w2'] ]))
        print jpc
        self._left_arm.move_to_joint_positions(jpc)

        print("IDK")
        time.sleep(6)

        rate = rospy.Rate(100);
        if not rospy.is_shutdown():
            for i in range(100):
                if rospy.is_shutdown():
                    return False
                self._left_arm.set_position_mode()
                self._pub_rate.publish(100)
                rate.sleep()
            #return to normal
            self.set_neutral()
            return True

#def main(options):
def main(limb,xc,yc,zc,xq,yq,zq,wq):
    rospy.init_node("rethink_rsdk_inverse_kinematics_test")
    ns = "/sdk/robot/limb/left/solve_ik_position"
    rospy.wait_for_service(ns)
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    poses = {
        'left': PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=float(xc),
                    y=float(yc),
                    z=float(zc),
                ),
                orientation=Quaternion(
                    x=float(xq),
                    y=float(yq),
                    z=float(zq),
                    w=float(wq),
                ),
            ),
        ),
        'right': PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=xc,
                    y=yc,
                    z=zc,
                ),
                orientation=Quaternion(
                    x=xq,
                    y=yq,
                    z=zq,
                    w=wq,
                ),
            ),
        ),
    }

    ikreq.pose_stamp.append(poses[limb])
    try:
        resp = iksvc(ikreq)
    except rospy.ServiceException,e :
        rospy.loginfo("Service call failed: %s" % (e,))
    if (resp.isValid[0]):
        print("SUCCESS - Valid Joint Solution Found:")
        #Format solution into Limb API-compatible dictionary with valid joint names
        limb_joints = dict(zip([name[-2:] for name in resp.joints[0].names], resp.joints[0].angles))
        limb_joints = dict(zip(['e0', 'e1', 's0', 's1', 'w0', 'w1', 'w2'], [ limb_joints['e0'], limb_joints['e1'], limb_joints['s0'], limb_joints['s1'], limb_joints['w0'], limb_joints['w1'], limb_joints['w2'] ]))
        print limb_joints
        rospy.signal_shutdown("Extracted joint angles")
        while not rospy.is_shutdown():
            print ".",
        rospy.spin()
        print ""
        cmd = "rosrun baxter_grasping fk.py %s %f %f %f %f %f %f %f" % (limb,limb_joints['e0'], limb_joints['e1'], limb_joints['s0'], limb_joints['s1'], limb_joints['w0'], limb_joints['w1'], limb_joints['w2'])
        #print cmd
        fk_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = fk_process.communicate()
        errcode = fk_process.returncode
        print out
        print err
        print "Returned with ExitCode -> ", errcode
    else:
        print("INVALID POSE - No Valid Joint Solution Found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("limb", help="the limb to test <left | right>")
    parser.add_argument("xc", help="the limb to test <left | right>")
    parser.add_argument("yc", help="the limb to test <left | right>")
    parser.add_argument("zc", help="the limb to test <left | right>")
    parser.add_argument("xq", help="the limb to test <left | right>")
    parser.add_argument("yq", help="the limb to test <left | right>")
    parser.add_argument("zq", help="the limb to test <left | right>")
    parser.add_argument("wq", help="the limb to test <left | right>")
    args = parser.parse_args()

    main(args.limb,args.xc,args.yc,args.zc,args.xq,args.yq,args.zq,args.wq)
