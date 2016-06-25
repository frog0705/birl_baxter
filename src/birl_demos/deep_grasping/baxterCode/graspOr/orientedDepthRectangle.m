function D2 = orientedDepthRectangle(D,rectPoints)

SCALE = 1;

if any(isnan(rectPoints(:)))
    D2 = NaN;
    return;
end

gripAng = atan2(rectPoints(1,2) - rectPoints(2,2),rectPoints(1,1)-rectPoints(2,1));
[imX,imY] = meshgrid(1:size(D,2),1:size(D,1));
imPoints = [imX(:),imY(:)];

alignRot = rotMat2D(gripAng);

rectPointsRot = rectPoints * alignRot;
imPointsRot = imPoints * alignRot;

inRect = pointsInAARect(imPointsRot,rectPointsRot);
newPoints = imPointsRot(inRect,:);
newPoints = bsxfun(@minus,newPoints,min(newPoints));
newPoints = newPoints * SCALE + 1;

D2 = zeros(round(max(newPoints(:,2))),round(max(newPoints(:,1))));

newInd = sub2ind(size(D2),round(newPoints(:,2)),round(newPoints(:,1)));

D2(newInd) = D(inRect);