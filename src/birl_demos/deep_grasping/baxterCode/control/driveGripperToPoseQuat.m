% Drives Baxter's gripper to a given point, oriented according to the given
% quaternion. May complain and fail if Baxter can't reach that pose. 
% 
% Takes an optional height argument which will override the third coord of
% the point.

function driveGripperToPoseQuat(P,orQuat,ht)

if nargin > 2
    P(3) = ht;
end

% Call a Python script to compute the inverse kinematics for the given pose
% and drive the gripper to it. This script will listen to ctrl-C, so you
% can mash that if you realize you gave it a bad point.
system(sprintf('rosrun baxter_grasping pythoninp.py left %f %f %f %f %f %f %f',P(1),P(2),P(3),orQuat(1),orQuat(2),orQuat(3),orQuat(4)));
