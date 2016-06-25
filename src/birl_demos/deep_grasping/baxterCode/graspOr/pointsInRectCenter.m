% Computes a mask for points in the center of a given rectangle in the
% given depth image.

function inRect = pointsInRectCenter(D,rectPoints)

if any(isnan(rectPoints(:)))
    inRect = NaN;
    return;
end

gripAng = atan2(rectPoints(1,2) - rectPoints(2,2),rectPoints(1,1)-rectPoints(2,1));
[imX,imY] = meshgrid(1:size(D,2),1:size(D,1));
imPoints = [imX(:),imY(:)];

alignRot = rotMat2D(gripAng);

rectPointsRot = rectPoints * alignRot;
imPointsRot = imPoints * alignRot;

inRect = pointsInAARectCenter(imPointsRot,rectPointsRot);
inRect = reshape(inRect,size(D));