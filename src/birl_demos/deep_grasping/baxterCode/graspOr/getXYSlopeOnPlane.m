% Gets the slope of the intersection between the plane with the given
% normal and the X-Y plane, in the base (identity) frame

function m = getXYSlopeOnPlane(N)

m = -N(1)/N(2);