% Prompt user to draw a box on the image, then return a center point for
% that box as X,Y,Z coordinates. Z coordinate will be the average depth
% over the box, to help avoid outliers.

function P = selectKinectPoint(I,D)

rect = imSelectROI(I);

P = zeros(3,1);
P(1) = mean(rect.Xrange);
P(2) = mean(rect.Yrange);

DRect = D(rect.Yrange,rect.Xrange);
P(3) = meanIgnoreZeros(DRect(:));