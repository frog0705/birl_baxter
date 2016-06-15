#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/filters/passthrough.h>

// Tutorial follows: http://pointclouds.org/documentation/tutorials/passthrough.php#passthrough
// API & Example: http://docs.pointclouds.org/trunk/classpcl_1_1_pass_through.html
/* In this tutorial we will learn how to perform a simple filtering along a specified dimension – that is, cut off values that are either inside or outside a given user range. */

class cloudHandler
{
public:
    // Constructor: 1 input/1 output
    cloudHandler()
    {
        pcl_sub = nh.subscribe("pcl_output", 10, &cloudHandler::cloudCB, this);
        pcl_pub = nh.advertise<sensor_msgs::PointCloud2>("pcl_filtered", 1);
    }

    void cloudCB(const sensor_msgs::PointCloud2 &input)
    {
        // create input and output structures
        pcl::PointCloud<pcl::PointXYZ> cloud;
        sensor_msgs::PointCloud2 output;

        // Convert the 'pcl_filterd' ros pc2 to regular pcl 
        pcl::fromROSMsg(input, cloud);

        // Instantiate algorithm class for the passthrough filter
        pcl::PassThrough<pcl::PointXYZ> pt;
        pt.setInputCloud(cloud.makeShared()); // copy (deep copy) cloud to heap, return smart ptr.
        pt.setFilterLimits(0.0, 0.5);
        pt.setFilterFieldName("z"); // can be "x" or "xz" etc. 

        // Convert pcl type to ROS type and publish
        pcl::toROSMsg(cloud, output);
        pcl_pub.publish(output);

    }
protected:
    ros::NodeHandle nh;
    ros::Subscriber pcl_sub;
    ros::Publisher pcl_pub;
};

main(int argc, char **argv)
{
    // Initialize the node to pcl_passthrough
    ros::init(argc, argv, "pcl_passthrough");

    // Create an instance of our cloudHandler class
    cloudHandler handler;

    // Do a blocking spin and stay in the callback
    ros::spin();

    return 0;
}

