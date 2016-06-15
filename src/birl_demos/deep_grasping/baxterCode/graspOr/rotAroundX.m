function R = rotAroundX(th)

cTh = cos(th);
sTh = sin(th);

R = [1 0 0; 0 cTh -sTh; 0 sTh cTh];