% Computes the new, offset position from point P, based on the visual
% servoing control command for image I. Servos along the Y-axis of the
% gripper rotation matrix gripR

function newP = visServoOffset(P,I,gripR,bgColor)

cmd = controlCommandForImage(I,bgColor);

newP = shiftAlongY(P,gripR,cmd);