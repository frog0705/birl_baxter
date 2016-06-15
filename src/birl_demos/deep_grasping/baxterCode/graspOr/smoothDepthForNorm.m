% Smooths out the depth channel using a local averaging filter. Can change
% to use other filters. Need to smooth before we compute normals, since
% otherwise they might be very noisy.

function D = smoothDepthForNorm(D)

AVE_SZ = 5;

D = conv2(D,ones(AVE_SZ,AVE_SZ)/(AVE_SZ^2),'same');