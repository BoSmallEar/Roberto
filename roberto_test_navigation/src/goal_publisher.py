#! /usr/bin/env python

import rospy
import os
import sys
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

def callback(msg):
    global status
    if msg.status.status == msg.status.SUCCEEDED:
        status = 1
        rospy.loginfo("Current goal reached")
    else:    
        status = 2
        rospy.logerr("Current goal failed!!!")


rospy.init_node('goal_publisher',log_level=rospy.INFO) 

path_file = open("/home/zzliu/roberto_navigation/roberto_ws/src/roberto_test_navigation/data/"+str(sys.argv[1])+".txt","r")
num_goals = int(path_file.readline())
rospy.loginfo("Read file successfully!")

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1000)
sub = rospy.Subscriber('/move_base/result',MoveBaseActionResult, callback)
while (pub.get_num_connections() == 0):
    continue  
cmd = PoseStamped() 
cmd.header.frame_id = 'map'

x_transform = 6.502378 - 0.777284
y_transform = 1.0866362 - (-11.0984)

for it in range(num_goals):
    goal_list = path_file.readline().split()
    cmd.pose.position.x = float(goal_list[0]) + x_transform
    cmd.pose.position.y = float(goal_list[1]) + y_transform
    cmd.pose.position.z = float(goal_list[2])
    cmd.pose.orientation.x = float(goal_list[3])
    cmd.pose.orientation.y = float(goal_list[4])
    cmd.pose.orientation.z = float(goal_list[5])
    cmd.pose.orientation.w = float(goal_list[6])
    rospy.loginfo("Current goal: %s", cmd.pose)
    status = 0

    pub.publish(cmd) 
    while status == 0:
        continue
    if status != 1: 
        break

if status == 1:
    rospy.loginfo("Success! All goals have been reached!")
else:
    rospy.logerr("Failed on node %d!!!",it)


 
