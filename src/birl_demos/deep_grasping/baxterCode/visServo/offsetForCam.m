% Centers the camera for the given grasp. This means putting it where the
% gripper will be when grasping. Or, if sign is -1, moves it back so the
% gripper is centered.
%
% This is important because it avoids perspective issues that would crop up
% if the camera position was different from the gripper position. It means
% we can simply center the object in the hand camera's view and be sure
% that it'll be centered with respect to the gripper.

function P = offsetForCam(P,gripR,sign)

if nargin < 3
    sign = 1;
end

X_OFFSET = 0.0325*sign;
Y_OFFSET = 0.01*sign;

P = P - gripR(:,1)*X_OFFSET - gripR(:,2)*Y_OFFSET;