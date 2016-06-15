#include <iostream>
#include <ros/ros.h>
#include <pcl/visualization/cloud_viewer.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>

/* PCL provides many ways to visualize point clouds. The simplest is through the basic cloud viewer, which can visualize all PCL point cloud types. It also provides a set of callbacks for user interaction. */

// Tutorial: http://pointclouds.org/documentation/tutorials/cloud_viewer.php#cloud-viewer
class cloudHandler
{
public:
    // Our class will inherit and acquire the viewer instance. 
    cloudHandler()
    : viewer("Cloud Viewer")
    {
        pcl_sub = nh.subscribe("pcl_output", 10, &cloudHandler::cloudCB, this); // set the callback to a public member of the class.

        // Timer will be used to trigger a callback every 100ms and check if the window has been closed. If so, shut down the node. 
        viewer_timer = nh.createTimer(ros::Duration(0.1), &cloudHandler::timerCB, this);
    }

    // The callback function is a public member of the class
    void cloudCB(const sensor_msgs::PointCloud2 &input)
    {
        pcl::PointCloud<pcl::PointXYZ> cloud;
        pcl::fromROSMsg(input, cloud);

        viewer.showCloud(cloud.makeShared());
    }

    void timerCB(const ros::TimerEvent&)
    {
        if (viewer.wasStopped())
        {
            ros::shutdown();
        }
    }

protected:
    ros::NodeHandle nh;
    ros::Subscriber pcl_sub;
    pcl::visualization::CloudViewer viewer;
    ros::Timer viewer_timer;
};

main (int argc, char **argv)
{
    ros::init (argc, argv, "pcl_visualize");

    cloudHandler handler;
    ros::spin();

    return 0;
}
