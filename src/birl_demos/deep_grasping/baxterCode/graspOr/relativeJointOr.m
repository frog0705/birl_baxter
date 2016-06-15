% Computes the relative orientation of the link running from the index
% fromInd to the index toInd, where P defines the location of each joint,
% and R similarly defines rotations. This orientation is computed relative
% to the frame of the joint with index frameInd
%
% Typically, fromInd and toInd will be two sequential joints connected by a
% link, and frameInd will be the frame of the joint previous to the joint
% at fromInd. This is necessary since in NITE skeletons, the frame at each
% joint is relative to the next link down the chain, e.g. the shoulder
% frame is oriented towards the elbow, etc., but we care about the
% orientation w/r/t the previous joint, i.e. we care about how the upper
% arm is oriented w/r/t the shoulder
%
% We flip the x axis of the coordinate frame for the left arm to make
% representations symmetric.
%
% Don't bother computing roll because it isn't relevant for most links
% (NITE won't give us forearm roll, for example). getRollForRotParams will
% compute the roll

function [az,el] = relativeJointOr(P,R,fromInd,toInd,frameInd)

% Flip x axis when computing coords if we're looking at one of the left-arm
% links 
xSign = xSignForJoint(toInd);

V = P(toInd,:) - P(fromInd,:);

[az,el] = relativePolar(V,squeeze(R(frameInd,:,:)),xSign);