function [N,minD] = normAroundClosestPt(D,rect)

D = double(D);

inRect = double(pointsInRectCenter(D,dbnRectToOld(rect)));

[minD,minInd] = minIgnoreZero(D.*inRect);

[minP(2), minP(1)] = ind2sub(size(D),minInd);

N = aveNormAroundP(minP,D);