% Drives the gripper to a particular pose, taking the orientation in
% axis/angle form, specifying the Z axis of the gripper and the rotation
% around that axis. 
%
% Drives to an approach pose for the given point - i.e. the actual position
% will be set APPR_OFFSET meters back from the given point along the given
% approach axis.
%
% Computes and returns the rotation matrix for the axis/angle combination,
% so we don't have to keep re-computing it.

function orRot = driveGripperToApproachPoseAA(P,ax,ang)

APPR_OFFSET = 0.1;

ax = unitVec(ax);

% Offset the point
P = P - ax*APPR_OFFSET;

% Compute the rotation matrix and quaternion for the axis/angle rotation
orRot = getGripperMatrix(ax,ang);
orQuat = qGetQ(orRot);

% Make the robot go
driveGripperToPoseQuat(P,orQuat);