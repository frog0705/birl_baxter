% Project a vector from Kinect space to robot space. Same as a point,
% except origins are ignored

function V = kinectVectToRobot3D(V,N,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR)

V = kinectVectTo3D(V,N,xAxK,yAxK,zAxK);
V = vectToRobot3d(V,xAxR,yAxR,zAxR);