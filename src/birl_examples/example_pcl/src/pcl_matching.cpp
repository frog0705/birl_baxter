#include <ros/ros.h>
#include <pcl/point_cloud.h>
#include <pcl/registration/icp.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>

/* Simple Intro: technique used to find common features in two datasets and use them to stich the data sets together. That may be finding where one dataset ends, and where the other starts. Useful for moving sources at high rage and having an estimate of the movement source.

Detailed Description: The problem of consistently aligning various 3D point cloud data views into a complete model is known as registration. Its goal is to find the relative positions and orientations of the separately acquired views in a global coordinate framework, such that the intersecting areas between them overlap perfectly. For every set of point cloud datasets acquired from different views, we therefore need a system that is able to align them together into a single point cloud model, so that subsequent processing steps such as segmentation and object reconstruction can be applied. 

The algorithmic work in the PCL registration library is motivated by finding correct point correspondences in the given input datasets, and estimating rigid transformations that can rotate and translate each individual dataset into a consistent global coordinate framework. This registration paradigm becomes easily solvable if the point correspondences are perfectly known in the input datasets. This means that a selected list of points in one dataset have to “coincide” from a feature representation point of view with a list of points from another dataset. Additionally, if the correspondences estimated are “perfect”, then the registration problem has a closed form solution.

PCL contains a set of powerful algorithms that allow the estimation of multiple sets of correspondences, as well as methods for rejecting bad correspondences, and estimating transformations in a robust manner from them. The following sections will describe each of them individually.

We sometimes refer to the problem of registering a pair of point cloud datasets together as pairwise registration, and its output is usually a rigid transformation matrix (4x4) representing the rotation and translation that would have to be applied on one of the datasets (let’s call it source) in order for it to be perfectly aligned with the other dataset (let’s call it target, or model).

The pipeline looks as follows: 
(i)   data acquisition
(ii)  keypoint estimation: points w/ special proerties (NARF, SIFT, FAST).
(iii) feature descriptors estimation: extract vectors (NARF, FPFH, BRIEF, SIFT).
(iv)  correspondances estimation: find overlap based on features (brute-force, kd-tree, search in img/index space)
(v)   correspondance rejection: reject poor correspondances. 
(vi)  transformation estimation: eval error metric to compute.

Common Pipeline Alg's:
(a) ICP: search correspondances, reject bad correspondances, estimate transform, iterate.
(b) Feat. Registration: SIFT-keypoints, FPFH descriptors, pcl::CorrespondanceEsitmation, pcl::CorrespondanceRejectionXXX
 */

// Tutorial: http://pointclouds.org/documentation/tutorials/registration_api.php#registration-api

class cloudHandler
{
public:
    cloudHandler()
    {
        pcl_sub = nh.subscribe("pcl_downsampled", 10, &cloudHandler::cloudCB, this);
        pcl_pub = nh.advertise<sensor_msgs::PointCloud2>("pcl_matched", 1);
    }

    void cloudCB(const sensor_msgs::PointCloud2 &input)
    {
        // Need two data sources to compare
        pcl::PointCloud<pcl::PointXYZ> cloud_in;
        pcl::PointCloud<pcl::PointXYZ> cloud_out;
        
        // Stiched cloud 
        pcl::PointCloud<pcl::PointXYZ> cloud_aligned;
        sensor_msgs::PointCloud2 output;

        pcl::fromROSMsg(input, cloud_in);

        // Generate the 2nd data source from the first.
        cloud_out = cloud_in;

        for (size_t i = 0; i < cloud_in.points.size (); ++i)
        {
            cloud_out.points[i].x = cloud_in.points[i].x + 0.7f;
        }

        // ICP
        pcl::IterativeClosestPoint<pcl::PointXYZ, pcl::PointXYZ> icp;
        icp.setInputSource(cloud_in.makeShared());
        icp.setInputTarget(cloud_out.makeShared());

        // Params
        icp.setMaxCorrespondenceDistance(5);  // min dist 2 corr pts need to be considered

        // Stoping Conditions
        icp.setMaximumIterations(100);        // No more than this number of iters
        icp.setTransformationEpsilon (1e-12); // Diff between prev/curr transforms < e
        icp.setEuclideanFitnessEpsilon(0.1);  // Limit for sum of Euc. squared errors 

        // Work the magic (SVD for transformations)
        icp.align(cloud_aligned);

        pcl::toROSMsg(cloud_aligned, output);
        pcl_pub.publish(output);
    }

protected:
    ros::NodeHandle nh;
    ros::Subscriber pcl_sub;
    ros::Publisher pcl_pub;
};

main(int argc, char **argv)
{
    ros::init(argc, argv, "pcl_matching");

    cloudHandler handler;

    ros::spin();

    return 0;
}
