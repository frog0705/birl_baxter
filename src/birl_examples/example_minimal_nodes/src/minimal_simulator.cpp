#include<ros/ros.h>
#include<std_msgs/Float64.h>

std_msgs::Float64 g_velocity;
std_msgs::Float64 g_force;

// This callback uses force data to compute the acceleration
void myCallaback(const std_msgs::Float64& message_holder)
{
  // check for messages on topic "force_cmd"
  ROS_INFO("received force value is: %f",message_holder.data);
  g_force.data = message_holder.data;	// post the data to global variable for access by main program.
}

int main(int argc,char**argv)
{
  ros::init(argc,argv,"minimal_simulator");	// name this node.
  ros::NodeHandle nh; 

  // Create a subscriber object to receive force
  ros::Subscriber my_subscriber_object=nh.subscribe("force_cmd",1,myCallaback);

  // Create a publisher object to publish velocity. Rate 1Hz. 
  ros::Publisher my_publisher_object=nh.advertise<std_msgs::Float64>("velocity",1);

  // Compute differential velocity
  double mass = 	1.0;	// mass in kg
  double dt = 		0.01; 	// 10ms integration time step
  double sample_rate =  1.0/dt; // frequency: 100Hz
  g_velocity.data = 	0.0;   	// initialize velocity to zero
  g_force.data = 	0.0;	// initialize force to zero. will be updated by callback.

  // Set ros rate for operations (spinOnce)
  ros::Rate loopRate(sample_rate); // 100Hz

  while(ros::ok())
    {
      // 1. Compute velocity. 
      g_velocity.data=g_velocity.data+(g_force.data/mass)*dt; // Euler integration of acceleration
      // 2. Publish velocity at 1Hz.
      my_publisher_object.publish(g_velocity);

      // 3. Print data
      ROS_INFO("velocity=%f",g_velocity.data);

      // 4. Allow force data to be updated. 
      // Simulator loop 100Hz. Updated force variable in callback will be set at  10Hz, outside the program. 
      // Force will be updated 1/10 messages. 
      // Callback will not block this loop. It is allowed to repeat its iterations at the higher rate. 
      ros::spinOnce(); // Checks callbacks at the rate of sample_rate. 
      loopRate.sleep(); // this loop rate is faster that then update of 10Hz controller. 
    }
  return 0;
}
