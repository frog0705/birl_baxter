% Takes a vector, assumed to have exactly one non-zero dimension, and
% shifts that to be the third. Used to take a color vector and shift it to
% something we can use with bsxfun on an image.

function A = colorToThirdDim(A)

myDim = find(size(A) > 1);

A = shiftdim(A,myDim - 3);