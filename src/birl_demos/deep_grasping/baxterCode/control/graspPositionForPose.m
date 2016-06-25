% Project a pose, which presumably positions the tips of the grippers right
% at the edge of the object, into an actual grasping position, which
% positions the gripper to grasp.
%
% Do so by shifting along the Z axis (direction the gripper's pointing) by
% the length of the gripper.
%
% Have to be careful not to run the gripper into the table - Baxter's
% compliant, so it won't be death, but the gripper won't be able to close.
% Do this by taking the min distance between the gripper length and the
% distance along the Z axis to the table.

function graspP = graspPositionForPose(P,gripR)

% Height of the table, in robot coords
TBL_HT = -0.24;

GRIP_LEN = 0.075;

% Fraction of the gripper length to drive forwards
OFFSET_SCALE = 0.7;

% Fraction of the distance to the table to drive forwards, in cases where
% we'll hit the table firstS
TBL_OFF_SCALE = 0.9;

ax = gripR(:,3);

tblOff = (TBL_HT - P(3))/ax(3);

if tblOff > 0 && tblOff < GRIP_LEN*(OFFSET_SCALE + 1)
    graspP = P + ax*(tblOff - GRIP_LEN)*TBL_OFF_SCALE;
else
    graspP = P + ax*GRIP_LEN*OFFSET_SCALE;
end

