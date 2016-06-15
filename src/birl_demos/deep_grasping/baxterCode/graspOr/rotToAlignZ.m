% Finds a rotation matrix which aligns the Z axis of an identity
% rotation matrix to the given axis. Specifically, finds a rotation that's
% a composition of a rotation around the Y axis, followed by the X axis,
% since this is easy to compute.

function R = rotToAlignZ(newZ)

az = atan2(newZ(1),newZ(3));
el = -atan2(newZ(2),norm([newZ(1) newZ(3)]));

R = sphericalRot(az,el);