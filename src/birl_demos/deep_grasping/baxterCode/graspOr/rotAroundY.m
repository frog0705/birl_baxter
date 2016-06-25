function R = rotAroundY(th)

cTh = cos(th);
sTh = sin(th);

R = [cTh 0 sTh; 0 1 0; -sTh 0 cTh];