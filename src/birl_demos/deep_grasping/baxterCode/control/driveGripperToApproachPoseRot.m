% Drives the gripper to a particular pose, taking the orientation as a
% rotation matrix.
%
% Drives to an approach pose for the given point - i.e. the actual position
% will be set APPR_OFFSET meters back from the given point along the
% approach vector (Z axis of the rotation matrix)

function driveGripperToApproachPoseRot(P,R)

APPR_OFFSET = 0.1;

ax = R(:,3);

P = P - ax*APPR_OFFSET;

orQuat = qGetQ(R);

driveGripperToPoseQuat(P,orQuat);