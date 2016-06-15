Running "Deep Learning for Detecting Robotic Grasps" code on Baxter:

=== Conventions ===

--- Coordinate frames ---

This code uses four sets of coordinate frames, defined as follows:

Kinect frame: Raw coordinates from Kinect. X axis is image columns, Y axis is
image rows, Z axis is depth. Note that these are not exactly orthongonal, but
don't need to be thanks to the way we handle translating from the Kinect to
global frames.

Global frame: Established by physical markers on the tabletop. Arbitrary as
long as the Z axis points upwards, but typically the X axis should point right
relative to the robot, and the Y axis should point away from the robot. See
below for more instructions on setting up markers.

Robot frame: Baxter's coordinate frame, used for manipulation. Centered 
at Baxter's base. Z axis points upwards, X axis points out of the robot, and
Y axis points left.  

Gripper frame: coordinate frame attached to Baxter's gripper. Z axis points
out of the gripper, Y axis runs parallel to the line between gripper tips,
and X points roughly from the gripper center towards the camera. Origin is
roughly 7.5 cm back along the Z axis from the midpoint of the gripper tips.
Used to make local translations in gripper position, e.g. for approaching and
visual servoing.

=== Physical setup ===

This code assumes that objects are placed on a table in front of Baxter,
at roughly the height of Baxter's base.

You will need to securely mount a Kinect to Baxter's head, angled downwards
at roughly a 75 degree angle towards the table. 

You will also need to mark a set of points corresponding to 3D unit axes.
You'll need markers at (0, 0, 0), (1, 0, 0), (0, 1, 0), and (1, 1, 1) in some
world frame, where the X axis runs left/right relative to Baxter, the Y axis
runs forward/backwards, and the Z axis runs out of the table. These points
correspond to a unit square (with arbitrary units, as long as they're
consistent), with one corner raised one unit above the table. For this corner,
you'll need to use some tall object and mark a point one unit above the table.

The direction of the X and Y axes doesn't matter, as long as the sign is
set during calibration. So, you could mark (0, 0, 0), (-1, 0, 0), (0, 1, 0),
and (-1, 1, 1) for example, and just set X_SIGN = -1 in calibrateRobot.m
and calibrateKinect.m


=== Software ===

This code relies on the MATLAB Kinect package, available at:

http://www.mathworks.com/matlabcentral/fileexchange/30242-kinect-matlab

Which, in turn, relies on the OpenNI Kinect interface. A good tutorial for
installing all the components of OpenNI in Ubuntu can be found at:

http://mitchtech.net/ubuntu-kinect-openni-primesense/

However, the code can also be used with other methods of importing Kinect
data into MATLAB, as long as they produce equal-resolution, aligned images
for the RGB and depth channels. 

This code also assumes that you're using ROS Groovy and have it configured
to work with Baxter.

You'll also need to add the baxter_grasping directory to your ROS workspace
for any commands involving Baxter to work.

=== Setting up your Environment ===

Before running any of the other code, run setup.m

This will set up your MATLAB path and some other environment variables.

To run anything on the robot, you should first enable it with:

rosrun tools enable_robot.py -e


=== Calibration ===

To calibrate the transformation between Kinect's and Baxter's coordinate
frames, you'll need the coordinates of the points laid out above in both
frames. By convention, points will be named as follows:

POr[K/R]: (0, 0, 0)
PX[K/R] : (1, 0, 0)
PY[K/R] : (0, 1, 0)
PZ[K/R] : (1, 1, 1)

with K/R indicating Kinect/Robot. All functions take points as 3D column
vectors. Running calibration scripts will populate the workspace with
[x/y/z]Ax[K/R], corresponding to axis information needed to transform
from Kinect to robot space. Note that the units in these axes may not
be consistent, as Kinect axes are handled differently from robot axes, 
and the Kinect Z axes is handled differently from its X and Y axes.

--- Robot ---

To get coordinates in Baxter's frame, enable Baxter, so you can move the
arms, and use the following command to run the interactive angles and pose
display tool:

rosrun baxter_grasping angles_and_pose

Move the left gripper to each point, and record its coordinates by pressing
 "l". The gripper should be oriented vertically, pointing downwards, with the
midpoint of its tips as close to the midpoint of the marked point as possible.

With POrR, PXR, PYR, and PZR set to the appropriate points in Baxter's
coordinates, run CalibrateRobot.m to compute the robot's frame and store it
in your workspace.

Since the code contains protections to make sure a grasp approach doesn't
run Baxter's gripper into the table, you'll need to set the table height
in TBL_HT in control/graspPositionForPose.m. This should be set to POrR(3)

--- Kinect ---

To get coordinates in Kinect's frame, simply make sure the point markers are
visible from Kinect, then run CalibrateKinect.m. This script will ask you to
select each of the points in a Kinect image, in the order they're listed
above. You'll be asked to draw a box around each point - draw a small
rectangle containing the point, but avoiding any depth discontinuities (e.g
don't go over the edge of the object that PZ is mounted on.) In addition to
the three axes, this will add a variable N corresponding to the table surface
normal in Kinect space to the workspace.

NOTE: Kinect images may appear flipped from left to right, depending on the
Kinect interface used. This is OK - the calibration process will automatically
handle it.


=== Grasping ===

Once the Kinect is calibrated with Baxter, you can use the provided code to 
detect and execute grasps. This also assumes that you've used the recognition
training code to learn a network, which is stored in ../weights

First, you'll need to take a background image from Kinect. This will be used 
to segment objects from the tabletop, and to correct for its slant. Clear the
tabletop and run TakeBackgroundImage.m. 

You'll need to select a physical setting of the grippers for each object to
be grasped. Both of the provided settings use the thinnest set of Baxter
grippers, the "thin" setting mounted at the close positions, so that the 
gripper tips touch when closed, and the "wide" setting mounted at the wide
positions, so that there's about 4 cm distance between the gripper tips when
closed.

Scripts are provided for both these settings, as GraspFromKinect[Thin/Wide].m.
These scripts will take you through the process of executing a grasp. When
prompted to select the grasping region, you can simply select the area in
which you're placing objects - the code will ignore regions containing only
background when searching for grasps. 

This code assumes that only one object is placed in the grasping region. If
multiple objects are present, it will find a grasp for one of them. You can
select a bounding box containing only one to make it grasp that object.

Some settings are included in GraspFromImage[Thin/Wide].m (used by 
GraspFromKinect[Thin/Wide].m as well as for grasping from a provided image)

VIS_SERVO : if 1, will use visual servoing to execute the grasp. See below
for details (default: 0)
BG_COLOR : background color to use for visual servoing from the hand camera.
See below for details. Not used if visual servoing is disabled 
(default: [170 170 170]' - light grey)


--- Visual servoing ---

The visual servoing code provided here requires the following command to be
running:

roslaunch baxter_grasping dumpLeftCamera

This will stream images from the left hand camera to ~/.ros

Because of the way images are numbered, the servoing code won't work if the
output image number passes 10000. In this case, simply stop the command
(using ctrl-C), run ClearHandIms.m, and restart the command after that's
complete.

The visual servoing included with this code will attempt to re-position the
gripper to center the largest visible connected component of foreground pixels
under it. This is determined based on a fixed background color. To determine
the background color you should use, you can aim the hand camera at the 
tabletop and run AveBGColor.m. This will prompt you to select a rectangle
containing only background, and put the average background color in the
aveBGColor variable in your workspace.

Visual servoing may fail in cases where the region to be grasped isn't 
surrounded by background, e.g. the rim of a mug.

--- Other image sources ---

The above assumes you're using the MATLAB Kinect interface described above,
but grasping can be performed from any Kinect interface, as long as the RGB
and depth images can be imported as MATLAB matrices. Import the RGB and depth
background images as IBG and DBG, respectively. Then, import the RGB and depth
images containing objects as I and D, and use GraspFromImage[Thin/Wide].m
to detect and execute grasps. 

For this method, the RGB image in MATLAB's workspace is assumed to be a
480x640x3 double, and the depth image is a 480x640 double.


=== Extending this code ===

While this code is designed for robotic grasping, it provides functionality 
which might be useful for other perception/manipulation tasks on Baxter.
Some useful pieces of code are discussed below:

--- Control ---

The functions in the control directory, along with the provided ROS code,
allow for control of Baxter's end-effector pose using a variety of 
orientation representations. In particular, the Axis/Angle (AA) representation
is useful for many manipulation actions - it lets you specify an axis to
orient the gripper along, and a rotation around that axis. The rotation is
defined relative to a "level" position where the vector between gripper tips
is parallel to the ground plane.

Naming conventions for the driverGripperToPose functions:

Approach : drive to an approach position, set some fixed distance (default is
10 cm) back along the gripper's Z axis (approach vector)

AA : orientation is specified by an axis to align the gripper along, and a
rotation angle around that axis. A 0 degree rotation will align the gripper
so its Y axis is parallel to the ground plane. Function will also return a
rotation matrix for the gripper.

Rot : orientation is specfied by a rotation matrix, relative to the robot's
base frame.

--- Coordinate transformations --- 

Once calibrated, robotCalibration/kinectPointToRobot3D.m will translate a
point from Kinect's coordinate frame to Baxter's. This allows perception
from Kinect to be used for manipulation on Baxter.

--- Visual servoing ---

The code in visServo could be adapted to other visual servoing applications,
such as placing an object in a target area. It also provides a simple way to
access Baxter's hand cameras in MATLAB.

