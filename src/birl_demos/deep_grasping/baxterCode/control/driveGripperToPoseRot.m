% Drives the gripper to a particular pose, taking the orientation as a
% rotation matrix.

function driveGripperToPoseRot(P,gripR)

orQuat = qGetQ(gripR);

driveGripperToPoseQuat(P,orQuat);