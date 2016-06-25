% Gives the azimuth and elevation for the given vector V with respect to
% the coordinate frame defined by R (assumes coincident origins)
%
% az is defined based on the projection of V into the z-x plane defined by
% R, el is the rotation around the new x axis after applying the azimuth
% rotation to get the z axis to align with V

function [az,el] = relativePolar(V,R)

xP = dot(V,R(:,1));
yP = dot(V,R(:,2));
zP = dot(V,R(:,3));

% We want azimuth relative to the z axis, but to get a right-handed
% rotation, need to use z as the Y component for atan2, so just add pi/4
% (90 deg)
az = angToPiRange(atan2(zP,xP));
el = atan2(yP,norm([xP zP]));

