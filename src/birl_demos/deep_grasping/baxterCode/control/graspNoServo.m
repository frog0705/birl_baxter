% Executes the grasp for the given point and gripper orientation.
% Returns the final position of the gripper.

function P = graspNoServo(P,gripR)

% Height to lift the object to
AWAY_OFFSET = 0.3;

openGripper;

oldP = P;

P = graspPositionForPose(P,gripR);

driveFromApproachToGrasp(oldP,P,gripR,5);

closeGripper;

P(3) = P(3) + AWAY_OFFSET;

driveGripperToPoseRot(P,gripR);