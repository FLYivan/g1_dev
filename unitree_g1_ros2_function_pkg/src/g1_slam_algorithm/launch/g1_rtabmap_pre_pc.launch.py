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
    # 输入参数声明


    
    # 使用自定义odom，进行tf关系发布节点
    start_cus_tftree_node =  Node(
            package='g1_slam_algorithm',                      
            executable='motion_to_tf',             
            name='motion_to_tf',
            output='screen',
        )
    

 
    # 激光frame_id修改launch文件
    start_lidar_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_lidar_processing'), '/launch', '/cloud_to_scan.launch.py']),
    )	


    # g1的URDF发布launch文件
    start_urdf_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_sim'), '/launch', '/g1_urdf2tf.launch.py']),
    )	



    return launch.LaunchDescription([
 
  
        start_lidar_launch_file,        # 启动激光frame_id修改launch文件
        start_urdf_launch_file,
        # start_realsense_launch_file,


        start_cus_tftree_node,



    ])
