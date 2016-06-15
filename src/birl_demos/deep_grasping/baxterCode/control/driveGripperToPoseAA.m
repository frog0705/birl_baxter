% Drives the gripper to a particular pose, taking the orientation in
% axis/angle form, specifying the Z axis of the gripper and the rotation
% around that axis. 
%
% Computes and returns the rotation matrix for the axis/angle combination,
% so we don't have to keep re-computing it.

function orRot = driveGripperToPoseAA(P,ax,ang)

orRot = alignToAxAndLevel(ax)*rotAroundZ(ang);
orQuat = qGetQ(orRot);

driveGripperToPoseQuat(P,orQuat);