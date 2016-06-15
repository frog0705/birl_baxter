% Compute the average column value of masked-in pixels for the given binary
% mask

function centC = centerColOfMask(M)

centC = sum(sum(bsxfun(@times,M,1:size(M,2))))/sum(M(:));