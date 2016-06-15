% Computes a mask of pixels which are more than some threshold's worth from
% the value of the center pixel of the given depth image.

function M = thresholdFromCenterValue(D,thresh)

centVal = D(round(size(D,1)/2),round(size(D,2)/2));

M = D - centVal < thresh;