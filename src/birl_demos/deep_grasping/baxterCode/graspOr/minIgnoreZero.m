% Computes the minimum value of A and its index, ignoring any values of
% zero

function [minVal,minInd] = minIgnoreZero(A)

A(A == 0) = inf;

[minVal,minInd] = min(A(:));