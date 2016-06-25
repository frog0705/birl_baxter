function [P,or,rotAng] = kinectRectToRobotGrasp3D(rect, D, POrK, N, xAxK, yAxK, zAxK, POrR, xAxR, yAxR, zAxR)

[or, minD] = robotNormAroundClosestPt(D,rect,POrK,N,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR);


% Figure out the center points of the gripper plates
gP1 = round(fliplr(mean(rect(1:2,:))));
gP2 = round(fliplr(mean(rect(3:4,:))));
gCent = round(mean([gP1; gP2]))';
gCent(3) = minD;


%or = or.*[-1 -1 1]';

gripDiff = gP2 - gP1;

rotAng = atan2(gripDiff(2),-gripDiff(1));

or = snapToVert(-or,rotAng);

P = kinectPointToRobot3D(gCent, POrK, N, xAxK, yAxK, zAxK, POrR, xAxR, yAxR, zAxR);
