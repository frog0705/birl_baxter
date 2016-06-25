% Computes the average surface normal, in robot space, in a window around
% point P. Converts points inside that window to robot space first - this
% is important to get a correct surface normal, and works much better than
% computing the surface normal in Kinect space and attempting to translate
% it. 

function nMean = aveRobotNormAroundP(P,D,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR)

% Points further than this in depth from the center point will be ignored.
% Avoids including background points, etc.
DIST_THRESH = 30;

P = round(P);

D = smoothDepthForNorm(D);

DP = depthPatchAroundP(P,D);

mask = thresholdFromCenterValue(DP,DIST_THRESH);

N = getSurfNormRobot(DP,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR);

nMean = zeros(3,1);

for i = 1:3
    chan = N(:,:,i);
    chan(~mask) = NaN;
    nMean(i) = nanmean(chan(:));
end

nMean = unitVec(nMean);