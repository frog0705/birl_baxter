% Computes a rotation to align the Z axis to the given vector, and "level"
% the Y axis, i.e. rotate around Z to get the Y axis parallel to the ground
% plane.

function R = alignToAxAndLevel(V)

R = rotToAlignZ(V);
R = R*rotToLevelYInXYPlane(R);