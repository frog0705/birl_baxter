% Computes the robot-space surface normals for a given depth image. All
% points in the image are first converted to X,Y,Z robot-space coordinates,
% then the normals are computed

function N = getSurfNormRobot(D,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR)

[X,Y,Z] = depthImToRobotPoints(D,POrK,NK,xAxK,yAxK,zAxK,xAxR,yAxR,zAxR);

[Nx, Ny, Nz] = surfnorm(X,Y,Z);

N = zeros([size(Nx,1) size(Nx,2) 3]);
N(:,:,1) = Nx;
N(:,:,2) = Ny;
N(:,:,3) = Nz;

N = bsxfun(@rdivide,N,sqrt(sum(N.^2,3)));