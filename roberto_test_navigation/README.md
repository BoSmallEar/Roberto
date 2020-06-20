# Roberto Test Navigation

## Instructions to Run
1. Clone the repository into the src directory of your catkin workspace.
2. Make sure the `tiago_gazebo` directory is in the catkin workspace (it comes with the tiago installation).
3. Open the robot in gazebo with
    ```
    $ roslaunch roberto_test_navigation start_navigation.launch
    ```
4. Perform MCL algorithm to localize
    ```
    $ roslaunch roberto_test_navigation initialize_navigation.launch
    ```
5. In launch/goal_publisher.launch, specify the args to indicate the name of the path file that you want to run. Then run
    ```
    $ roslaunch roberto_test_navigation goal_publisher.launch
    ```
All of the path files we use for the demo of this project are located in data/ and named from 'path1' to path7. 