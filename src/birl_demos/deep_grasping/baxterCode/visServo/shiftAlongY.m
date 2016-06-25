% Translates point P by shifting it along the Y axis of the given rotation
% matrix, scaled according to the given scale

function P = shiftAlongY(P,R,scale)

P = P + scale*R(:,2);