% Computes the visual servoing-based proportional control command for an
% image. The error used is the difference between the center column of the
% largest foreground blob detected in the camera image (based on color
% segmentation from the given background color) and the fixed target column
% (probably the center of the image).
%
% Uses only some central region (vertically) of the image, as defined by
% BUF. So, if BUF is 70, we'd shave 70 rows off the top and bottom of the
% image. This helps the servoing to focus on the region to be grasped.
%
% Stops when the error is within some deadzone of zero, since Baxter
% probably won't be able to reposition within this range and we'll just get
% stuck in a loop.

function cmd = controlCommandForImage(I,bgColor)

BG_COLOR = 170;
TGT_COL = 160;
DEADZONE = 10;
KP = 1/(3e3);

BUF = 70;

% If BG color wasn't supplied, just use the default
if nargin < 2
    bgColor = BG_COLOR * ones(3,1);
end

% Mask object out from background
objMask = maskInObjectFlatBG(double(I(BUF+1:end-BUF,:,:)),bgColor,0);

% Find central column and compute error
centC = centerColOfMask(objMask);

diff = TGT_COL - centC;

% If we're inside the deadzone, no command, otherwise use proportional
% control with the set KP
if abs(diff) < DEADZONE
    cmd = 0;
else
    cmd = diff*KP;
end