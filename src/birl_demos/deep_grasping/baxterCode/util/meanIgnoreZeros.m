function val = meanIgnoreZeros(A)

A(A == 0) = NaN;

val = nanmean(A(:));