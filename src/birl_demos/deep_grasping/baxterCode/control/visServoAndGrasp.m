% Executes the grasp with the given position and gripper orientation, with
% visual servoing to center the object with respect to the gripper. This
% may not work for objects where the graspable region only spans part of
% the object (e.g. the rim of a coffee mug).
%
% Returns the final position of the gripper.

function P = visServoAndGrasp(P,gripR)

AWAY_OFFSET = 0.3;

openGripper;

% Shift the camera to the gripper's center point. This lets us center the
% grasp with respect to the gripper, rather than the camera.
P = offsetForCam(P,gripR,1);

driveGripperToApproachPoseRot(P,gripR);

P = runVisualServo(P,gripR);

% Move the gripper back to the position the camera ended up in after visual
% servoing
P = offsetForCam(P,gripR,-1);

oldP = P;

% Drive from the current position to a grasping position, where the gripper
% spans the grasp point, in steps - this is to attempt to force Baxter to
% move the gripper in a (mostly) straight line along the approach vector
P = graspPositionForPose(P,gripR);

driveFromApproachToGrasp(oldP,P,gripR,5);

closeGripper;

P(3) = P(3) + AWAY_OFFSET;

driveGripperToPoseRot(P,gripR);