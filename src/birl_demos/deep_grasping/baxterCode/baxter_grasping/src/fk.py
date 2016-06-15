#!/usr/bin/env python

# Copyright (c) 2013, Rethink Robotics
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

import signal
import math
import random
import time
import argparse
import roslib
roslib.load_manifest('joint_velocity')
import rospy

from std_msgs.msg import (
    UInt16,)
from sensor_msgs.msg import (
    JointState,)
from baxter_msgs.msg import (
    JointVelocities,
    JointCommandMode,)

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

    def bringToAngles(self, limb, e0b, e1b, s0b, s1b, w0b, w1b, w2b):
        #self.set_neutral()
        """
        Brings left arm to the desired angles

        """
        rate = rospy.Rate(1000);
        start = rospy.Time.now()

        done = False
        print("Starting to move. Press any key to stop...")
#        while not done and not rospy.is_shutdown():
#            c = iodevices.getch()
#            if c:
#                done = True
#            else:
#                self._pub_rate.publish(1000)
#                elapsed = rospy.Time.now() - start
#                cmd = dict(zip(self._joint_names, [v_funcs[i](elapsed) for i in range(len(self._joint_names))]))
#                self._left_arm.set_velocities(cmd)
#                rate.sleep()
#        self._left_arm.set_pose(   dict(zip(['e0', 'e1', 's0', 's1', 'w0', 'w1', 'w2'], [-1.15, 1.32, -0.11, -0.62, 0.80, 1.27, 2.39]))   )
        self._left_arm.move_to_joint_positions(dict(zip(['e0', 'e1', 's0', 's1', 'w0', 'w1', 'w2'], [float(e0b), float(e1b), float(s0b), float(s1b), float(w0b), float(w1b), float(w2b)])))
        #self._left_arm.move_to_joint_positions(   dict(zip(['e0', 'e1', 's0', 's1', 'w0', 'w1', 'w2'], [-0.893885199733119,1.2679789443546783, -0.6385064965107536, -0.3050569420347243, 1.0130868024843116, 1.0695686598843879, -0.8670164430795886]))   )

        grip_left = baxter_interface.Gripper('left')
        grip_right = baxter_interface.Gripper('right')
        bindings = {
    #   key: (function, args, description)
        ',': (grip_left.close, [], "left: gripper close"),
        'm': (grip_left.open, [], "left: gripper open"),
        '/': (grip_left.calibrate, [], "left: gripper calibrate"),
        }
        if not done and not rospy.is_shutdown():
            c = iodevices.getch()
            if c:
                #catch Esc or ctrl-c
                if c in ['\x1b', '\x03']:
                    done = True
                elif c in bindings:
                    cmd = bindings[c]
                    #expand binding to something like "set_j(right, 's0', 0.1)"
                    cmd[0](*cmd[1])
                    print("command: %s" % (cmd[2],))
                else:
                    print("key bindings: ")
                    print("  Esc: Quit")
                    print("  ?: Help")
                    for key, val in sorted(bindings.items(), key=lambda x: x[1][2]):
                        print("  %s: %s" % (key, val[2]))





        print("IDK")
        #raw_input()
	#time.sleep(6)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("limb", help="the limb to test <left | right>")
    parser.add_argument("e0", help="the limb to test <left | right>")
    parser.add_argument("e1", help="the limb to test <left | right>")
    parser.add_argument("s0", help="the limb to test <left | right>")
    parser.add_argument("s1", help="the limb to test <left | right>")
    parser.add_argument("w0", help="the limb to test <left | right>")
    parser.add_argument("w1", help="the limb to test <left | right>")
    parser.add_argument("w2", help="the limb to test <left | right>")
    args = parser.parse_args()

    print("Initializing node... ")
    rospy.init_node("rethink_rsdk_joint_velocity")
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable()
    print("Enabling robot... ")
    rs.enable()

    orienter = Thetaposition()
    orienter.bringToAngles(args.limb,args.e0,args.e1,args.s0,args.s1,args.w0,args.w1,args.w2)

    #print("Disabling robot... ")
    #rs.disable()
    print("done.")
