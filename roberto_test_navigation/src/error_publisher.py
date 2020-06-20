#! /usr/bin/env python

import rospy 
import math
from std_msgs.msg import Float32
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
from nav_msgs.msg import Odometry

def callback1(msg):
    global current_pose
    current_pose = msg.pose.pose
   

def callback2(msg):
    global current_odom
    current_odom = msg.pose.pose
 


rospy.init_node('error_publisher',log_level=rospy.INFO) 

current_pose = Pose()
current_odom = Pose()

pub1 = rospy.Publisher('/error_position',Float32, queue_size=1000)
pub2 = rospy.Publisher('/error_quaternion',Float32, queue_size=1000)
sub1 = rospy.Subscriber('/robot_pose',PoseWithCovarianceStamped, callback1)
sub2 = rospy.Subscriber('/ground_truth_odom',Odometry, callback2)

 
rospy.loginfo("Start publishing error")
rate = rospy.Rate(10) 

error1 = Float32()
error2 = Float32()

while (True):
    
    error1.data = math.sqrt((current_pose.position.x-(1.0085*current_odom.position.x + 5.6594))**2 + (current_pose.position.y-(current_odom.position.y*0.9635 +11.8493))**2 + (current_pose.position.z-current_odom.position.z)**2)
    error2.data = 2*math.acos(abs(current_pose.orientation.x * current_odom.orientation.x + current_pose.orientation.y * current_odom.orientation.y + current_pose.orientation.z * current_odom.orientation.z + current_pose.orientation.w * current_odom.orientation.w))
    pub1.publish(error1)
    pub2.publish(error2)
    rate.sleep()
