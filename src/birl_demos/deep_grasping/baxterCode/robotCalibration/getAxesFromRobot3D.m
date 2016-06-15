% Get the axes for projecting a 3D point to the robot's frame. Takes a
% series of points corresponding to Baxter's reported end-effector position
% when the gripper is pointing downwards over the following coordinates in
% some world frame (NOT Baxter's coordinates):
%
% POr: (0, 0, 0)
% PX : (1, 0, 0)
% PY : (0, 1, 0)
% PZ : (1, 1, 1)
% 
% The X and Y axes can also be negated - if this is the case, xSign/ySign
% should be set to -1. If no values are provided for these, 1 is assumed.

function [POr,xAx,yAx,zAx] = getAxesFromRobot3D(POr,PX,PY,PZ,xSign,ySign)

% Length of Baxter's gripper
VERT_OFFSET = 0.075;

if nargin < 5
    xSign = 1;
end

if nargin < 6
    ySign = 1;
end

% X and Y axes are just the vector from the origin to the appropriate
% points
xAx = xSign*(PX - POr);
yAx = ySign*(PY - POr);

% Z point is (1,1,1) so need to remove the other components
zAx = PZ - POr - xSign*xAx - ySign*yAx;

% Shift the origin downwards. This is because points are taken from the top
% of the gripper, but we want the actual gripping point. Don't need to
% shift all the points, since axes will be the same, just need to shift
% origin.
POr = offsetZ(POr,VERT_OFFSET);
