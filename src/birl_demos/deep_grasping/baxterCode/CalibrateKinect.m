X_SIGN = -1;
Y_SIGN = 1;

goAndGrabIm;

[POrK,PXK,PYK,PZK] = getAxisPointsFromKinect(I,D);

[N,xAxK,yAxK,zAxK] = getAxesFromKinect3DPoints(POrK,PXK,PYK,PZK,-1,1);