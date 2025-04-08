#!/bin/bash
echo "Setup unitree g1 in ros2 environment on desk-pc"
# source /opt/ros/humble/setup.bash
# source $HOME/dog_robot/unitree/unitree_ros2/cyclonedds_ws/install/setup.bash
source $HOME/dog_robot/unitree_go2_ros2_demo/cyclonedds_ws/install/local_setup.bash
source $HOME/human_robot/unitree_g1_ros2_demo/unitree_g1_ros2_function_pkg/install/local_setup.bash

export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><Interfaces>
                            <NetworkInterface name="ens37" priority="default" multicast="default" />
                        </Interfaces></General></Domain></CycloneDDS>'
