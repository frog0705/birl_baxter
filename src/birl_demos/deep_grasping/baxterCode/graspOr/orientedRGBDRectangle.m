function [I2,D2] = orientedRGBDRectangle(I,D,rectPoints)

SCALE = 1;

if any(isnan(rectPoints(:)))
    I2 = NaN;
    D2 = NaN;
    return;
end

gripAng = atan2(rectPoints(1,2) - rectPoints(2,2),rectPoints(1,1)-rectPoints(2,1));
[imX,imY] = meshgrid(1:size(I,2),1:size(I,1));
imPoints = [imX(:),imY(:)];

alignRot = rotMat2D(gripAng);

rectPointsRot = rectPoints * alignRot;
imPointsRot = imPoints * alignRot;

inRect = pointsInAARect(imPointsRot,rectPointsRot);
newPoints = imPointsRot(inRect,:);
newPoints = bsxfun(@minus,newPoints,min(newPoints));
newPoints = newPoints * SCALE + 1;


I2 = zeros(round(max(newPoints(:,2))),round(max(newPoints(:,1))),3);
D2 = zeros(round(max(newPoints(:,2))),round(max(newPoints(:,1))));

newInd = sub2ind(size(I2(:,:,1)),round(newPoints(:,2)),round(newPoints(:,1)));

for i = 1:3
    channel = I(:,:,i);
    newChannel = zeros(size(I2,1),size(I2,2));
    newChannel(newInd) = channel(inRect);
    I2(:,:,i) = newChannel;
end

D2(newInd) = D(inRect);

