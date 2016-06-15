% Rotates the given frame around its Z axis to get the Y axis to lie in the
% X-Y plane, i.e. be parallel to the ground plane.

function R = rotToLevelYInXYPlane(R)

% Find the slope of the intersection of the X-Y plane in the base frame 
% and the plane normal to the Z axis of the current frame
xySlop = getXYSlopeOnPlane(R(:,3));

% Use this to get a vector for this intersection in the base frame
if abs(xySlop) < inf
    PXY = [1 xySlop 0]';
else
    PXY = [0 sign(xySlop) 0]';
end

% Project to current frame
PXY = R'*PXY;

% Use the vector to determine the rotation to align the Y axis. Add pi/2 to
% the result of atan2 to align Y rather than X
rollAng = atan2(PXY(2),PXY(1)) + pi/2;

% End result is a rotation around the Z axis by this amount
R = rotAroundZ(rollAng);