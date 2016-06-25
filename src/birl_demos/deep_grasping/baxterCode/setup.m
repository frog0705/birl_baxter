% Setup the path. Might have to change this to match your directories
addpath ~/baxterGrasping
addpath ~/baxterGrasping/kinectCalibration/
addpath ~/baxterGrasping/robotCalibration/
addpath ~/baxterGrasping/util/
addpath ~/baxterGrasping/control/
addpath ~/baxterGrasping/graspDetection
addpath ~/baxterGrasping/graspDetection/detectionHelpers
addpath ~/baxterGrasping/visServo/
addpath ~/baxterGrasping/graspOr/

% Sets up your path inside MATLAB's workspace. Yes this is necessary even
% if your path is right in bash
setenv('LD_LIBRARY_PATH','/lib:/opt/ros/groovy/share/roscpp/lib:/opt/ros/groovy/share/roscpp_serialization/lib:/opt/ros/groovy/share/xmlrpcpp/lib:/opt/ros/groovy/share/rosconsole/lib:/opt/ros/groovy/share/roslib/lib:/opt/ros/groovy/share/rospack/lib:/opt/ros/groovy/share/rostime/lib:/opt/ros/groovy/share/cpp_common/lib:/usr/local/lib:/opt/ros/groovy/lib');

% Set up handles to Kinect. Comment this out if you're not using the
% MATLAB-Kinect interface
initHandles;

% This is your path to the learning/offline detection code
REC_CODE_PATH = '~/deepGraspingCode/';

load(sprintf('%s/data/graspModes24.mat',REC_CODE_PATH));
load(sprintf('%s/data/graspWhtParams.mat',REC_CODE_PATH));
load(sprintf('%s/weights/graspWFinal.mat',REC_CODE_PATH));

w_class = w_class(:,1);