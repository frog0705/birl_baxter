#ifndef CONTROLLER_
#define CONTROLLER_

#include <ros/ros.h>
#include <eigen3/Eigen/LU>
#include <eigen3/Eigen/Core>
#include <sensor_msgs/JointState.h>
#include <baxter_core_msgs/EndpointState.h>
#include <baxter_core_msgs/SEAJointState.h>
#include <geometry_msgs/Wrench.h>
#include <geometry_msgs/Vector3.h>
#include <force_controller/forceControl.h>
#include <force_controller/kinematics.h>

#include <istream>
#include <ostream>
#include <fstream>

#define PI 3.141592654

namespace force_controller

{
  static const int LEFT = 0, RIGHT = 1;
  static const double COEFF[2][7][3] = {
    { {0.045284, 0.412655, -0.102458}, {-13.645011, 15.076427, -2.089347 }, {9.605912, 46.06344, 53.876335}, 
      {0.175529, -0.174395, -1.880203}, {2.788387, -3.276785, 1.355042}, {-0.224896, 0.726712, -0.299096}, {-0.295167, 1.183197, -0.832453} },
    { {-0.881133, 0.4475, 0.108815}, {24.779869, -44.860449, 17.881954}, {-4.511136, 22.0123, -24.573247}, 
      {0.17174, -0.207249, -0.946106}, {-2.530283, -3.267953, -0.817067}, {-0.554553, 1.847279, -1.338913}, {0.144515, 0.506907, 0.507274} }	  
  };

  class controller
  {
  public:
   
    // Constructor
  	controller(ros::NodeHandle node): node_handle_(node)
	  {
      n_ = 0;		m_ = 0;	no_ = 0;
      double gain;
      int nj;

      /*** Get Parameter Values ***/
      // Strings
      node_handle_.param<std::string>("side", side_, "right");
      node_handle_.param<std::string>("tip_name", tip_name_, "right_gripper");

      // Gains
      node_handle_.param<double>("gain_force", gain, 0.00005);
      gF_ = Eigen::Vector3d::Constant(gain);
      node_handle_.param<double>("gain_moment", gain, 0.0000035);
      gM_ = Eigen::Vector3d::Constant(gain);
      error_ = Eigen::VectorXd::Zero(6);

      // State
      exe_ = false;	jo_ready_ = false;

      // Subscriber and Service Advertisement
      joints_sub_ = root_handle_.subscribe<baxter_core_msgs::SEAJointState>("/robot/limb/" + side_ + "/gravity_compensation_torques", 1, &controller::updateJoints, this);
      ctrl_server_ = root_handle_.advertiseService("/" + side_ + "/force_controller", &controller::execute, this); // Creates service.

      // Create the kinematic chain/model through kdl from base to right/left gripper
	    kine_model_ = Kinematics::create(tip_name_, nj);

      // Clear torque and gravitational torque vectors.
      torque_.clear();
      tg_.clear();

      // Confirm 7 DoF
      if(nj == 7)
        {
          fillJointNames();
          init_ = true;
        }

      // Print successfull exit.
      ros::Duration(1.0).sleep();
      ROS_INFO("Force controller on baxter's %s arm is ready", side_.c_str());
	  }

    // Destructor
    ~controller() { }

	  inline bool start()
	  {
      return init_;
	  }


	private:

	  void fillJointNames();
	  Eigen::VectorXd getTorqueOffset();
	  sensor_msgs::JointState fill(Eigen::VectorXd dq);
	  Eigen::Vector3d getWrenchEndpoint(std::string type);
	  std::vector<double> toVector(const geometry_msgs::Vector3& d);

	  bool JacobianProduct(std::string type, Eigen::VectorXd& update);
	  bool execute(forceControl::Request &req, forceControl::Response &res);
	  void updateJoints(const baxter_core_msgs::SEAJointStateConstPtr& state);
	  void updateGains(std::vector<geometry_msgs::Vector3> gain, std::vector<std::string> type);
	  bool NullSpaceProjection(std::vector<Eigen::VectorXd> updates, sensor_msgs::JointState& dq);
	  bool ComputePrimitiveController(std::vector<Eigen::VectorXd>& update, std::string type, geometry_msgs::Vector3 desired, std::vector<double>& e);
    // double computeError(...) // inline method below.

    /*** Inline Methods ***/
	  inline void ini()
	  {
      std::ostringstream num2;
      num2 << "s" << m_ << "__" << "Joints_" << side_ << "_sim.txt";
      std::string title2 = num2.str();
      char * name2 = new char [title2.length()+1];
      std::strcpy (name2, title2.c_str());

      save_.open(name2, std::ios::out);
      exe_ = true;
	  }

	  inline void fin()
	  {
      exe_=false;
      if(save_.is_open())
        save_.close();

      joints_sub_.shutdown();
	  }

	  inline double computeError(std::string type, Eigen::Vector3d xt, Eigen::Vector3d xd)
	  {
      double mag;
      int offset =0;
      if(type == "moment")
        offset = 3;

      error_ = Eigen::VectorXd::Zero(6);
      for(unsigned int i=0; i<3; i++)
        error_(i+offset) = xt(i) - xd(i);

      mag = error_.norm();
      return mag;
	  }

    // ROS Types: node handle, subscriber, service server. 
	  ros::Subscriber endPoint_sub_, joints_sub_;
	  ros::NodeHandle node_handle_, root_handle_;
	  ros::ServiceServer ctrl_server_;

    // Kinematics model pointers.
	  Kinematics::Ptr kine_model_;
	 
	  std::string side_, tip_name_;
	  std::vector<std::string> joints_names_;

	  Eigen::Vector3d gF_, gM_;
	  Eigen::VectorXd error_;
	  std::vector<double> j_t_1_, tm_t_1_, tg_t_1_;
	  std::vector<std::vector<double> > joints_, torque_, tg_;

	  bool init_, exe_, jo_ready_;
	  int n_, no_, m_, points_;
	  std::ofstream save_;

	  ros::Time to_;
  };

}

#endif /* REPLAY_ */
