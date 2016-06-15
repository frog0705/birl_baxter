% Not safe near edges of the image so just don't use it there OK?

function DP = depthPatchAroundP(P,D)

PATCH_WD = 5;

rRange = max(P(2)-PATCH_WD,1):min(P(2)+PATCH_WD,size(D,1));
cRange = max(P(1)-PATCH_WD,1):min(P(1)+PATCH_WD,size(D,2));

DP = D(rRange,cRange);