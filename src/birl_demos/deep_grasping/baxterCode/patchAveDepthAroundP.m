% Not safe near edges of the image so just don't use it there OK?

function z = patchAveDepthAroundP(P,D)

AVE_WD = 5;

rRange = P(2)-AVE_WD:P(2)+AVE_WD;
cRange = P(1)-AVE_WD:P(1)+AVE_WD;

z = meanIgnoreZeros(D(rRange,cRange));