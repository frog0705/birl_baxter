% Drives the gripper from an approach pose to a grasping pose. Takes
% several steps, to attempt to get the gripper to move in a (relatively)
% straight line, and avoid disrupting the object.
% 
% Arguments:
% 
% P : object surface point - corresponds to the grasp projected onto the
% surface of the object.
% 
% graspP : grasping point - final location of the gripper to grasp the
% object. Assumed to be some shift forwards along the gripper Z axis
% (approach vector) from P. Might not always be a constant shift, though,
% to avoid collision i.e. with the table, other objects, parts of the
% current object, etc.
%
% gripR : gripper rotation matrix. Z is the approach vector
% 
% nSteps: number of steps to take when moving from the approach to grasping
% poses. 
%
% Assumes that the gripper is positioned APPR_OFFSET meters back from P
% along the approach vector. 

function driveFromApproachToGrasp(P,graspP,gripR,nSteps)

APPR_OFFSET = 0.1;

extraOff = norm(graspP - P);

% Compute total offset along the approach vector from approach to grasping
% positions
totalOff = APPR_OFFSET + extraOff;

ax = gripR(:,3);

% Step along the approach vector from the approach to grasp pose
for i = 1:nSteps
    curOff = totalOff*(nSteps-i)/nSteps;
    
    driveGripperToPoseRot(graspP - curOff*ax,gripR);
end