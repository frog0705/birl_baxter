cmake_minimum_required(VERSION 2.8.3)
project(example_button_gui)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  qt_gui
  rospy
  rqt_gui
)

catkin_python_setup()
catkin_package()

install(FILES plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY resource
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(PROGRAMS scripts/example_button_gui.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# cmake_minimum_required(VERSION 2.8.3)
# project(example_gui_pub)

# find_package(catkin_simple REQUIRED)
# catkin_python_setup()
# catkin_simple()

# # example boost usage
# # find_package(Boost REQUIRED COMPONENTS system thread)

# # C++0x support - not quite the same as final C++11!
# # SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")

# # Libraries
# # cs_add_library(my_lib src/my_lib.cpp)   

# # Executables
# # cs_add_executable(example src/example.cpp)
# # target_link_library(example my_lib)

# cs_install()
# cs_export()
    