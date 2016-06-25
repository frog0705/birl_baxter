% Closes Baxter's gripper with maximum force

function closeGripper()

system('rostopic pub -1 /sdk/robot/limb/left/accessory/gripper/command_set baxter_msgs/GripperCommand -- 0 100.0 100.0 100.0 3.0');