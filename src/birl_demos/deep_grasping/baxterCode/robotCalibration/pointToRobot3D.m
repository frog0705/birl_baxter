% Takes a point in world space and translates it to Baxter's coordinate
% frame, used for manipulation

function P = pointToRobot3D(P,POr,xAx,yAx,zAx)

P = POr + P(1)*xAx + P(2)*yAx + P(3)*zAx;