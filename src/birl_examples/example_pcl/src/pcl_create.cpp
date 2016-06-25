#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>

// Learn how to create PCL poitn clouds composed solely of pseudorandom points and publish them to /pcl_output. You will learn (i) how to generate point clouds with custom data, and (ii) how to convert them to the corresponding ROS message type in order to broadcast point clouds to subscribers. 

main (int argc, char **argv)
{
    ros::init (argc, argv, "pcl_create");

    ros::NodeHandle nh;
    ros::Publisher pcl_pub = nh.advertise<sensor_msgs::PointCloud2> ("pcl_output", 1);

// pcl has a templated structure pcl::PointCloud that will take one of many possible types of point cloud classes. Most common ones are: pcl::PointXYZ, pcl::PointXYZI, pcl::PointXYZRGB; pcl::PointXYZRGBA; pcl::Normal.
    pcl::PointCloud<pcl::PointXYZ> cloud;
    sensor_msgs::PointCloud2 output;

    // Fill in the cloud data for an ordered point cloud type. 
    cloud.width  = 100;
    cloud.height = 1;
    cloud.points.resize(cloud.width * cloud.height);

    // Assign random locations to the points. (units: cm)
    for (size_t i = 0; i < cloud.points.size (); ++i)
    {
        cloud.points[i].x = 1024 * rand () / (RAND_MAX + 1.0f);
        cloud.points[i].y = 1024 * rand () / (RAND_MAX + 1.0f);
        cloud.points[i].z = 1024 * rand () / (RAND_MAX + 1.0f);
    }

    // Convert the cloud to ROS message
    pcl::toROSMsg(cloud, output);
    output.header.frame_id = "camera_link";

    // Publish the cloud at 1 Hz. 
    ros::Rate loop_rate(1);
    while (ros::ok())
    {
        pcl_pub.publish(output);
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}

