#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/io/pcd_io.h>

/* PCL provides a standard format to load and store point clouds to disk. The format is called PCD. It starts with a header containg info about the point cloud, followed by a list of points conforming to the specified type. Below is an example of how to read a file through PCL's API*/

// To learn about the PCD file format: 
// http://pointclouds.org/documentation/tutorials/pcd_file_format.php#pcd-file-format
// Reading PC data from PCD Fiels tutorial:
// http://pointclouds.org/documentation/tutorials/reading_pcd.php#reading-pcd

main(int argc, char **argv)
{
    ros::init (argc, argv, "pcl_read");

    ros::NodeHandle nh;
    ros::Publisher pcl_pub = nh.advertise<sensor_msgs::PointCloud2> ("pcl_output", 1);

    sensor_msgs::PointCloud2 output;
    pcl::PointCloud<pcl::PointXYZ> cloud;
    
    // Load data from file. See API: http://docs.pointclouds.org/1.7.2/a02409.html
    // Remember that before running this file you should change to the folder with the file
    pcl::io::loadPCDFile ("test_pcd.pcd", cloud);

    pcl::toROSMsg(cloud, output);
    output.header.frame_id = "camera_link";

    ros::Rate loop_rate(1);
    while (ros::ok())
    {
        pcl_pub.publish(output);
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}

