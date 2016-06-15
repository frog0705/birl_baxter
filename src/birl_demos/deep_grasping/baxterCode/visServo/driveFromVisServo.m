% Re-positions the gripper from the current point using visual servoing.
% gripR gives the rotation matrix for the gripper, where the Z axis is the
% approach vector, and the Y axis will be servoed along.
%
% Also returns whether or not the servoing is done. This happens when the
% movement command is zero.

function [newP,done] = driveFromVisServo(curP,gripR,bgColor)

I = getCurHandImage();

newP = visServoOffset(curP,I,gripR,bgColor);

done = all(newP == curP);

if ~done
    driveGripperToApproachPoseRot(newP,gripR);
end

