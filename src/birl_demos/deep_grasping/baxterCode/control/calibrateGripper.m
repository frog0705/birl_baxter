% Runs the calibration routine for Baxter's gripper. Needs to be run once
% before any other gripper actions can be run.

function calibrateGripper()

system('rostopic pub -1 /robot/limb/left/accessory/gripper/command_calibrate std_msgs/Empty');