% Rotation based on an azimuth/elevation pair in spherical coordinates,
% where the azimuthal rotation occurs in the X-Z plane, and the elevation
% is defined in the (rotated) Y-Z plane. 

function R = sphericalRot(az,el)

R = rotAroundY(az)*rotAroundX(el);