% Transform a point P from Kinect space, using the given points/axes in
% Kinect and robot spaces

function P = kinectPointToRobot3D(P,POrK,N,xAxK,yAxK,zAxK,POrR,xAxR,yAxR,zAxR)

P = kinectPointTo3D(P,POrK,N,xAxK,yAxK,zAxK);
P = pointToRobot3D(P,POrR,xAxR,yAxR,zAxR);
