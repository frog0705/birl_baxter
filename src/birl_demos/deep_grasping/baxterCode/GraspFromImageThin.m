% Assuming that the RGB and depth channels of an image containing an object
% to be grasped are in the MATLAB workspace as I and D, respectively. If
% this script is called from GraspFromKinectWide, this will always be the
% case. 
%
% Prompts the user to select a region containing an object to be grasped.
% Searches for the optimal grasp in this region, displays it, and asks the
% user if they want to run it. If yes, uses Baxter to execute the grasp,
% hopefully picking up the object in question. 

% Should we use visual servoing to fine-tune the grasping position?
VIS_SERVO = 0;

% Color of the hand camera image background - not used if visual servoing
% isn't
BG_COLOR = [170 170 170]';

setupThinSearch;

bestRects = getGraspForSelectionDisplay(I,D,DBG,w1,w2,w_class,featMeans,featStds,angs,hts,wds,step,trainModes);

fprintf(1,'Run grasp?\n');

k = getkey;

if k ~= 'y'
    fprintf(1,'OK, aborting\n');
    return;
end

fprintf(1,'Running...\n');

[P,or,rotAng] = kinectRectToRobotGrasp3D(squeeze(bestRects(1,:,:)),D,POrK,N,xAxK,yAxK,zAxK,POrR,xAxR,yAxR,zAxR);

gripR = driveGripperToApproachPoseAA(P,or,rotAng);

if VIS_SERVO
    visServoAndGrasp(P,gripR,BG_COLOR);
else
    graspNoServo(P,gripR);
end