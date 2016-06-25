% Project a point P in Kinect space to world space, using the given origin,
% table normal, and axes.

function [P3D] = kinectPointTo3D(P,POr,N,xAx,yAx,zAx)

% First, project the point to the table, and record the Z coordinate
[PPl,P3D(3)] = projectToTablePlane(P,POr,N,zAx);

% Get point relative to the origin
PPl = PPl - POr;

% Project to the X and Y axes
P3D(1) = dot(PPl,xAx);
P3D(2) = dot(PPl,yAx);