cmake_minimum_required(VERSION 2.8.3)
project(example_baxter_kinematics)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  baxter_interface
  baxter_core_msgs
  #python_orocos_kdl
  roscpp
  rospy
  geometry_msgs
  sensor_msgs
  tf
  #urdfdom
)

catkin_python_setup()

catkin_package(
   CATKIN_DEPENDS 
   baxter_interface 
   baxter_core_messages
   # python_orocos_kdl 
   geometry_msgs
   sensor_msgs
   roscpp 
   rospy 
   tf   
   # urdfdom
   DEPENDS
   python_orocos_kdl
   urdfdom
)

install(
  DIRECTORY scripts/
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  USE_SOURCE_PERMISSIONS
)
