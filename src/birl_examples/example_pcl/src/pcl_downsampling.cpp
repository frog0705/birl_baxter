#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/filters/voxel_grid.h>

/* In this tutorial we will learn how to downsample – that is, reduce the number of points – a point cloud dataset, using a voxelized grid approach.
The VoxelGrid class that we’re about to present creates a 3D voxel grid (think about a voxel grid as a set of tiny 3D boxes in space) over the input point cloud data. Then, in each voxel (i.e., 3D box), all the points present will be approximated (i.e., downsampled) with their centroid. This approach is a bit slower than approximating them with the center of the voxel, but it represents the underlying surface more accurately. 
# Note: Run rosrun examples_pcl pcl_filter before running thsi one.*/

// Tutorial follows: http://pointclouds.org/documentation/tutorials/voxel_grid.php

class cloudHandler
{
public:
    // Constructor: 1 input/1 output
    cloudHandler()
    {
        pcl_sub = nh.subscribe("pcl_filtered", 10, &cloudHandler::cloudCB, this);
        pcl_pub = nh.advertise<sensor_msgs::PointCloud2>("pcl_downsampled", 1);
    }

    void cloudCB(const sensor_msgs::PointCloud2 &input)
    {
        // Create 3 structures: input/ouput for regular pcl. One output for ROS type. 
        pcl::PointCloud<pcl::PointXYZ> cloud;
        pcl::PointCloud<pcl::PointXYZ> cloud_downsampled;
        sensor_msgs::PointCloud2 output;

        // Convert the 'pcl_filterd' ros pc2 to regular pcl 
        pcl::fromROSMsg(input, cloud);

        // Need to instantiate an object for the pcl class that we will use to manipulate the pc.
        // Here the VoxelGrid class will filter the pc according to the leaf size. There are three steps to the filter:
        // (i)   Set the input cloud 
        // (ii)  Set the leaf size
        // (iii) Downsample
        pcl::VoxelGrid<pcl::PointXYZ> voxelSampler;
        voxelSampler.setInputCloud(cloud.makeShared());
        voxelSampler.setLeafSize(0.01f, 0.01f, 0.01f);
        voxelSampler.filter(cloud_downsampled);

        // Convert pcl type to ROS type and publish
        pcl::toROSMsg(cloud_downsampled, output);
        pcl_pub.publish(output);

    }
protected:
    ros::NodeHandle nh;
    ros::Subscriber pcl_sub;
    ros::Publisher pcl_pub;
};

main(int argc, char **argv)
{
    // Initialize the node to pcl_downsampling
    ros::init(argc, argv, "pcl_downsampling");

    // Create an instance of our cloudHandler class
    cloudHandler handler;

    // Do a blocking spin and stay in the callback
    ros::spin();

    return 0;
}

