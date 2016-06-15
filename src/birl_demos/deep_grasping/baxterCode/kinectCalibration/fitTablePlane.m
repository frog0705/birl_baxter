% Fit a plane to the given set of points, relative to POr, so it gets
% subtracted from every point. This is nice because it means the plane
% passes through (0,0,0) and we don't have to worry about the bias.

function N = fitTablePlane(POr,PX,PY)

[~,~,V] = svd([0 0 0; (PX-POr)'; (PY-POr)'],0);

N = V(:,end);