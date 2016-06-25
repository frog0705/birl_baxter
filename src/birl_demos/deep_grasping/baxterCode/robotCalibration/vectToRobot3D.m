% Project a vector from world to robot space. Same as projecting a point,
% except we ignore the origin.

function V = vectToRobot3D(V,xAx,yAx,zAx)

V = pointToRobot3D(V,[0 0 0]',xAx,yAx,zAx);