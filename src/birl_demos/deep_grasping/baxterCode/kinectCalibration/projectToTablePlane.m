% Project point P to table plane with normal N, along the given Z axis zAx

function [PProj,ZCoord] = projectToTablePlane(P,POr,N,zAx)

P = P - POr;

ZCoord = dot(P,N)/dot(zAx,N);

PProj = P - ZCoord*zAx;
PProj = PProj + POr;