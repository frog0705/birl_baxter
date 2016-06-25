% Finds the point with minimum depth inside the center region of the given
% grasping rectangle in the given depth image. Returns the average surface
% normal, in robot space, around that point, and the depth at that point.

function [N,minD] = robotNormAroundClosestPt(D,rect,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR)

D = double(D);

inRect = double(pointsInRectCenter(D,dbnRectToOld(rect)));

[minD,minInd] = minIgnoreZero(D.*inRect);

[minP(2), minP(1)] = ind2sub(size(D),minInd);

N = aveRobotNormAroundP(minP,D,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR);