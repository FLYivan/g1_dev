import launch
import os

from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import HasNodeParams, RewrittenYaml

def generate_launch_description():




 
    # livox激光雷达启动launch文件
    start_livox_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'livox_ros_driver2'), '/launch_ROS2', '/rviz_MID360_launch.py']),
    )	


    # realsense启动launch文件
    start_realsense_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'realsense2_camera'), '/launch', '/rs_launch.py']),
    )	



    return launch.LaunchDescription([
 
  
        start_livox_launch_file,        # livox激光雷达启动
        start_realsense_launch_file,    # realsense启动





    ])
