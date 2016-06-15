function R = rotAroundZ(th)

cTh = cos(th);
sTh = sin(th);

R = [cTh -sTh 0; sTh cTh 0; 0 0 1];