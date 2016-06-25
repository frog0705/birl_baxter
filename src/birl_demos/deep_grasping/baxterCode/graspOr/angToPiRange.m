% Converts the given angle into the equivalent in the range from -pi to pi

function ang = angToPiRange(ang)

if ang > 0
    ang = mod(ang,2*pi);
else
    ang = -mod(-ang,2*pi);
end

if ang > pi
    ang = ang-2*pi;
elseif ang < -pi
    ang = ang+2*pi;
end
        
    