function openGripper()

system('rostopic pub -1 /sdk/robot/limb/left/accessory/gripper/command_set baxter_msgs/GripperCommand -- 100.0 30.0 100.0 0.0 3.0');