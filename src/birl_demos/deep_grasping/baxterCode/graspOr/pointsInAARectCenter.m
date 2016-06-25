% Computes a mask for the points in the center of an axis-aligned
% rectangle, given by the 4x2 matrix rectPoints, where each row corresponds
% to a corner point, and the 1st and 2nd columns correspond to the X and Y
% coordinates, respectively.
%
% The rectangle will be contracted by a factor of [X/Y]_FRAC in the
% appropriate directions before masking.

function inRect = pointsInAARectCenter(imPoints,rectPoints)

X_FRAC = 3;
Y_FRAC = 4/3;

xMean = mean(rectPoints(:,1));
pDist = rectPoints(:,1) - mean(rectPoints(:,1));
pDist = pDist/X_FRAC;
rectPoints(:,1) = xMean + pDist;

yMean = mean(rectPoints(:,2));
pDist = rectPoints(:,2) - mean(rectPoints(:,2));
pDist = pDist/Y_FRAC;
rectPoints(:,2) = yMean + pDist;

inRect = sign(imPoints(:,1) - rectPoints(1,1)) ~= sign(imPoints(:,1) - rectPoints(3,1))...
    & sign(imPoints(:,2) - rectPoints(1,2)) ~= sign(imPoints(:,2) - rectPoints(3,2));