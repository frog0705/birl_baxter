#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/filters/statistical_outlier_removal.h>

/*StatisticalOutlierRemoval uses point neighborhood statistics to filter outlier data.

The algorithm iterates through the entire input twice: During the first iteration it will compute the average distance that each point has to its nearest k neighbors. The value of k can be set using setMeanK(). Next, the mean and standard deviation of all these distances are computed in order to determine a distance threshold. The distance threshold will be equal to: mean + stddev_mult * stddev. The multiplier for the standard deviation can be set using setStddevMulThresh(). During the next iteration the points will be classified as inlier or outlier if their average neighbor distance is below or above this threshold respectively. 
  The neighbors found for each query point will be found amongst ALL points of setInputCloud(), not just those indexed by setIndices(). The setIndices() method only indexes the points that will be iterated through as search query points. */

// API: http://docs.pointclouds.org/1.7.2/a01212.html#details
class cloudHandler
{
public:
    cloudHandler()
    {
        pcl_sub = nh.subscribe("pcl_output", 10, &cloudHandler::cloudCB, this);
        pcl_pub = nh.advertise<sensor_msgs::PointCloud2>("pcl_filtered", 1);
    }

    void cloudCB(const sensor_msgs::PointCloud2& input)
    {
        pcl::PointCloud<pcl::PointXYZ> cloud;
        pcl::PointCloud<pcl::PointXYZ> cloud_filtered; // Used to set the filtered pcl cloud
        sensor_msgs::PointCloud2 output; // Used to publish in ROS

        pcl::fromROSMsg(input, cloud);

        pcl::StatisticalOutlierRemoval<pcl::PointXYZ> statFilter;
        statFilter.setInputCloud(cloud.makeShared());
        statFilter.setMeanK(10); // set the number of neighbors to compute mean distance
        statFilter.setStddevMulThresh(0.2); // set the number of std. deviations
        statFilter.filter(cloud_filtered); // write the new filtered cloud here

        pcl::toROSMsg(cloud_filtered, output);
        pcl_pub.publish(output);
    }

protected:
    ros::NodeHandle nh;
    ros::Subscriber pcl_sub;
    ros::Publisher pcl_pub;
};

main(int argc, char** argv)
{
    ros::init(argc, argv, "pcl_filter");

    cloudHandler handler;

    ros::spin();

    return 0;
}

