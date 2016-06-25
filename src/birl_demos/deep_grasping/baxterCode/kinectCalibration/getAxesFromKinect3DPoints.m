% Gets the axes and table surface normal for a set of Kinect points,
% probably selected from a Kinect image using getAxisPointsFromKinect.
% These are used to transform from Kinect to world space (and probably then
% to robot space).
% 
% In world space: 
% 
% POr: (0, 0, 0)
% PX : (1, 0, 0)
% PY : (0, 1, 0)
% PZ : (1, 1, 1)
% 
% The X and Y axes can also be negated - if this is the case, xSign/ySign
% should be set to -1. If no values are provided for these, 1 is assumed.

function [N,xAx,yAx,zAx] = getAxesFromKinect3DPoints(POr,PX,PY,PZ,xSign,ySign)

if nargin < 3
    xSign = 1;
end

if nargin < 4
    ySign = 1;
end

% Find the surface normal for the table plane
N = fitTablePlane(POr,PX,PY);

% Compute the un-scaled X and Y axes
xAx = xSign*(PX - POr);
yAx = ySign*(PY - POr);

% Need to remove the X and Y components from the Z axis
zAx = PZ - POr - xSign*xAx - ySign*yAx;

% Scale the X and Y axes so that they project PX/PY to a unit distance from
% the origin
xNorm = norm(xAx);
xAx = xAx/(xNorm^2);

yNorm = norm(yAx);
yAx = yAx/(yNorm^2);

% We use the Z axis differently, so don't normalize that