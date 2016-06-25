% Prompts user to select four marked points (listed as world-space coords)
% in the given RGB and depth images from Kinect.
%
% POr: (0, 0, 0)
% PX : (1, 0, 0)
% PY : (0, 1, 0)
% PZ : (1, 1, 1)

function [POr,PX,PY,PZ] = getAxisPointsFromKinect(I,D)

disp('Select origin');

POr = selectKinectPoint(I,D);

disp('Select 2nd X axis point');

PX = selectKinectPoint(I,D);

disp('Select 2nd Y axis point');

PY = selectKinectPoint(I,D);

disp('Select 2nd Z axis point (1,1,1)');

PZ = selectKinectPoint(I,D);