#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl/octree/octree.h>

/* Partitioning Point Clouds
Simple idea: We might need to access a local region of a pc or manipulate the neighborhood of specific points. PCL offers two spatial data structures (recall that the standard structure of the point cloud is a 1D array): the kd-tree and the octree. Octrees are nodes, where each node has 8 children. kd-tree is a binary tree in which nodes represent k-dim points. This example will use the octree to: (i) search and (ii) retrieve all poitns surrounding a specific point. 
 */

// API: http://docs.pointclouds.org/1.7.2/a00623.html
// Tutorial: http://pointclouds.org/documentation/tutorials/octree.php#octree-search
class cloudHandler
{
public:
    cloudHandler()
    {
        pcl_sub = nh.subscribe("pcl_downsampled", 10, &cloudHandler::cloudCB, this);
        pcl_pub = nh.advertise<sensor_msgs::PointCloud2>("pcl_partitioned", 1);
    }

    void cloudCB(const sensor_msgs::PointCloud2 &input)
    {
        pcl::PointCloud<pcl::PointXYZ> cloud;
        pcl::PointCloud<pcl::PointXYZ> cloud_partitioned;
        sensor_msgs::PointCloud2 output;

        pcl::fromROSMsg(input, cloud);

        // Octree Searching Algorithm
        float resolution = 128.0f; // Resolution: size of voxels at lowest level of resltn
        pcl::octree::OctreePointCloudSearch<pcl::PointXYZ> octree (resolution);

        octree.setInputCloud (cloud.makeShared());
        octree.addPointsFromInputCloud ();

        // Define he center point of the partition: here handpicked to be near top
        pcl::PointXYZ center_point;
        center_point.x = 0 ;
        center_point.y = 0.4;
        center_point.z = -1.4;

        // Perform search in a radius about center point using radiusSearch
        float radius = 0.5;
        std::vector<int> radiusIdx;
        std::vector<float> radiusSQDist;

        // radiusSearch will output args that return the indices of pts within radius.
        // Sqrd dist from points to center is provided. We can then create cloud_partitioned, which will contain only points belonging to the partition. 
        if (octree.radiusSearch (center_point, radius, radiusIdx, radiusSQDist) > 0)
        {
            for (size_t i = 0; i < radiusIdx.size (); ++i)
            {
                cloud_partitioned.points.push_back(cloud.points[radiusIdx[i]]);
            }
        }

        pcl::toROSMsg(cloud_partitioned, output);
        output.header.frame_id = "camera_link";
        pcl_pub.publish(output);
    }

protected:
    ros::NodeHandle nh;
    ros::Subscriber pcl_sub;
    ros::Publisher pcl_pub;
};

main(int argc, char **argv)
{
    ros::init(argc, argv, "pcl_partitioning");

    cloudHandler handler;

    ros::spin();

    return 0;
}
