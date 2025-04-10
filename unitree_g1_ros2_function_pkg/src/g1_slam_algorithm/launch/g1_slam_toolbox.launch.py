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

    slam_params_file = LaunchConfiguration('slam_params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # 获取launch文件和定义地址
    bringup_dir = get_package_share_directory("g1_slam_algorithm")

    # 获取rviz配置文件路径
    rviz_file = os.path.join(
        get_package_share_directory('g1_slam_algorithm'),
        'rviz',
        'dog_slam_simp.rviz'
    )


    # 声明slam-toolbox启动时，参数文件的默认地址
    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(bringup_dir,'config', 'mapper_params_online_async.yaml'),                
        description='Full path to the slam parameters file to use for the slam_toolbox node')
    

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='False',
        description='Use simulation (Gazebo) clock if true')

    
    
    # 使用自定义odom，进行tf关系发布节点
    start_cus_tftree_node =  Node(
            package='g1_slam_algorithm',                      
            executable='motion_to_tf',             
            name='motion_to_tf',
            output='screen',
        )
    
    # slam-toolbox节点
    start_async_slam_toolbox_node = Node(
            parameters=[
                slam_params_file,
                {'use_sim_time': use_sim_time}
            ],
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            # remappings=[
            #         ('/map', '/map_slamtoolbox_g1')  # 将 /map 重映射为 /map_slamtoolbox_g1
            #          ]
        )
 
    # 激光frame_id修改launch文件
    start_lidar_launch_file = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'g1_lidar_processing'), '/launch', '/cloud_to_scan.launch.py']),
    )	


    # RViz2节点
    start_rviz_node =Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_file],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        )

    # 运动轨迹显示节点
    start_traject_node =  Node(
        package='g1_slam_algorithm',                      
        executable='trajectory_visualizer',             
        name='trajectory_visualizer',
        output='screen',
    )



    return launch.LaunchDescription([

        
        declare_slam_params_file_cmd,
        declare_use_sim_time_cmd,
  
        start_lidar_launch_file,        # 启动激光frame_id修改launch文件
        start_cus_tftree_node,
        start_async_slam_toolbox_node,  # slam-toolbox算法节点
        start_rviz_node,
        # start_traject_node,             # 运动轨迹显示节点



    ])
