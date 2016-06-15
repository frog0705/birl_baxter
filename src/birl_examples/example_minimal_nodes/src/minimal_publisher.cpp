#include <ros/ros.h>
#include <std_msgs/Float64.h>
int main(int argc, char **argv)
{
  ros::init(argc,argv,"minimal_publisher1"); 	// name of this node will be "minimal_publisher1"
  ros::NodeHandle n; 				// two lines to create a publisher object that can talk to ROS
  ros::Publisher my_publisher_object = n.advertise<std_msgs::Float64>("topic1",1);
  //"topic1" is the name of the topic to which we will publish
  // the "1" argument says to use a buffer size of 1; could make larger, if expect network backups
  std_msgs::Float64 input_float; 		//create a variable of type "Float64", as defined in: /opt/ros/fuerte/share/std_msgs
  // any message published on a ROS topic must have a pre-defined format, so subscribers know how to
  // interpret the serialized data transmission
  input_float.data=0.0;

  // ROS Rates
  ros::Rate loopRate(1000); 	       		// Create a ros::Rate object. Set the time for a 1Hz sleeper timer.
  while(ros::ok()) 				// do work here in infinite loop (desired for this example), but terminate if detect ROS has faulted
    {
      // this loop has no sleep timer, and thus it will consume excessive CPU time
      // expect one core to be 100% dedicated (wastefully) to this small task
      input_float.data = input_float.data+0.001; // increment by 0.001 each iteration
      my_publisher_object.publish(input_float);  // publish the value--of type Float64-- to the topic "topic1"
      loopRate.sleep();				// The call to sleep makes this node's while loop to be called every 1Hz.
    }
}
