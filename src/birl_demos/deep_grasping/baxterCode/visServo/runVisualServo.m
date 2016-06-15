% Keep running visual servoing until the gripper's in place (i.e. we get no
% motion command). Returns the final position of the gripper.

function P = runVisualServo(P,gripR,bgColor)

done = 0;

while ~done
    [P,done] = driveFromVisServo(P,gripR,bgColor);
end