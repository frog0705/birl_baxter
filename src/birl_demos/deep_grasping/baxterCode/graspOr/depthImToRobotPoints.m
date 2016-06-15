% Convert a depth image to a set of X,Y,Z robot points. Returns each of the
% coordinates as a separate matrix. Very expensive, and shouldn't be used
% on a large depth image.

function [X,Y,Z] = depthImToRobotPoints(D,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR)

X = zeros(size(D));
Y = zeros(size(D));
Z = zeros(size(D));

for r = 1:size(D,1)
    for c = 1:size(D,2)
        curP = [c r D(r,c)]';

        robP = kinectPointToRobot3D(curP,[0 0 POrK(3)]',NK,xAxK,yAxK,zAxK,[0 0 0]',xAxR,yAxR,zAxR);
        
        X(r,c) = robP(1);
        Y(r,c) = robP(2);
        Z(r,c) = robP(3);
    end
end