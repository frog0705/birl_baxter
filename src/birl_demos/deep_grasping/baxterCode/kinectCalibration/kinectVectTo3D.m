% Project a vector from Kinect space to world space

function V = kinectVectTo3D(V,N,xAx,yAx,zAx)

xAx = unitVec(xAx);
yAx = unitVec(yAx);
zAx = unitVec(zAx);

V = kinectPointTo3D(V,[0 0 0]',N,xAx,yAx,zAx);