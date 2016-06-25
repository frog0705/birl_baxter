% Masks in the largest foreground blob (connected component) in image I,
% which is assumed to have constant background color BGColor. 
%
% Can optionally specify a padding size for the mask, which might help deal
% with noisy input

function mask = maskInObjectFlatBG(I, bgColor, padSz)

% Minimum L2 distance from background color to consider a pixel foreground
OFF_THRESH = 150;

if nargin < 3
    padSz = 0;
end

% Find foreground pixels with color thresholding
bgColor = colorToThirdDim(bgColor);

diff = sqrt(sum(abs(bsxfun(@minus,I,bgColor)).^2,3));
diff = diff > OFF_THRESH;

% Run connected components
CC = bwconncomp(diff,8);

maxObj = -1;
maxSz = -1;

% Find the largest connected component
for i = 1:CC.NumObjects
    curSz = length(CC.PixelIdxList{i});
    if curSz > maxSz
        maxObj = i;
        maxSz = curSz;
    end
end

% Create and pad the mask
mask = zeros(size(I,1),size(I,2));

maskInd = CC.PixelIdxList{maxObj};

mask(maskInd) = 1;

padFil = ones(padSz*2 + 1);
mask = conv2(mask,padFil,'same') > 0;
